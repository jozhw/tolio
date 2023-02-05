import sqlite3, os, copy

from typing import List, Tuple, Any 

import tolio


class Database:
  def __init__(self, db_path: str = "files/data/portfolio.db", sql_path: str = "src/database/init_db.sql") -> None:
      
    # locate database
    # target_dir = "~/Applications/AppData/Local/Tolio/db"
    self.connection = sqlite3.connect(os.path.expanduser(db_path))
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
        

  def all_shares_table(self, reset: bool=False) -> None:

      # will need to change this for whenever there is an update to drop the table or else continue with the previous
      if reset == True:
          self.cur.execute("DROP TABLE all_shares;")

      self.cur.execute('''CREATE TABLE IF NOT EXISTS all_shares (individual_share_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, transaction_id INT, security_id INTEGER NOT NULL,
      institution_id INTEGER NOT NULL, timestamp DATETIME, amount REAL NOT NULL, price_USD REAL NOT NULL, sold_price REAL, age_transaction INTEGER, long_counter TEXT, date_disposed DATETIME,
      FOREIGN KEY(institution_id) REFERENCES institutions(institution_id),
      FOREIGN KEY(security_id) REFERENCES securities(security_id),
      FOREIGN KEY(timestamp) REFERENCES transactions(timestamp),
      FOREIGN KEY(transaction_id) REFERENCES transactions(transaction_id)
      );''')

      # for those who already have a database for this application, must initialize
      previous_data = self.cur.execute("SELECT long_counter FROM all_shares").fetchone()

      if bool(previous_data) is True:
          pass
      else:
          # insert in order to avoid any mishaps
          # the institution_id of the transfer is the one from which is begin transfered from
          input_data = self.cur.execute("""SELECT transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction, 
          transaction_abbreviation, transfer_from, transfer_to FROM Transactions ;""").fetchall()

          for transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction, transaction_abbreviation, transfer_from, transfer_to in input_data:
              
              if transaction_abbreviation == "A": 
                  self.insert_all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction)
              elif transaction_abbreviation == "D":              
                  self.dispose_all_shares(security_id, institution_id, amount, price_USD, timestamp)
              elif transaction_abbreviation == "T":
                  self.transfer_all_shares(transaction_id, security_id, amount, transfer_to, institution_id)
              elif transaction_abbreviation == "SS":
                  pass
                  # there are some major issues with the below - for some reason the rust extension does not work with it
                  # name, ticker = self.get_specific_value(security_id=security_id)
                  # self.stock_split(security_id, name, ticker, amount, timestamp)

              



          self.connection.commit()

          """To input the transactions, there are the requirements for the insert
          query but also the function that is used to insert the data must be able
          to indentify if a security is new or not. If so, it will be routed to another
          function that will input with the initiation process for the securities table.
          With all of the initial values except for the identifiers as 0 or null.
          For the graphic interface all of necessary inputs must be visible for the
          user to enter."""




    # ============================== updated function for number of long shares calculations ==============================

  def insert_all_shares(self,transaction_id:int, security_id:int, institution_id:int, timestamp:str, amount:float, price_USD:float, age_transaction:int) -> None:
    # incase numeric type is a string
    amount = float(amount)

    # check for fractional shares below 1 share
    if amount < 1:
      price_USD = price_USD *amount
    else:
      price_USD = price_USD / amount

    # check to see amount size
    if amount > 1:
      # control for fractional greater than 1
      remainder = amount % 1
      amount = amount - remainder
      for i in range(int(amount)):
        number = 1
        self.insert_into_all_shares(transaction_id, security_id, institution_id, timestamp, number, price_USD, age_transaction)

      if remainder > 0:
        self.insert_into_all_shares(transaction_id, security_id, institution_id, timestamp, remainder, price_USD, age_transaction)

    elif amount <= 1:
      self.insert_into_all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction)

    self.connection.commit()


  def dispose_all_shares(self,security_id:int, institution_id:int, amount:float, price_USD:float, date_disposed:str) -> None:

    # have to determine amount because of how many times to loop; however must also consider fractional
    self.the_check = self.check_if_whole_share(security_id, institution_id)
    amount = abs(amount)
    num = copy.deepcopy(amount)
    remainder = num % 1
    num = int(num - remainder)
    # check for fractional shares below 1 share
    if amount < 1:
      price_USD = abs(price_USD * amount)
    else:
      price_USD = abs(price_USD / amount)
    if amount >= 1:
      for i in range(int(num)):
        # must check if the updated is a single share or not
        if  self.the_check == 1:
          self.change_to_minus(price_USD, security_id, institution_id, date_disposed, self.the_check)
              
        else:            
          self.change_amount_share(security_id, institution_id, price_USD, date_disposed, self.the_check, 1)

      if remainder > 0:
        # new check
        new_check = self.check_if_whole_share(security_id, institution_id)
        # must get to check if it is a single share
        # check if new_check or remainder is bigger for price accuracy
        self.change_amount_share(security_id, institution_id, price_USD, date_disposed, new_check, remainder)

    else:
      self.change_amount_share(security_id, institution_id, price_USD, date_disposed, self.the_check, remainder)
  

  def transfer_all_shares(self,transaction_id: int,security_id:int, amount:int, transfer_to:str, institution_id:str) -> None:

    """Have to make sure that only whole shares can be transfered. When the transfer happens, we have to find the earliest
    whole share of that institution and convert it to said institution. Note: For the transactions table, the institution_id
    for the transfer is the institution that is doing the transfering (transfer from)"""

    transfer_to_institution_id = self.get_specific_value(institution_name = transfer_to)
    place_holder = {
      "transaction_id": transaction_id,
      "transfer_to_institution_id": transfer_to_institution_id,
      "institution_id": institution_id
    }
    for i in range(abs(int(amount))):
      self.cur.execute(""" UPDATE all_shares SET transaction_id = :transaction_id, institution_id = :transfer_to_institution_id
          WHERE security_id = :security_id AND institution_id = :institution_id AND 
          individual_share_id = (
          SELECT min(individual_share_id)
          FROM All_shares
          WHERE long_counter = '+' AND institution_id = :institution_id AND amount = 1);
          """, place_holder)
      self.connection.commit()


  # ============================== dispose shares functionalities ==============================

  # define function to check the shares to see if they are whole shares
  def check_if_whole_share(self,security_id: int, institution_id: int) -> float:

    place_holder = {"security_id": security_id, "institution_id": institution_id}

    return self.cur.execute("""
      SELECT amount FROM all_shares
      WHERE long_counter = '+' AND security_id = :security_id AND institution_id = :institution_id AND individual_share_id = (
      SELECT min(individual_share_id)
      FROM all_shares
      WHERE long_counter = '+' AND institution_id = :institution_id
      );
      """, place_holder).fetchone()[0]
      

  def check_price(self,security_id: int, institution_id: int) -> List[Tuple[float]]:

    place_holder = {"security_id": security_id, "institution_id": institution_id}

    return self.cur.execute("""
      SELECT sold_price FROM all_shares
      WHERE long_counter = '+' AND security_id = :security_id AND institution_id = :institution_id AND individual_share_id = (
      SELECT min(individual_share_id)
      FROM All_shares
      WHERE long_counter = '+' AND institution_id = :institution_id
      );
      """, place_holder).fetchone()
      

  def change_to_minus(self,price_USD: float, security_id: int, institution_id: int, dispose_date: str, number: float, remainder: float = 0) -> None:
    place_holder = {
      "price_USD": price_USD,
      "security_id": security_id,
      "institution_id": institution_id,
      "dispose_date": dispose_date,
      "number": number,
      "remainder": remainder
  }

    if  number == 1 and remainder == 0:
      self.cur.execute("""
      UPDATE all_shares
      SET long_counter = '-', sold_price = :price_USD, date_disposed= :dispose_date}
      WHERE long_counter = '+' AND security_id = :security_id AND institution_id = :institution_id AND individual_share_id = (
      SELECT min(individual_share_id)
      FROM All_shares
      WHERE long_counter = '+'
      AND institution_id = :institution_id
      );
      """, place_holder)

    elif number < 1 and number == remainder:
      previous_price = self.check_price(security_id, institution_id)
      if bool(previous_price) == True:
        place_holder["price_USD"] = previous_price[0] + price_USD
        self.cur.execute("""
        UPDATE all_shares
        SET long_counter = '-', sold_price = :price_USD, date_disposed= :dispose_date
        WHERE long_counter = '+' AND security_id = :security_id AND institution_id = :institution_id AND individual_share_id = (
        SELECT min(individual_share_id)
        FROM All_shares
        WHERE long_counter = '+'
        AND institution_id = :institution_id
        );
        """, place_holder)

      else:

        self.cur.execute("""
        UPDATE all_shares
        SET long_counter = '-', sold_price = :price_USD, date_disposed= :dispose_date
        WHERE long_counter = '+' AND security_id = '{security_id}' AND
        institution_id = :institution_id AND individual_share_id = (
        SELECT min(individual_share_id)
        FROM All_shares
        WHERE long_counter = '+'
        AND institution_id = :institution_id
        );
        """, place_holder)

    elif number > 0:

      previous_price = self.check_price(security_id, institution_id)

      if bool(previous_price) == True:
        place_holder["price_USD"] = previous_price[0] + price_USD
        self.cur.execute("""
        UPDATE all_shares
        SET sold_price = :price_USD, date_disposed= :dispose_date
        WHERE long_counter = '+' AND security_id = :security_id AND
        institution_id = :institution_id AND individual_share_id = (
        SELECT min(individual_share_id)
        FROM All_shares
        WHERE long_counter = '+'
        AND institution_id = :institution_id
        );
        """, place_holder)
      else:
        self.cur.execute("""
        UPDATE all_shares
        SET sold_price = :price_USD, date_disposed= :dispose_date
        WHERE long_counter = '+' AND security_id = :security_id AND
        institution_id = :institution_id AND individual_share_id = (
        SELECT min(individual_share_id)
        FROM All_shares
        WHERE long_counter = '+'
        AND institution_id = :institution_id
        );
        """, place_holder)
  
    self.connection.commit()


  def change_amount_share(self,security_id: int, institution_id: int, price_USD: float, date_disposed:str, number: float, remainder: float = 0, n: bool=True) -> None:
    to_add = abs(number) - abs(remainder)

    place_holder = {
      "to_add": to_add,
      "security_id": security_id,
      "institution_id": institution_id,
      "price_USD": price_USD,
      "date_disposed": date_disposed,
      }

    if n == True:

      if abs(number) > abs(remainder):
        new_price_USD = copy.deepcopy(price_USD) * abs(remainder)
      else:
        new_price_USD = copy.deepcopy(price_USD) * abs(number)
      
    if to_add == 0:

      if n == True:
        self.change_to_minus(new_price_USD, security_id, institution_id, date_disposed, self.the_check, remainder)
      else:
        self.change_to_minus(price_USD, security_id, institution_id, date_disposed, self.the_check, remainder)

    elif to_add > 0:

      self.cur.execute("""
          UPDATE all_shares
          SET amount = :to_add, date_disposed= :date_disposed
          WHERE long_counter = '+' AND security_id = :security_id AND
          institution_id = :institution_id AND individual_share_id = (
          SELECT min(individual_share_id)
          FROM all_shares
          WHERE long_counter = '+'
          AND institution_id = :institution_id
          );
          """, place_holder)

      if n == True:
        self.change_to_minus(new_price_USD, security_id, institution_id, date_disposed, to_add)
      else:
        self.change_to_minus(price_USD, security_id, institution_id, date_disposed, to_add)

      self.connection.commit()

    elif to_add < 0:

      self.cur.execute(f"""
        UPDATE all_shares
        SET amount = {0}, , date_disposed=:date_disposed
        WHERE long_counter = '+' AND security_id = :security_id AND
        institution_id = :institution_id AND individual_share_id = (
        SELECT min(individual_share_id)
        FROM all_shares
        WHERE long_counter = '+'
        AND institution_id = :institution_id
          );
          """, place_holder)

      self.connection.commit()

      if n == True:
        self.change_to_minus(new_price_USD, security_id, institution_id, date_disposed, 0)
      else:
        self.change_to_minus(price_USD, security_id, institution_id, date_disposed, 0)

      brand_new_check = self.check_if_whole_share(security_id, institution_id) 

      if abs(brand_new_check) > abs(to_add):
        self.change_amount_share(security_id, institution_id, abs(to_add) * price_USD, date_disposed, brand_new_check , to_add, n=False)
      else:
        self.change_amount_share(security_id, institution_id, abs(brand_new_check) * price_USD, date_disposed, brand_new_check , to_add, n=False)


  # ============================== determine if exists/check ==============================

  # determine if security exists
  def check_security(self,name:str, ticker:str) -> tuple:
    return self.cur.execute("SELECT * FROM securities WHERE security_name=? and security_ticker=?;", (name, ticker)).fetchone()


  # determine if institution exists
  def check_institution(self,institution_name:str) -> tuple:
    return self.cur.execute("SELECT * FROM institutions WHERE institution_name=?;", (institution_name,)).fetchone()


  # check amount of shares
  def check_shares(self,name:str, ticker:str, trans_from:str) -> tuple:
    security_id=self.cur.execute("SELECT security_id from securities WHERE security_name=? AND security_ticker=?;", (name, ticker)).fetchone()[0]
    institution_id=self.cur.execute("SELECT institution_id from institutions WHERE institution_name=?;", trans_from).fetchone()[0]
    return self.cur.execute("SELECT amount_held FROM institutions_held WHERE institution_id=? AND security_id=?;", (institution_id, security_id)).fetchone()
      

  # ============================== insert ==============================

  # define insert into all_shares function
  def insert_into_all_shares(self,transaction_id:int, security_id:int, institution_id:int, timestamp:str, amount:float, price_USD:float, age_transaction: int, sold_price: float=0) -> None:
    self.cur.execute("""
      INSERT INTO all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction, long_counter, sold_price) VALUES (?, ?, ?, ?, ?, ?, ?, "+", ?);
      """, (transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction, sold_price))
    
      

  def insert_into_stock_split_history(self, security_id: int, name: str, ticker: str, split_amount:int, timestamp:str) -> None:
    if bool(timestamp) is True:
      self.cur.execute("""
        INSERT INTO stock_split_history (security_id, security_name, ticker, split_amount, timestamp) VALUES (?,?,?,?,?);
          """, (security_id, name, ticker, split_amount, timestamp))
    else:
      self.cur.execute("""
        INSERT INTO stock_split_history (security_id, security_name, ticker, split_amount, timestamp) VALUES (?,?,?,?, datetime(CURRENT_TIMESTAMP, 'localtime') );
          """, (security_id, name, ticker, split_amount))
      

  # insert a new security in database: all is needed is name and ticker
  def insert_security(self,name:str, ticker:str) -> None:
    self.cur.execute("INSERT INTO securities (security_name, security_ticker) VALUES (?,?)", (name, ticker))
    self.connection.commit()
      

  # insert a new institution in database, all is needed is the name
  def insert_institution(self,institution_name:str) -> None:
    institution_name=institution_name.capitalize()
    self.cur.execute("INSERT INTO institutions (institution_name) VALUES (?)", (institution_name,))
    self.connection.commit()
      
      
  # insert a new transaction type
  # most likely will never use
  def insert_transaction_type(self,new_transaction_type:str, new_transaction_abb:str) -> None:
    self.cur.execute('''INSERT INTO transaction_names (transaction_type, transaction_abbreviation)
      VALUES (?,?)''', (new_transaction_type, new_transaction_abb))

    self.connection.commit()
      

  # insert a new transaction: security_id, name, ticker, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer-to
  def insert_transaction(self,security_id: int, date_time: str, trans_type:str, shares:float, price:float, institution_id: int = None, transfer_to: str = None) -> None:
    place_holder = {
      "security_id": security_id,
      "date_time": date_time,
      "trans_type": trans_type,
      "shares": shares,
      "price": price,
      "institution_id": institution_id,
      "transfer_to": transfer_to
    }

    if transfer_to != None:
      if bool(date_time) == False:
        self.cur.execute("INSERT INTO transactions (security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to) VALUES (:security_id, :institution_id, datetime(CURRENT_TIMESTAMP, 'localtime'), :trans_type, :shares, :price, :institution_id, :transfer_to);",
        place_holder)
      else:
        self.cur.execute("INSERT INTO transactions (security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to) VALUES (:security_id, :institution_id, :date_time, :trans_type, :shares, :price, :institution_id, :transfer_to);",
        place_holder)
    elif trans_type == "SS":
      if bool(date_time) == False:
        self.cur.execute("INSERT INTO transactions (security_id, timestamp, transaction_abbreviation, amount) VALUES (:security_id, datetime(CURRENT_TIMESTAMP, 'localtime'), :trans_type, :shares);", 
        place_holder)
      else:
        self.cur.execute("INSERT INTO transactions (security_id, timestamp, transaction_abbreviation, amount) VALUES (:security_id, :date_time, :trans_type, :shares);",
        place_holder)
    else:
      if bool(date_time) == False:
        self.cur.execute("INSERT INTO transactions (security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD) VALUES (:security_id, :institution_id, datetime(CURRENT_TIMESTAMP, 'localtime'), :trans_type, :shares, :price);",
        place_holder)
      else:
        self.cur.execute("INSERT INTO transactions (security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD) VALUES (:security_id, :institution_id, :date_time, :trans_type, :shares, :price);",
        place_holder)
      
    self.connection.commit()


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


  # update securities
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



  # ==============================  stock split ============================== 

  # stock split
  def stock_split(self,security_id: int, name: str, ticker: str, split_amount:int, timestamp:str, target_dir:str = "src/portfolio.db") -> None:

    self.insert_into_stock_split_history(security_id, name, ticker, split_amount, timestamp)
    self.insert_transaction(security_id, timestamp, "SS", split_amount, None)
    self.split_all_shares(security_id, split_amount, timestamp)
    self.update_split_all_shares(target_dir)


  # stock split functionalities
  
  def split_all_shares(self,security_id: int, split_amount:int, timestamp:str) -> None:
    place_holder = {
      "split_amount": split_amount,
      "timestamp": timestamp,
      "security_id": security_id
    }

    self.cur.execute("""
    UPDATE all_shares SET amount=amount*:split_amount WHERE long_counter = '+' AND security_id = :security_id
    AND (timestamp IS NULL OR timestamp > :timestamp);
    """, place_holder
  )
    self.connection.commit()
  

  # insert from all_shares into all_shares_split and back to all_shares and delete all_shares_split
  def update_split_all_shares(self, target_dir) -> None:
    tolio.insert_into_all_shares(target_dir)

  # divide the data into 10000 chunks of rows
  def chunk_data_insert(self, data: List[Tuple[Any]], rows: int=10000) -> List[Tuple[Any]]:
    for i in range(0, len(data), rows):
      yield data[i:i+rows]

  # ============================== Refresh individual shares ==============================

  def refresh_individual_shares(self) -> None:
    self.all_shares_table(reset=True)
    



        



# test
if __name__ =="__main__":
  data = Database()
  data.refresh_individual_shares()
  data.update_transaction_age()
  data.update_securities()
  data.update_institutions_held()
  data.update_split_all_shares()
  

    
