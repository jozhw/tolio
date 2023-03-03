from tkinter import messagebox
from typing import Callable
import tkinter as tk
import customtkinter

class Records(customtkinter.CTkFrame):

    def __init__(self, master, my_tree):
        super().__init__(master)
        self.master = master
        self.my_tree = my_tree

    def select_record(self, event, entry_dic: dict, *args: list) -> None:
        '''class method to bind record for treeview entry boxes'''
        # change to normal state in case of later bind
        for entry in entry_dic.values():
            entry.configure(state="normal")
            entry.delete(0,tk.END)
        # grab records
        selected = self.my_tree.focus()
        # grab record value
        values = self.my_tree.item(selected,'values')
        count = 0

        # insert into entry box
        for name,entry in entry_dic.items():
            if name == "id_entry" or name == "age_entry" or name == "long_entry" or name == "history_id":
                entry.insert(count, values[count])
                entry.configure(state="disabled")
                count += 1
            else:
                entry.insert(count, values[count])
                count += 1

    def remove_all(self) -> None:
        '''class method to remove records from treeview'''
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)

    def delete_record(self, entry_dic: dict) -> None:
        '''class method to remove selected record from the database'''
        to_delete = messagebox.askyesno("Delete Record", "Are you sure you would like to delete this record?")
        if to_delete == 1:
            self.my_tree.focus()
            id_entry = entry_dic["id_entry"]
            id_entry.configure(state="normal")
            id_value = id_entry.get()
            x = self.my_tree.selection()[0]
            self.my_tree.delete(x)
            id_entry.delete(0, tk.END)
            entry_dic["n_entry"].delete(0, tk.END)
            entry_dic["ticker_entry"].delete(0, tk.END)
            entry_dic["institution_entry"].delete(0, tk.END)
            entry_dic["date_entry"].delete(0, tk.END)
            entry_dic["type_entry"].delete(0, tk.END)
            entry_dic["from_entry"].delete(0, tk.END)
            entry_dic["to_entry"].delete(0, tk.END)
            entry_dic["price_entry"].delete(0, tk.END)
            entry_dic["amount_entry"].delete(0, tk.END)
            entry_dic["age_entry"].delete(0, tk.END)
            entry_dic["long_entry"].delete(0, tk.END)

            self.master.db.delete_row(id_value)
            messagebox.showinfo("Deleted!", "Your record has been deleted.")
        else:
            messagebox.showinfo("Not Deleted.", "Your record was not deleted.")


    def delete_all_data(self):
        '''class method to delete all data in database'''
        answer = messagebox.askyesno(title="Delete All Records",
                                  message="""Would you like to delete all of your records?
                                  """)
        if answer == True:
            answer_2 = messagebox.askyesno(title="Delete All Records",
                                      message="This action cannot be undone. Would you still like to continue?")
            if answer_2 == True:
                messagebox.showinfo(title="All Records Deleted", message="All your records have been deleted.")
                self.master.db.delete_all_data()
                self.remove_all()
            else:
                messagebox.showinfo(title="Records Not Deleted", message="Your records were not deleted.")
        else:
            messagebox.showinfo(title="Records Not Deleted", message="Your records were not deleted.")



    def update_record(self, entry_dic: dict) -> None:
        '''class method to update selected record on the database'''
        selected = self.my_tree.focus()

        id_entry = entry_dic["id_entry"]
        id_entry.configure(state="normal")
        transaction_id = id_entry.get()
        security_name = entry_dic["n_entry"].get()
        security_ticker = entry_dic["ticker_entry"].get()
        institution_name = entry_dic["institution_entry"].get()
        timestamp = entry_dic["date_entry"].get()

        # not transaction_abbreviation
        transaction_type = entry_dic["type_entry"].get()
        transfer_from = entry_dic["from_entry"].get()
        transfer_to = entry_dic["to_entry"].get()
        price_usd = entry_dic["price_entry"].get()
        amount = entry_dic["amount_entry"].get()
        age_transaction=entry_dic["age_entry"].get()
        long = entry_dic["long_entry"].get()

        # define a dictionary to contain all of the values for the rust method
        value_dic = {
          "transaction_id": transaction_id,
          "security_name": security_name,
          "security_ticker": security_ticker,
          "institution_name": institution_name,
          "timestamp": timestamp,
          "transaction_type": transaction_type,
          "transfer_from": transfer_from,
          "transfer_to": transfer_to,
          "price_usd": price_usd,
          "amount": amount,
          "age_transaction": age_transaction,
          "long": long
        }

        self.my_tree.item(selected,text="",values=(
        transaction_id,
        security_name,
        security_ticker,
        institution_name,
        timestamp,
        transaction_type,
        transfer_from,
        transfer_to,
        price_usd,
        amount,
        age_transaction,
        long
        ))

        id_entry.delete(0, tk.END)
        entry_dic["n_entry"].delete(0, tk.END)
        entry_dic["ticker_entry"].delete(0, tk.END)
        entry_dic["institution_entry"].delete(0, tk.END)
        entry_dic["date_entry"].delete(0, tk.END)
        entry_dic["type_entry"].delete(0, tk.END)
        entry_dic["from_entry"].delete(0, tk.END)
        entry_dic["to_entry"].delete(0, tk.END)
        entry_dic["price_entry"].delete(0, tk.END)
        entry_dic["amount_entry"].delete(0, tk.END)
        entry_dic["age_entry"].delete(0, tk.END)
        entry_dic["long_entry"].delete(0, tk.END)

        to_update = messagebox.askyesno("Update Record", "Are you sure you would like to update this record?")
        if to_update == 1:
            self.master.db.update_table(value_dic)
            messagebox.showinfo("Data Updated", "Your transaction has been updated.")
        else:
            messagebox.showinfo("Not Updated.", "Your record was not updated.")

    def query_database(self, func: Callable) -> None:
        '''wraper function to standardize input data from database'''
        count = 0
        records=func()
        for record in records:
            rec=[record[i] for i in range(len(record))]
            rec=tuple(rec)

            if count % 2 == 0:
                self.my_tree.insert(parent='',index='end',text="",values=rec,tags=('evenrow',))
            else:
                self.my_tree.insert(parent='',index='end',text="",values=rec,tags=('oddrow',))
            count += 1