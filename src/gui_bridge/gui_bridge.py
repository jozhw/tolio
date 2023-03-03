'''gui_bridge.py - gui_bridge class that houses methods that bridge main.py and database.py'''
import re
import sys
import os
from functools import wraps
from typing import Dict, Callable
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from database import Database
from utils import StandardizeEntry


# ================================= general functionalities =================================
# get the values from the customtkinter object
def edit_entry_dic(entry_dic: Dict) -> Dict:
    '''takes entry_dic and gets the value of the customtkinter object and implements
     the standardize_entry.py regex_sub class method returns the edited object'''
    for key in entry_dic.keys():
        entry_dic[key] = entry_dic[key].get()
        edited_entry_dic = StandardizeEntry(entry_dic).regex_sub()
    return edited_entry_dic

# define wrapper to carry out all of the messages for insert
def insert_wrapper(method: Callable) -> None:
    '''takes a insert method and wraps it with the gui message interface'''
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
    '''This class serves as the bridge between main.py and database.py'''
    db = Database()

    @classmethod
    def alt__init__(cls, db_path: str):
        '''alternative init in the case of testing or other similar reasons'''
        cls.db = Database(db_path)
        return cls()

    # ================================= database inserts functionalities =================================
    @insert_wrapper
    def stock_split(self, entry_dic: Dict) -> None:
        '''implements database.py insert_stock_split class meethod and removes the values from gui'''
        # use get method to convert customtkinter obj to python obj
        edited_entry_dic = edit_entry_dic(entry_dic)
        # check correct values and modify for final insert
        if self.check_correct_values(edit_entry_dic, split=True) == False:
          raise Exception("There is/are value error(s).") 
        # final insert
        self.db.insert_stock_split(edited_entry_dic)
        # remove from gui entry_box
        entry_dic["amount"].delete(0, tk.END)
        entry_dic["timestamp"].delete(0, tk.END)

    @insert_wrapper
    def insert_transaction_into_database(self, entry_dic: Dict) -> None:
        '''edits the entry_dic values and implements database.py insert_acquire_or_dispose class method'''
        # use get method to convert customtkinter obj to python obj
        edit_entry_dic = edit_entry_dic(entry_dic)
        # check correct values and modify for final insert
        self.check_correct_values(edit_entry_dic)
        final_entry_dic = self.modify_insert_transaction_into_database(edit_entry_dic)
        # final insert
        self.db.insert_acquire_or_dispose(final_entry_dic)
        # remove from gui entry_box
        entry_dic["amount"].delete(0, tk.END)
        entry_dic["timestamp"].delete(0, tk.END)
        entry_dic["price_USD"].delete(0, tk.END)
    
    @insert_wrapper
    def transfer_security(self, entry_dic: Dict) -> None:
        '''edits the entry_dic values and implements database.py insert_transfer class method'''
        # use get method to convert customtkinter obj to python obj
        edit_entry_dic = edit_entry_dic(entry_dic)
        # check correct values and modify for final insert
        self.check_correct_values(edit_entry_dic, transfer = True)
        self.modify_insert_transaction_into_database(edit_entry_dic)
        # final insert
        self.db.insert_transfer(entry_dic)
        # remove from gui entry_dox
        entry_dic["amount"].delete(0, tk.END)
        entry_dic["timestamp"].delete(0, tk.END)
        entry_dic["to_institution_name"].delete(0, tk.END)


    # ================================= define methods for insert adjustments =================================
    # tailored inserts
    def modify_insert_transaction_into_database(self, entry_dic: Dict) -> Dict:
        # remove the customtkinter obj
        entry_dic = edit_entry_dic()
        # Standardize the entries
        return StandardizeEntry(entry_dic).return_entry_dic()

    # verify if the date and time syntax is correct
    def check_correct_values(self, entry_dic: Dict, transfer: bool = False, split: bool = False) -> bool:
        success = True
        timestamp = entry_dic["timestamp"]
        date_regex = re.compile(r'\d\d\d\d-\d\d-\d\d')

        # timestamp
        if bool(date_regex.search(timestamp)):
            pass
        else:
            success = False
            messagebox.showerror("Date Error", "Date must be in \"YYYY-MM-DD\" format consisting of all numbers except for the dash.")
            raise ValueError("Date must be in YYYY-MM-DD format consisting of all numbers except for the dash.")
        # amount
        try:
            float(entry_dic["amount"])
        except:
            messagebox.showerror("Amount Error", "Amount should be a float or able to be converted into a float." )
            raise TypeError("Amount should be a float or able to be converted into a float.")
          
        if bool(entry_dic['name']) and bool(entry_dic["ticker"]) and bool(entry_dic["institution_name"]):
            pass
        else:
            if bool(entry_dic['name']) and bool(entry_dic["ticker"]) and split:
                pass
            else:
                success = False
                messagebox.showerror("Name, Ticker, or Institution Error", "Name, ticker, or institution cannot be null.")
                raise ValueError("Name, ticker, or institution cannot be null.")

        if transfer or split:
            if transfer:
                if entry_dic["to_institution_name"] == entry_dic['institution_name']:
                    messagebox.showerror("Institution Error", "The institutions transfer from and to cannot be the same institution.")
                    success = False
                    raise ValueError("""The Institution Transfer From and Institution Transfer To cannot be the same institution.""")        
        else:
            # check price_USD
            try:
                float(entry_dic["price_USD"])
            except:
                entry_dic["price_USD"]
                messagebox.showerror("Price Error", "Price in USD should be a float or able to be converted into a float.")
                raise TypeError(f"Price in USD should be a float or able to be converted into a float.")
        return success

    # refresh the interal database every time the button associated with this function is clicked
    def refresh_database(self) -> None:
        pass