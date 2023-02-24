
import re, sys, os
from functools import wraps
from typing import Dict, Callable
from tkinter import *
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import tolio
from database import Database
from utils import StandardizeEntry


# ================================= general functionalities =================================
# get the values from the customtkinter object
def edit_entry_dic(entry_dic: Dict) -> Dict:
  for key in entry_dic.keys():
    entry_dic[key] = entry_dic[key].get()
    edited_entry_dic = StandardizeEntry(entry_dic).regex_sub()
  return edited_entry_dic

# define wrapper to carry out all of the messages for insert
def insert_wrapper(method: Callable) -> None:
  @wraps(method)
  def _impl(self, *method_args, **method_kwargs):
    inital_ask = messagebox.askyesno(title="Insert Transaction?", message="Would you like to insert this transaction into the database?")
    if inital_ask == True:
      final_ask = messagebox.askokcancel(title="Please Check", message="Please verify the information is correct. Press OK to finalize submission.")
      if final_ask == True:
        method_output = method(self, *method_args, **method_kwargs)
        messagebox.showinfo("Submission Success","Your transaction was submitted.")
        return method_output
      else:
        messagebox.showinfo("Submission Canceled","Submission was canceled.")
    else:
      messagebox.showinfo("Submission Canceled","Submission was canceled.")
  return _impl
         
class GuiBridge:
  db = Database()

  @classmethod
  def alt__init__(cls, db_path: str):
    cls.db = Database(db_path)
    return cls()

