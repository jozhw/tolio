
import tkinter as tk
import customtkinter

class WindowAddTransaction(customtkinter.CTkFrame):
    '''class that opens a new window to input a transaction for acquiring or disposing a security'''

    def __init__(self, master):
        '''to initiate takes master (the main tkinter)'''
        super().__init__(master)
        self.master = master
        self.transaction_window = customtkinter.CTkToplevel(self.master)
        self.transaction_window.title("Add Transaction")

        width = 1000
        height = 500

        self.transaction_window.geometry(f"{width}x{height}")
        self.transaction_window.minsize(width, height)
        self.transaction_window.maxsize(width, height)
        self.transaction_window.grid_rowconfigure(0, weight=1)
        self.master = master

        self.window_widgets()

    def window_widgets(self):

        # create title
        title = customtkinter.CTkLabel(self.transaction_window,
                                       text="Transaction Entry",
                                       corner_radius=10)
        title.configure(font=("Arial Bold", 17))
        title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        # labels: name, ticker, institution_name, time of transaction, amount, price_USD
        label_rely = 0.1
        labels = ["Name of Security", "Ticker", "Institution Name",
                    "Time of Transaction", "Amount of Shares", "Price in USD",
                    "Transaction Type"]
        for i in labels:
            my_label = customtkinter.CTkLabel(self.transaction_window, text=i, anchor=tk.W)
            my_label.configure(font=('Arial Bold',13))
            my_label.place(relx=0.01, rely=label_rely, relwidth=0.2, relheight=0.1)
            label_rely = label_rely + 0.1

        # all entries but it is in combo box style
        name_of_security_entry = customtkinter.CTkComboBox(self.transaction_window,
                                                           values=self.master.db.get_table_value("security_name"))
        name_of_security_entry.set(value="")
        name_of_security_entry.place(relx=0.16, rely=0.125, relwidth=0.82, relheight=0.05)

        ticker_entry = customtkinter.CTkComboBox(self.transaction_window,
                                                 values=self.master.db.get_table_value("security_ticker"))
        ticker_entry.set(value="")
        ticker_entry.place(relx=0.16, rely=0.225, relwidth=0.82, relheight=0.05)

        institution_name_entry = customtkinter.CTkComboBox(self.transaction_window,
                                                           values=self.master.db.get_table_value("institution"))
        institution_name_entry.set(value="")
        institution_name_entry.place(relx=0.16, rely=0.325, relwidth=0.82, relheight=0.05)

        tot_text = "Input in the format \"YYYY-MM-DD\" or leave this field empty."
        time_of_transaction_entry = customtkinter.CTkEntry(self.transaction_window,
                                                           placeholder_text=tot_text)
        time_of_transaction_entry.place(relx=0.16, rely=0.425, relwidth=0.82, relheight=0.05)

        amount_of_shares_entry = customtkinter.CTkEntry(self.transaction_window,
                                                        placeholder_text="Input only a number.")
        amount_of_shares_entry.place(relx=0.16, rely=0.525, relwidth=0.82, relheight=0.05)

        price_usd_entry = customtkinter.CTkEntry(self.transaction_window,
                                                 placeholder_text="Input only a number. Do not input the currency.")
        price_usd_entry.place(relx=0.16, rely=0.625, relwidth=0.82, relheight=0.05)

        transaction_type_entry = customtkinter.CTkOptionMenu(self.transaction_window,
                                                             values =["Acquire", "Dispose"],
                                                             fg_color =("#F9F9FA", "#343638"),
        button_color = ("#979DA2", "#565B5E"),
        button_hover_color = ("#6E7174", "#7A848D"))
        transaction_type_entry.set(value="Acquire")
        transaction_type_entry.place(relx=0.16, rely=0.725, relwidth=0.82, relheight=0.05)

        # dictionary of entries
        entry_dic = {"name": name_of_security_entry, "ticker": ticker_entry,
            "institution_name": institution_name_entry, "timestamp": time_of_transaction_entry,
            "amount": amount_of_shares_entry, "price_USD": price_usd_entry,
            "transaction_type": transaction_type_entry
        }

        # entry button
        entry_button = customtkinter.CTkButton(self.transaction_window,
                                               text="Enter",
                                               command=lambda: self.master.gb.insert_transaction_into_database(entry_dic))
        entry_button.place(relx=0, rely=0.825, relwidth=1, relheight=0.05)

        # return to main menu and exit button
        return_main_button = customtkinter.CTkButton(self.transaction_window,
                                                     text="Close Window",
                                                     command=self.transaction_window.destroy)
        exit_button=customtkinter.CTkButton(self.transaction_window,
                                            text="Exit Program",
                                            command=self.master.on_closing)

        return_main_button.place(relx=0, rely=0.924, relwidth=0.2, relheight=0.075)
        exit_button.place(relx=0.8, rely=0.924, relwidth=0.2, relheight=0.075)