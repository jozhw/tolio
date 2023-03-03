'''module that houses the ShowTransactionWindow class to show transactions on the treeview'''
import tkinter as tk
import customtkinter

from tkinter import ttk
from .records import Records
from .appearance import Appearance

class ShowTransactionWindow(customtkinter.CTkFrame):
    '''class that shows the list of transactions on treeview'''

    def __init__(self, master, parent):
        super().__init__(master)
        self.master = master
        self.parent = parent
        # ================================= Tree View =================================
       # create treeview
        self.main_view = customtkinter.CTkFrame(self.parent)
        self.main_view.place(relx=0, rely=0.05, relheight=0.65, relwidth=1, anchor="nw")
        # create tree
        self.my_tree = ttk.Treeview(self.main_view, selectmode="extended")
        self.my_tree.place(relx=0, rely=0, relheight=1, relwidth=1, anchor="nw")
         # treeview styling
        self.style = ttk.Style()

        # define records class instance
        self.rc = Records(self.master, self.my_tree)

        # define appearance class instance
        self.ap = Appearance(self.master, self.my_tree, self.style)


        # scrollbar
        self.tree_scroll = ttk.Scrollbar(self.main_view,orient="vertical",
                                         command=self.my_tree.yview,
                                         style='arrowless.Vertical.TScrollbar')
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # configure scrollbar
        self.my_tree.configure(yscrollcommand=self.tree_scroll.set)
        self.style.theme_use('default')
        self.style.layout('arrowless.Vertical.TScrollbar',
                          [('Vertical.Scrollbar.trough',
                            {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})],
                             'sticky': 'ns'})])

        # set style based upon style selection
        self.ap.change_appearance_mode(self.master.appearance_options.get())

        # data
        self.my_tree['columns'] = ("ID", "Name","Ticker", "Institution", "Date",
                                   "Type", "From", "To", "Price", "Amount", "Age",
                                   "Long" )
        # format columns
        self.my_tree.column("#0", width=0, stretch='no')
        columns = ["ID", "Name", "Ticker", "Institution", "Date", "Type", "From",
                   "To", "Price", "Amount", "Age", "Long" ]
        for i in columns:
            self.my_tree.column(f"{i}", anchor='w', width=0)
        # create headings
        self.my_tree.heading("#0", text="", anchor='w')
        for i in columns:
            self.my_tree.heading(f"{i}", text=f"{i}", anchor='w')

        # insert transactions
        self.rc.query_database(self.master.db.get_transactions_table)

        self.window_menu()
        self.after(500, self.ap.delay_appearance)

    def window_menu(self):
        # ================================== Tree View Menu =================================

        # add record entry boxes
        self.data_frame = customtkinter.CTkFrame(master=self.parent)
        self.data_frame.place(relx=0, rely=0.7, relheight=0.20, relwidth=1, anchor='nw')

        # column 1
        id_label = customtkinter.CTkLabel(self.data_frame,text="ID", anchor='w')
        id_label.place(relx=0.005, rely=0, relheight=0.4, relwidth=0.06, anchor='nw')
        id_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        id_entry.place(relx=0.085, rely=0.1, relwidth=0.145, anchor='nw')

        date_label = customtkinter.CTkLabel(self.data_frame, text="Date", anchor='w')
        date_label.place(relx=0.005, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        date_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        date_entry.place(relx=0.085, rely=0.4, relwidth=0.145, anchor=tk.NW)

        price_label = customtkinter.CTkLabel(self.data_frame,text="Price", anchor='w')
        price_label.place(relx=0.005, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        price_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        price_entry.place(relx=0.085, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 2

        n_label = customtkinter.CTkLabel(self.data_frame, text="Name", anchor='w')
        n_label.place(relx=0.262,rely=0,relheight=0.4, relwidth=0.06, anchor=tk.NW)
        n_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        n_entry.place(relx=0.342, rely=0.1, relwidth=0.145, anchor=tk.NW)

        type_label = customtkinter.CTkLabel(self.data_frame, text="Type", anchor='w')
        type_label.place(relx=0.262, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        type_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        type_entry.place(relx=0.342, rely=0.4, relwidth=0.145, anchor=tk.NW)

        amount_label = customtkinter.CTkLabel(self.data_frame, text="Amount", anchor='w')
        amount_label.place(relx=0.262, rely=0.6, relheight=0.4, relwidth=0.06, anchor='nw')
        amount_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        amount_entry.place(relx=0.342, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 3

        ticker_label = customtkinter.CTkLabel(self.data_frame, text="Ticker", anchor='w')
        ticker_label.place(relx=0.519, rely=0, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        ticker_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        ticker_entry.place(relx=0.599, rely=0.1, relwidth=0.145, anchor=tk.NW)

        from_label = customtkinter.CTkLabel(self.data_frame,text="From", anchor='w')
        from_label.place(relx=0.519, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        from_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        from_entry.place(relx=0.599, rely=0.4, relwidth=0.145, anchor=tk.NW)

        age_label = customtkinter.CTkLabel(self.data_frame, text="Age", anchor='w')
        age_label.place(relx=0.519, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        age_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        age_entry.place(relx=0.599, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 4

        institution_label = customtkinter.CTkLabel(self.data_frame,text="Institution", anchor='w')
        institution_label.place(relx=0.77, rely=0, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        institution_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        institution_entry.place(relx=0.85, rely=0.1, relwidth=0.145, anchor=tk.NW)

        to_label = customtkinter.CTkLabel(self.data_frame,text="To", anchor='w')
        to_label.place(relx=0.77, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        to_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        to_entry.place(relx=0.85, rely=0.4, relwidth=0.145, anchor=tk.NW)

        long_label = customtkinter.CTkLabel(self.data_frame, text="Long", anchor='w')
        long_label.place(relx=0.77, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        long_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        long_entry.place(relx=0.85, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # dictionary of entries
        transaction_entries={"id_entry":id_entry,"n_entry":n_entry,"ticker_entry":ticker_entry,
        "institution_entry":institution_entry,"date_entry":date_entry,"type_entry":type_entry,
        "from_entry":from_entry,"to_entry":to_entry,"price_entry":price_entry,"amount_entry":amount_entry,
        "age_entry":age_entry,"long_entry":long_entry}

        # add buttons
        self.button_frame = customtkinter.CTkFrame(self.parent)
        self.button_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1, anchor=tk.NW)

        update_button = customtkinter.CTkButton(self.button_frame, text="Update Record",
                                                command=lambda:self.rc.update_record(transaction_entries))
        update_button.place(relx=0.005, rely=0.25, relwidth=0.225)

        rm_rec_button = customtkinter.CTkButton(self.button_frame, text="Remove Record",
                                                command=lambda:self.rc.delete_record(transaction_entries))
        rm_rec_button.place(relx=0.262, rely=0.25, relwidth=0.225)

        mm_button = customtkinter.CTkButton(self.button_frame, text="Delete All Records",
                                            command=self.rc.delete_all_data)
        mm_button.place(relx=0.519, rely=0.25, relwidth=0.225)

        ex_button = customtkinter.CTkButton(self.button_frame, text="Exit Program",
                                            command=self.master.on_closing)
        ex_button.place(relx=0.77, rely=0.25, relwidth=0.225)

        self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.rc.select_record(event,transaction_entries))
        self.my_tree.bind("<ButtonRelease-1>", lambda event: self.rc.select_record(event,transaction_entries))
