import sqlite3, os, copy

from typing import List, Tuple, Any

import tolio


class Database:
  def __init__(self, db_path: str = "files/data/portfolio.db", sql_path: str = "src/database/init_db.sql") -> None:
      
    # locate database
    self.db_path = os.path.expanduser(db_path)
    self.connection = sqlite3.connect(os.path.expanduser(self.db_path))
    self.cur = self.connection.cursor()

    # ============================== create tables ==============================

    self.execute_sql_script(os.path.expanduser(sql_path))
    self.connection.commit()
    

  # create .sql file to create the tables
  def execute_sql_script(self, filename):
    file_open = open(filename, 'r')
    sql_file = file_open.read()
    file_open.close()
    sql_commands = sql_file.split(";")
    for command in sql_commands:
      try:
        self.cur.execute(command)
      except sqlite3.OperationalError as msg:
        print("Command skipped: ", msg)
        

  # ============================== insert ==============================

  """
  All of the following insert methods affects the all_shares table
  """

  # insert a acquire or dispose (add) transaction into transactions
  def insert_acquire_or_dispose(self, value_dic: dict[Any]):
    tolio.insert_acquire_or_dispose(self.db_path, value_dic)
        
  # insert a transfer transaction into transactions
  def insert_transfer(self, value_dic:dict[Any]) -> None:
    tolio.insert_transfer(self.db_path, value_dic)

  # insert a stock split transaction into transaction 
  def insert_stock_split(self, value_dic: dict[Any]) -> None:
    tolio.insert_stock_split(self.db_path, value_dic)
  
   

  # ============================== update tables ================================

  # update transaction age
  def update_transaction_age(self) -> None:
    age=self.cur.execute('''SELECT transaction_id, timestamp,
    CASE
      WHEN strftime('%m', date('now')) > strftime('%m', date(timestamp)) THEN strftime('%Y', date('now')) - strftime('%Y', date(timestamp))
      WHEN strftime('%m', date('now')) = strftime('%m', date(timestamp)) THEN
        CASE
          WHEN strftime('%D', date('now')) >= strftime('%D', date(timestamp)) THEN strftime('%Y', date('now')) - strftime('%Y', date(timestamp))
          ELSE strftime('%Y', date('now')) - strftime('%Y', date(timestamp)) - 1
        END
    WHEN strftime('%m', date('now')) < strftime('%m', date(timestamp)) THEN strftime('%Y', date('now')) - strftime('%Y', date(timestamp)) - 1
    END AS 'age' FROM transactions''')
    age=self.cur.fetchall()
    for id, _, aage in age:
      self.cur.execute("UPDATE transactions SET age_transaction=? WHERE transaction_id=?;", (aage, id))

      # add the stocks that are long
      self.cur.execute("UPDATE transactions SET long=(SELECT amount FROM Transactions WHERE age_transaction > 0 and transaction_abbreviation='A') WHERE transaction_id=? AND transaction_abbreviation='A' AND age_transaction > 0;", (id,))

    # make sure negative age is gone
    self.cur.execute("UPDATE transactions SET age_transaction=0 WHERE age_transaction < 0;")

    self.connection.commit()


  # update securities - this dependent on the all_shares table
  def update_securities(self) -> None:
      # create list of securities
      get_securities=self.cur.execute("SELECT DISTINCT security_id FROM transactions WHERE transaction_abbreviation IS NOT 'SS';").fetchall()
      
      for security_id in get_securities:
        security_id = security_id[0]
        age=self.cur.execute("SELECT SUM(amount) FROM all_shares WHERE security_id=? AND age_transaction >= 1 AND long_counter = '+';", (security_id,)).fetchall()[0]
        self.cur.execute("UPDATE securities SET number_long=? WHERE security_id=?;", (age[0], security_id))
        
        amount=self.cur.execute("SELECT SUM(amount), SUM(price_USD), (SUM(price_USD)/SUM(amount)), (SELECT SUM(amount) FROM transactions WHERE transaction_abbreviation='D') FROM all_shares WHERE security_id=? AND long_counter = '+';", (security_id,)).fetchall()[0]
        
        (sum_amount, sum_price, cost_basis, amount_disposed) = amount

        get_data_2=self.cur.execute("SELECT (SELECT SUM(amount) FROM all_shares WHERE long_counter='+' AND age_transaction > 0 AND security_id=?), SUM(sold_price) FROM all_shares WHERE security_id=?;", (security_id, security_id)).fetchall()[0]
      
        (_, total_price_sold) = get_data_2
        
        if amount_disposed == None or amount_disposed == 0 or total_price_sold == None:
            average_price_sold = 0
        else:
            average_price_sold = round(float(total_price_sold) / abs(amount_disposed),3)
        
        try:
            total_price_sold = round(total_price_sold, 2)
        except:
            total_price_sold = 0

        self.cur.execute("UPDATE securities SET amount_held=?, total_cost=?, cost_basis=?, total_price_sold=?, average_price_sold=? WHERE security_id=?;", 
        (sum_amount, round(sum_price, 3), round(cost_basis, 3), total_price_sold, average_price_sold, security_id))

      self.connection.commit()

  # update institutions held: institution_id, security_id, amount_held, total_cost, cost_basis, number_long
  def update_institutions_held(self) -> None:
    get_institution_id=self.cur.execute(f"SELECT DISTINCT institution_id, security_id FROM Transactions").fetchall()
    for institution_id, security_id in get_institution_id:
      
      self.cur.execute("INSERT OR IGNORE INTO institutions_held (institution_id, security_id) VALUES (?,?);", (institution_id, security_id))
      get_data=self.cur.execute("""SELECT SUM(amount), SUM(price_USD), (SUM(price_USD)/(SUM(amount))), (SELECT SUM(amount) FROM transactions WHERE transaction_abbreviation='D')
      FROM All_shares WHERE institution_id=? AND security_id=? AND long_counter ='+';""", (institution_id, security_id)).fetchall()[0]
      
      (amount_held, total_cost, cost_basis, amount_disposed)=get_data
      if bool(total_cost) == False:
        total_cost = 0
      if bool(cost_basis) == False:
        cost_basis = 0
      if bool(amount_disposed) == False:
        amount_disposed = 0

      place_holder = {
        "security_id": security_id,
        "institution_id": institution_id,
        "amount_held": amount_held,
        "total_cost": round(total_cost,3),
        "cost_basis": round(cost_basis,3),
        "amount_disposed": round(amount_disposed,3)
        
      }

      get_data_2=self.cur.execute("SELECT (SELECT SUM(amount) FROM all_shares WHERE long_counter='+' AND age_transaction >= 1 AND institution_id = :institution_id AND security_id= :security_id), SUM(sold_price), (SELECT SUM(amount) FROM all_shares WHERE long_counter = '-' AND institution_id = :institution_id AND security_id=:security_id) FROM all_shares WHERE institution_id = :institution_id AND security_id=:security_id;", place_holder).fetchall()
      (long, total_price_sold, total_amount_sold) = get_data_2[0]

      place_holder["long"] = long
      if bool(total_price_sold) == False:
        total_price_sold = 0
      if bool(total_amount_sold) == False:
        average_price_sold = 0
      elif bool(total_amount_sold) == True:
        average_price_sold = round(total_price_sold/total_amount_sold, 3)
      place_holder["total_price_sold"] = total_price_sold
      place_holder["average_price_sold"] = average_price_sold
      
      self.cur.execute("UPDATE institutions_held SET amount_held=:amount_held, total_cost=:total_cost, cost_basis=:cost_basis, number_long=:long, total_price_sold=:total_price_sold, average_price_sold=:average_price_sold WHERE institution_id=:institution_id AND security_id=:security_id;", place_holder)
    self.connection.commit()


  # update table from transactions table
  def update_table(self,*args: Any) -> None:
    name=args[1].capitalize()
    ticker=args[2].upper()
    institution=args[3].capitalize()


    security_id=self.cur.execute("SELECT security_id FROM securities WHERE security_ticker = ? AND security_name = ?;", (ticker, name)).fetchone()[0]
    institution_id=self.cur.execute("SELECT institution_id FROM institutions WHERE institution_name=?;", (institution,)).fetchone()[0]

    self.cur.execute("""UPDATE transactions SET security_id = :sec_id, institution_id = :institution_id,
    timestamp = :timestamp, transaction_abbreviation = :trans_abb, amount = :amount,
    price_USD = :price, transfer_from = :trans_from ,transfer_to = :trans_to WHERE transaction_id = :trans_id
    """,{
    "sec_id": security_id,
    "institution_id": institution_id,
    "timestamp": args[4],
    "trans_abb": args[5],
    "amount": args[9],
    "price": args[8],
    "trans_from": args[6],
    "trans_to": args[7],
    "trans_id": args[0]

    })
    self.connection.commit()
    self.refresh_individual_shares()


  # ================================= get =================================

  def get_all_shares(self) -> None:
    return self.cur.execute("SELECT * FROM all_shares;").fetchall()

  # get stock_split_history for tree view
  def get_stock_split_history(self) -> None:
    split_history_list = self.cur.execute("""SELECT ss.security_id, s.security_name, s.security_ticker, ss.split_amount, ss.timestamp FROM stock_split_history AS ss
    INNER JOIN securities AS s ON ss.security_id=s.security_id;
    
    """).fetchall()
  
    return split_history_list
      

  # get transactions table for tree view
  def get_transactions_table(self) -> List[str]:
    return self.cur.execute("""SELECT
      t.transaction_id, s.security_name, s.security_ticker, i.institution_name, t.timestamp,
      tn.transaction_type, t.transfer_from, t.transfer_to, t.price_USD, t.amount,
      t.age_transaction, t.long
      FROM institutions as i INNER JOIN transactions AS t ON i.institution_id=t.institution_id
      INNER JOIN transaction_names AS tn ON t.transaction_abbreviation=tn.transaction_abbreviation
      INNER JOIN securities AS s USING(security_id)""").fetchall()


  # get institutions_held table for treeview
  def get_institutions_held_table(self) -> List[str]:
    return self.cur.execute("""
      SELECT i.institution_name, s.security_name, ih.amount_held, ih.total_cost, ih.cost_basis,
      ih.number_long, ih.total_price_sold, ih.average_price_sold
      FROM securities as s INNER JOIN institutions_held AS ih ON s.security_id=ih.security_id
      INNER JOIN institutions AS i USING(institution_id)
      """).fetchall()


  # get the securities table for treeview
  def get_security_table(self) -> List[str]:
    return self.cur.execute("""
      SELECT security_name, security_ticker, amount_held, total_cost, cost_basis, number_long, total_price_sold, average_price_sold
      FROM securities;
      """).fetchall()
      

  # get list of x that exists
  def get_table_value(self,value:str) -> List[str]:
    edited_array = []
    if value == "security_name":
      unedited_list = self.cur.execute("SELECT DISTINCT security_name FROM securities;").fetchall()
    elif value == "security_ticker":
      unedited_list = self.cur.execute("SELECT DISTINCT security_ticker FROM securities;").fetchall()
    elif value == "institution":
      unedited_list = self.cur.execute("SELECT DISTINCT institution_name FROM institutions;").fetchall()
    else:
      unedited_list = []
  
    if len(unedited_list) == 0:
      return [""]
    elif len(unedited_list) > 0:
      for i in unedited_list:
        edited_array.append(i[0])
      return edited_array


  # get institution_id | institution_name or security_id | security_name and security_ticker
  def get_specific_value(self, institution_id: int = None, institution_name: str = None, security_id: int = None, security_name: str = None, security_ticker: str = None) -> Any:
    if bool(institution_name) == True:
      return int(self.cur.execute("SELECT institution_id FROM institutions WHERE institution_name =?;",(institution_name,)).fetchone()[0])
    elif bool(institution_id):
      return self.cur.execute("SELECT institution_name FROM institutions WHERE institution_id =?;",(int(institution_id),)).fetchone()[0]
    elif bool(security_id) == True:
      return self.cur.execute("SELECT security_name, security_ticker FROM securities WHERE security_id =?;",(int(security_id),)).fetchone()
    elif bool(security_name) == True and bool(security_ticker) == True:
      return self.cur.execute("SELECT security_id FROM securities WHERE security_name = ? AND security_ticker = ?;", (security_name, security_ticker)).fetchone()[0]
    

  # get most recent transaction
  def get_most_recent_transaction(self):
    return self.cur.execute("SELECT transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long FROM transactions WHERE transaction_id = (SELECT MAX(transaction_id) FROM transactions);").fetchone()


  # ============================== delete ==============================

  # delete transaction row
  def delete_row(self,id:int) -> None:
    self.cur.execute(f"DELETE FROM transactions WHERE transaction_id=?;", (id,))
    self.connection.commit()
    self.refresh_individual_shares()


  # delete all transactions records
  def delete_all_data(self) -> None:
    self.cur.execute("DELETE TABLE transactions;")
    self.connection.commit()



  

  # ============================== Refresh individual shares ==============================

  def refresh_individual_shares(self) -> None:
    pass
  

    



        



# test
if __name__ =="__main__":
  data = Database()
  data.refresh_individual_shares()
  data.update_transaction_age()
  data.update_securities()
  data.update_institutions_held()
  data.update_split_all_shares()
  

    
