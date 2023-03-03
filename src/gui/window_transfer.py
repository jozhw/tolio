import tkinter as tk

import customtkinter

class WindowTransfer(customtkinter.CTk):
    '''class to create new window for transfer transactions'''
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.transfer_window = customtkinter.CTkToplevel(self.master)
        self.transfer_window.title("Transfer Institution")

        width = 1000
        height = 500
        self.transfer_window.geometry(f"{width}x{height}")
        self.transfer_window.minsize(width,height)
        self.transfer_window.maxsize(width,height)

        self.transfer_window.grid_rowconfigure(0, weight=1)
        window = customtkinter.CTkFrame(master=self.transfer_window, width=960, height=460)
        window.grid(row=0,column=0, padx=20, pady=20)

        self.window_widgets()

    def window_widgets(self):
        '''class method for all transfer window widgets'''
        # create title
        title = customtkinter.CTkLabel(self.transfer_window, text="Transfer Institution Entry", corner_radius=10)
        title.configure(font = ("Arial Bold", 17))
        title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        # labels: name, ticker, institution_name, time of transaction, amount, price_usd
        label_rely = 0.1
        labels = ["Name of Security", "Ticker", "From Institution Name", "Time of Transaction", "Amount of Shares", "To Institution Name", "Transaction Type"]
        for i in labels:
            my_label=customtkinter.CTkLabel(self.transfer_window, text=i , anchor=tk.W)
            my_label.configure(font=('Arial Bold',13))
            my_label.place(relx=0.01, rely=label_rely, relwidth=0.2, relheight=0.1)
            label_rely = label_rely + 0.1

        # all entries but it is in combo box style

        name_of_security_entry = customtkinter.CTkComboBox(self.transfer_window, values=self.master.db.get_table_value("name"))
        name_of_security_entry.set(value="")
        name_of_security_entry.place(relx=0.16, rely=0.125, relwidth=0.82, relheight=0.05)

        ticker_entry = customtkinter.CTkComboBox(self.transfer_window, values=self.db.get_table_value("ticker"))
        ticker_entry.set(value="")
        ticker_entry.place(relx=0.16, rely=0.225, relwidth=0.82, relheight=0.05)

        from_institution_name_entry = customtkinter.CTkComboBox(self.transfer_window, values=self.master.db.get_table_value("institution"))
        from_institution_name_entry.set(value="")
        from_institution_name_entry.place(relx=0.16, rely=0.325, relwidth=0.82, relheight=0.05)

        time_of_transaction_entry = customtkinter.CTkEntry(self.transfer_window, placeholder_text="Input in the format \"YYYY-MM-DD\" with each character being an integer or leave this field empty for current date and time.")
        time_of_transaction_entry.place(relx=0.16, rely=0.425, relwidth=0.82, relheight=0.05)

        amount_of_shares_entry = customtkinter.CTkEntry(self.transfer_window, placeholder_text="Input only a number.")
        amount_of_shares_entry.place(relx=0.16, rely=0.525, relwidth=0.82, relheight=0.05)

        to_institution_name_entry = customtkinter.CTkComboBox(self.transfer_window, values=self.master.db.get_table_value("institution"))
        to_institution_name_entry.set(value="")
        to_institution_name_entry.place(relx=0.16, rely=0.625, relwidth=0.82, relheight=0.05)

        set_transaction_type_entry = customtkinter.StringVar(value="Transfer")
        transaction_type_entry = customtkinter.CTkEntry(self.transfer_window, textvariable=set_transaction_type_entry)
        transaction_type_entry.configure(state="disabled")

        transaction_type_entry.place(relx=0.16, rely=0.725, relwidth=0.82, relheight=0.05)

        set_price_usd_entry = customtkinter.StringVar(value=0)
        price_usd_entry = customtkinter.CTkEntry(self.transfer_window, textvariable=set_price_usd_entry)


        # dictionary of entries
        entry_dic = {"name": name_of_security_entry, "ticker": ticker_entry,
            "institution_name": from_institution_name_entry, "timestamp": time_of_transaction_entry,
            "amount": amount_of_shares_entry, "to_institution_name": to_institution_name_entry,
            "transaction_type": transaction_type_entry, "price_USD": price_usd_entry
        }

        # entry button
        entry_button = customtkinter.CTkButton(self.transfer_window, text="Enter",
                                             command=lambda: self.master.gb.insert_transaction_into_database(entry_dic, transfer= True))
        entry_button.place(relx=0, rely=0.825, relwidth=1, relheight=0.05)

        # return to main menu and exit button
        return_main_button = customtkinter.CTkButton(self.transfer_window, text="Close Window", command=self.transfer_window.destroy)
        exit_button = customtkinter.CTkButton(self.transfer_window, text="Exit Program", command=self.master.on_closing)

        return_main_button.place(relx=0, rely=0.924, relwidth=0.2, relheight=0.075)
        exit_button.place(relx=0.8, rely=0.924, relwidth=0.2, relheight=0.075)