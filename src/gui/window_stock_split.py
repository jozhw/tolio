import tkinter as tk

import customtkinter

class WindowStockSplit(customtkinter.CTkFrame):
    '''class for openning a stock split transaction window'''
    def __init__(self, master):
        super().__init__(master)
        self.master =  master
        self.ss_window = customtkinter.CTkToplevel(self.master)
        self.ss_window.title("Stock Split")

        width = 750
        height = 400

        self.ss_window.geometry(f"{width}x{height}")
        self.ss_window.minsize(width, height)
        self.ss_window.maxsize(width, height)

        self.ss_window.grid_rowconfigure(0, weight=1)
        window = customtkinter.CTkFrame(master=self.ss_window, width=720, height=360)
        window.grid(row=0,column=0, padx=15, pady=15)

        self.window_widgets()

    def window_widgets(self):
        # create title
        title = customtkinter.CTkLabel(self.ss_window,text="Stock Split Adjustment", corner_radius=10)
        title.configure(font=("Arial Bold", 17))
        title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        # labels: name, ticker, institution_name, time of transaction, amount, price_USD
        label_rely = 0.1
        labels=["Name of Security", "Ticker", "Time of Split", "Split Amount", "Transaction Type"]
        for i in labels:
            my_label=customtkinter.CTkLabel(self.ss_window, text=i, anchor=tk.W)
            my_label.configure(font=('Arial Bold', 13))
            my_label.place(relx=0.01, rely=label_rely, relwidth=0.2, relheight=0.175)
            label_rely = label_rely + 0.13

        # all entries but it is in combo box style

        name_of_security_entry = customtkinter.CTkOptionMenu(self.ss_window,
                                                             values=self.master.db.get_table_value("security_name"),
                                                             fg_color=("#F9F9FA", "#343638"),
                                                             button_color=("#979DA2", "#565B5E"),
                                                             button_hover_color=("#6E7174", "#7A848D"))

        name_of_security_entry.set(value="")
        name_of_security_entry.place(relx=0.18, rely=0.155, relwidth=0.8, relheight=0.07)

        ticker_entry = customtkinter.CTkOptionMenu(self.ss_window,
                                                   values=self.master.db.get_table_value("security_ticker"),
                                                   fg_color=("#F9F9FA", "#343638"),
                                                   button_color=("#979DA2", "#565B5E"),
                                                   button_hover_color=("#6E7174", "#7A848D"))

        ticker_entry.set(value="")
        ticker_entry.place(relx=0.18, rely=0.285, relwidth=0.8, relheight=0.07)

        time_of_transaction_entry = customtkinter.CTkEntry(self.ss_window,
                                                           placeholder_text="Leave empty or input in the format \"YYYY-MM-DD\".")
        time_of_transaction_entry.place(relx=0.18, rely=0.415, relwidth=0.8, relheight=0.07)

        amount_of_shares_entry = customtkinter.CTkEntry(self.ss_window,
                                                        placeholder_text="Input only a whole number.")
        amount_of_shares_entry.place(relx=0.18, rely=0.545, relwidth=0.8, relheight=0.07)

        set_transaction_type_entry = customtkinter.StringVar(value="Stock Split")
        transaction_type_entry = customtkinter.CTkEntry(self.ss_window,
                                                        textvariable=set_transaction_type_entry)
        transaction_type_entry.configure(state="disabled")

        transaction_type_entry.place(relx=0.18, rely=0.675, relwidth=0.8, relheight=0.07)

        # dictionary of entries
        entry_dic = {"name": name_of_security_entry, "ticker": ticker_entry,
            "timestamp": time_of_transaction_entry,
            "amount": amount_of_shares_entry,
            "transaction_type": transaction_type_entry
        }
        # entry button
        entry_button = customtkinter.CTkButton(self.ss_window,
                                               text="Enter",
                                               command=lambda: self.master.gb.insert_transaction_into_database(entry_dic, split=True))
        entry_button.place(relx=0, rely=0.8, relwidth=1, relheight=0.07)

        # return to main menu and exit button
        return_main_button = customtkinter.CTkButton(self.ss_window,
                                                     text="Close Window",
                                                     command=self.ss_window.destroy)
        exit_button = customtkinter.CTkButton(self.ss_window,
                                              text="Exit Program",
                                              command=self.master.on_closing)

        return_main_button.place(relx=0, rely=0.919, relwidth=0.2, relheight=0.08)
        exit_button.place(relx=0.8, rely=0.919, relwidth=0.2, relheight=0.08)
