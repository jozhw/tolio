
import json
import re
import sys, os
from typing import Dict, Any, List, Tuple

from tkinter import *
from tkinter import messagebox

import customtkinter

from database_module import Database


class GuiFunction:

    # ================================= General functionalities =================================

    # get the path of the resource
    def resource_path(self, relative_path: str) -> str:
        # for pyinstaller
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    # refresh the interal database every time the button associated with this function is clicked
    def refresh_database(self) -> None:
        Database().update_transaction_age()
        Database().update_securities()
        Database().update_institutions_held()
        

    # edit the variables so that the format of security_name, security_ticker, and institution_name is standardized
    def edit_entry_dic(self, entry_dic: List[Tuple[Any]], transfer = False) -> List[Tuple[Any]]:
        try:
            entry_dic["name"] = re.sub(r"[a-zA-z]+\s*", self.convert_case, entry_dic["name"].get())
            entry_dic["ticker"] = str(entry_dic["ticker"].get()).upper()
            entry_dic["institution_name"] = re.sub(r"[a-zA-z]+\s*", self.convert_case, entry_dic["institution_name"].get())
        except:
            entry_dic["name"] = re.sub(r"[a-zA-z]+\s*", self.convert_case, entry_dic["name"])
            entry_dic["ticker"] = str(entry_dic["ticker"].get()).upper()
            entry_dic["institution_name"] = re.sub(r"[a-zA-z]+\s*", self.convert_case, entry_dic["institution_name"].get())
        if transfer == True:
            entry_dic["to_institution_name"] = re.sub(r"[a-zA-z]+\s*", self.convert_case, entry_dic["to_institution_name"].get())
            return entry_dic
        return entry_dic
    
    def convert_case(self, match_obj: Any) -> str:
        if match_obj.group() is not None:
            return match_obj.group().capitalize()


    # ================================= get or save previous settings ================================= 

    # get the previous setting before exiting the program 
    def get_previous_setting(self, json_path: str, transition_menu: bool = False, appearance_option: bool = False) -> str:
        
        with open(json_path) as f:
            data = json.load(f)
        if transition_menu == True:
            return data["transitionMenu"]
        elif appearance_option == True:
            return data["appearanceOption"]
    
    # save the previous setting before exiting the program
    def save_previous_setting(self, json_path: str, transition_menu: str, appearance_option: str) -> None:

        with open(json_path, "r") as f:
            data = json.load(f)
        data["transitionMenu"] = transition_menu
        data["appearanceOption"] = appearance_option
        with open(json_path, "w") as f:
            json.dump(data, f, indent= 2)
        

    # ================================= insert _ into database functionalities =================================

    # create entries and save the list as a dictionary and insert the transaction
    def insert_transaction_into_database(self,entry_dic: Dict[str, Any], transfer: bool=False, split: bool=False) -> None:

        if split == False:
            inital_ask = messagebox.askyesno(title="Insert Transaction?", message="Would you like to insert this transaction into the database?")
            if inital_ask == 1:
                if self.check_correct_values(entry_dic, transfer) == True:
                    final_ask = messagebox.askokcancel(title="Please Check", message="Please verify the information is correct. Press OK to finalize submission.")

                    # the response will be either True or False
                    if final_ask == True:
                        self.modify_insert_transaction_into_database(entry_dic)
                        messagebox.showinfo("Submission Success","Your transaction was submitted.")
                    else:
                        messagebox.showinfo("Submission Canceled","Submission was canceled.")
                else:
                    messagebox.showinfo("Submission Error","There is an error with the current submission.")
            else:
                messagebox.showinfo("Submission Canceled","Submission was canceled.")
        else:
            inital_ask = messagebox.askyesno(title="Insert Transaction?", message="Would you like to insert this transaction into the database?")
            if inital_ask == 1:
            
                final_ask = messagebox.askokcancel(title="Please Check", message="Please verify the information is correct. Press OK to finalize submission.")
                if final_ask == True:
                    ask_confirm = messagebox.askokcancel(title="Please Confirm", message="The stock split cannot be redone. Are you sure you would like to continue?")
                    if ask_confirm == True:
                        # no  need to add get for entry_dic["name"], entry_dic["ticker"], entry_dic["institution_name"]
                        security_id = Database().get_security_id(entry_dic["name"], entry_dic["ticker"])
                        Database().stock_split(security_id, entry_dic["name"], entry_dic["ticker"], entry_dic["amount"].get(), entry_dic["timestamp"].get())
                        entry_dic["amount"].delete(0,END)
                        entry_dic["timestamp"].delete(0,END)
                        messagebox.showinfo("Split Submitted","Your shares have been splitted.")
                    else:
                        messagebox.showinfo("Submission Canceled","Submission was canceled.")

                else:
                    messagebox.showinfo("Submission Canceled","Submission was canceled.")
            
            else:
                messagebox.showinfo("Submission Canceled","Submission was canceled.")
             
    # have to check if security or institution exits and insert seperately
    def modify_insert_transaction_into_database(self, entry_dic: Dict[str, Any]) -> None:
        
        # convert the acquire to abbreviation
        if entry_dic["transaction_type"].get() == "Acquire":
            transaction_abbreviation = "A"
        elif entry_dic["transaction_type"].get() == "Dispose":
            transaction_abbreviation = "D"
        elif entry_dic["transaction_type"].get() == "Transfer":
            transaction_abbreviation = "T"
        else:
            raise ValueError("Incorrect transaction_type.")
        
        # convert shares depending on acquire or dispose
        if transaction_abbreviation != "T":
            amount, price = self.change_value_sign(transaction_abbreviation, entry_dic["amount"].get(), entry_dic["price_USD"].get())
        else:
            amount, price = self.change_value_sign(transaction_abbreviation, entry_dic["amount"].get(), entry_dic["price_USD"].get())
        

        # check if new security and institution

        if bool(Database().check_security(entry_dic["name"], entry_dic["ticker"])) == True:
            pass
        else:
            # insert new security
            Database().insert_security(entry_dic["name"], entry_dic["ticker"])
            
        if bool(Database().check_institution(entry_dic["institution_name"])) == True:
             pass
        else:
            # insert new institution
            Database().insert_institution(entry_dic["institution_name"])
        
        # get security_id and institution_id and convert customtkinter obj to str
        security_id = Database().get_specific_value(security_name=entry_dic["name"], security_ticker=entry_dic["ticker"])
        institution_id = Database().get_specific_value(institution_name=entry_dic["institution_name"])
        timestamp = str(entry_dic["timestamp"].get())
        
    
        # no  need to add get for entry_dic["name"], entry_dic["ticker"], entry_dic["institution_name"]
        if transaction_abbreviation == "A" or transaction_abbreviation == "D":
            if transaction_abbreviation == "A":
                Database().insert_transaction(security_id, timestamp, transaction_abbreviation, amount, price, institution_id=institution_id)
                transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long = Database().get_most_recent_transaction()
                Database().insert_all_shares(transaction_id, security_id, institution_id, timestamp, amount, price_USD, age_transaction)
            elif transaction_abbreviation == "D":
                Database().insert_transaction(security_id, timestamp, transaction_abbreviation, amount, price, institution_id=institution_id)
                transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long = Database().get_most_recent_transaction()
                Database().dispose_all_shares(security_id, institution_id, amount, price_USD, timestamp)

            entry_dic["amount"].delete(0,END)
            entry_dic["timestamp"].delete(0,END)
            entry_dic["price_USD"].delete(0,END)

        elif transaction_abbreviation == "T":
            to_institution = str(entry_dic["to_institution_name"].get())
            Database().insert_transaction(security_id, timestamp, transaction_abbreviation, amount, price, institution_id = institution_id, transfer_to = to_institution)
            transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD, transfer_from, transfer_to, age_transaction, long = Database().get_most_recent_transaction()

            entry_dic["timestamp"].delete(0,END)
            entry_dic["amount"].delete(0,END)
    

    # verify if the date and time syntax is correct
    def check_correct_values(self, entry_dic: Dict[str, Any], transfer: bool = False) -> bool:
        success = True
        # check timestamp // try/except for unittest
        try:
            timestamp = entry_dic['timestamp'].get()
        except:
            timestamp = entry_dic['timestamp']

        date_regex=re.compile('\d\d\d\d-\d\d-\d\d')



        if len(timestamp) == 0:
            pass
        elif bool(date_regex.search(timestamp)) == True:
            pass
        else:
            success=False
            messagebox.showerror("Date Error", f"Date: {timestamp} must be in \"YYYY-MM-DD\" format consisting of all numbers except for the dash.")
            raise ValueError(f"Date: {timestamp} must be in YYYY-MM-DD format consisting of all numbers except for the dash.")
            

        # check amount // try/except for unittest
        try:
            amount = entry_dic["amount"].get()
        except:
            amount = entry_dic["amount"]
        
        try:
            float(amount)
        except:
            messagebox.showerror("Amount Error", f"Amount - {amount} - should be a float or able to be converted into a float." )
            raise TypeError(f"Amount - {amount} - should be a float or able to be converted into a float.")
        

        # check price_USD // try/except for unittest
        try:
            price_USD = entry_dic["price_USD"].get()
        except:
            price_USD = entry_dic["price_USD"]
        


        try:
            float(price_USD)
        except:
            messagebox.showerror("Price Error", f"Price in USD - {price_USD} - should be a float or able to be converted into a float." )
            raise TypeError(f"Price in USD - {price_USD} - should be a float or able to be converted into a float.")

        if bool(entry_dic['name']) == False or bool(entry_dic["ticker"]) == False or bool(entry_dic["institution_name"]) == False:
            success = False
            messagebox.showerror("Name, Ticker, or Institution Error", f"""Name, ticker, or institution cannot be null. 
            \nName: {entry_dic['name']}
            \nTicker: {entry_dic["ticker"]}
            \nInstitution: {entry_dic["institution_name"]}""" )

            raise ValueError(f"""Name, ticker, or institution cannot be null. 
            \nName: {entry_dic['name']}
            \nTicker: {entry_dic["ticker"]}
            \nInstitution: {entry_dic["institution_name"]}""")
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

    # change automatically negative or positive given transaction type
    def change_value_sign(self,trans_type:str,shares:float,price:float) -> float:
        shares = float(shares)
        price = float(price)
        if trans_type =="A" and (shares < 0 or price < 0):
            if shares < 0 and price < 0:
                shares=shares*(-1)
                price=price*(-1)
                return shares, price
            elif shares > 0 and price < 0:
                price=price*(-1)
                return shares, price
            elif shares < 0 and price > 0:
                shares=shares*(-1)
                return shares, price
        elif trans_type=="D" and (shares > 0 or price > 0):
            if shares > 0 and price > 0:
                shares=shares*(-1)
                price=price*(-1)
                return shares, price
            elif shares < 0 and price > 0:
                price=price*(-1)
                return shares, price
            elif shares > 0 and price < 0:
                shares=shares*(-1)
                return shares, price
        else:
            return shares, price


    # ================================= stock split functionality =================================

    def stock_split(self,security_id: int, name: str, ticker: str, split_amount:int, timestamp:str) -> None:
        
        Database().insert_into_stock_split_history(security_id, name, ticker, split_amount, timestamp)
        Database().split_all_shares(security_id, name, ticker, split_amount, timestamp)
        Database().update_split_all_shares()




    