# ================================= database inserts functionalities =================================
  @insert_wrapper
  def stock_split(self, entry_dic: Dict) -> None:
    edited_entry_dic = edit_entry_dic(entry_dic)
    if self.check_correct_values(edit_entry_dic, split=True) == False:
      raise Exception("There is/are value error(s).") 

    security_id = self.db.get_specific_value(security_name = edited_entry_dic["name"], security_ticker = edited_entry_dic["ticker"])
    name = edited_entry_dic["name"]
    ticker = edited_entry_dic["ticker"]
    split_amount = edited_entry_dic["amount"]
    timestamp = edited_entry_dic["timestamp"]

    self.db.stock_split(security_id, name, ticker, split_amount, timestamp)
    entry_dic["amount"].delete(0,END)
    entry_dic["timestamp"].delete(0,END)

  @insert_wrapper
  def insert_transaction_into_database(self, entry_dic: Dict) -> None:

    edit_entry_dic = edit_entry_dic(entry_dic)
    self.check_correct_values(edit_entry_dic)
    self.modify_insert_transaction_into_database(edit_entry_dic)
                    
    entry_dic["amount"].delete(0,END)
    entry_dic["timestamp"].delete(0,END)
    entry_dic["price_USD"].delete(0,END)
  
  @insert_wrapper
  def transfer_security(self, entry_dic: Dict) -> None:
    edit_entry_dic = edit_entry_dic(entry_dic)
    self.check_correct_values(edit_entry_dic, transfer = True)
    self.modify_insert_transaction_into_database(edit_entry_dic)
    entry_dic["amount"].delete(0,END)
    entry_dic["timestamp"].delete(0,END)
    entry_dic["to_institution_name"].delete(0,END)


  # ================================= define methods for insert adjustments =================================
  # tailored inserts
  def modify_insert_transaction_into_database(self, entry_dic: Dict) -> None:
    # remove the customtkinter obj
    entry_dic = edit_entry_dic()
    # Standardize the entries
    entry_dic = StandardizeEntry(entry_dic).return_entry_dic()

    # check if new security and institution
    if bool(self.db.check_security(entry_dic["name"], entry_dic["ticker"])) == False:
      # insert new security
      self.db.insert_security(entry_dic["name"], entry_dic["ticker"])
        
    if bool(self.db.check_institution(entry_dic["institution_name"])) == False:
      # insert new institution
      self.db.insert_institution(entry_dic["institution_name"])
    
    # define variables for all of the necessary arguments for methods
    security_id = self.db.get_specific_value(security_name=entry_dic["name"], security_ticker=entry_dic["ticker"])
    institution_id = self.db.get_specific_value(institution_name=entry_dic["institution_name"])
    timestamp = entry_dic["timestamp"]
    transaction_abbreviation = entry_dic["transaction_abbreviation"]
    amount = entry_dic["amount"]
    price = entry_dic["price_USD"]

    
    # no  need to add get for entry_dic["name"], entry_dic["ticker"], entry_dic["institution_name"]
    if transaction_abbreviation == "A" or transaction_abbreviation == "D":
      if transaction_abbreviation == "A":
        self.db.insert_transaction(security_id, timestamp, transaction_abbreviation, amount, price, institution_id=institution_id)
        self.db.update_transaction_age()
        transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long = Database().get_most_recent_transaction()
        self.db.insert_all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction)
      elif transaction_abbreviation == "D":
        self.db.insert_transaction(security_id, timestamp, transaction_abbreviation, amount, price, institution_id=institution_id)
        self.db.update_transaction_age()
        transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long = Database().get_most_recent_transaction()            
        self.db.dispose_all_shares(security_id, institution_id, amount, price_USD, timestamp)

    elif transaction_abbreviation == "T":
      to_institution = entry_dic["to_institution_name"]
      self.db.insert_transaction(security_id, timestamp, transaction_abbreviation, amount, price, institution_id = institution_id, transfer_to = to_institution)
      self.db.update_transaction_age()
      transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long = Database().get_most_recent_transaction()
      self.db.transfer_all_shares(transaction_id, security_id, amount, transfer_to, institution_id)
    
  # verify if the date and time syntax is correct
  def check_correct_values(self, entry_dic: Dict, transfer: bool = False, split: bool = False) -> bool:
    success = True

    timestamp = entry_dic["timestamp"]
    date_regex=re.compile('\d\d\d\d-\d\d-\d\d')

    # timestamp
    if bool(date_regex.search(timestamp)) == False:
      success=False
      messagebox.showerror("Date Error", "Date: {timestamp} must be in \"YYYY-MM-DD\" format consisting of all numbers except for the dash.".format(timestamp=timestamp))
      raise ValueError("Date: {timestamp} must be in YYYY-MM-DD format consisting of all numbers except for the dash.".format(timestamp=timestamp))
        
    # amount
    try:
      amount = float(entry_dic["amount"])
    except:
      messagebox.showerror("Amount Error", "Amount - {amount} - should be a float or able to be converted into a float.".format(amount=entry_dic["amount"]) )
      raise TypeError("Amount - {amount} - should be a float or able to be converted into a float.".format(amount=entry_dic["amount"]))
    
    if bool(entry_dic['name']) == False or bool(entry_dic["ticker"]) == False or bool(entry_dic["institution_name"]) == False:
      if bool(entry_dic['name']) == True and bool(entry_dic["ticker"]) == True and split == True:
        pass
      else:
        success = False
        messagebox.showerror("Name, Ticker, or Institution Error", f"""Name, ticker, or institution cannot be null. 
            \nName: {entry_dic['name']}
            \nTicker: {entry_dic["ticker"]}
            \nInstitution: {entry_dic["institution_name"]}""")

        raise ValueError(f"""Name, ticker, or institution cannot be null. 
            \nName: {entry_dic['name']}
            \nTicker: {entry_dic["ticker"]}
            \nInstitution: {entry_dic["institution_name"]}""")
    

    if transfer == False and split == False:
      # check price_USD
      try:
        price_USD = float(entry_dic["price_USD"])
      except:
        price_USD = entry_dic["price_USD"]
        messagebox.showerror("Price Error", "Price in USD - {price_USD} - should be a float or able to be converted into a float.".format(price_USD=price_USD) )
        raise TypeError(f"Price in USD - {price_USD} - should be a float or able to be converted into a float.".format(price_USD=price_USD))

    else:
      if transfer == True:
        if entry_dic["to_institution_name"] == entry_dic['institution_name']:
          messagebox.showerror("Institution Error", "The Institution Transfer From and Institution Transfer To cannot be the same institution.")
          success = False
          raise ValueError(f"""The Institution Transfer From and Institution Transfer To cannot be the same institution.
                \nInstitution: {entry_dic["institution_name"]}
                \nTransfer to Institution: {entry_dic["to_institution_name"]}"""
                )
  
                        
    return success

  # refresh the interal database every time the button associated with this function is clicked
  def refresh_database(self) -> None:
    self.db.update_transaction_age()
    self.db.update_securities()
    self.db.update_institutions_held()

  

  # insert_csv bridge
  def insert_csv(self, csv_path: str, db_path: str = "files/data/portfolio.db") -> None:
    tolio.insert_csv_to_db(db_path, csv_path)

  






    