import tkinter as tk
from tkinter import ttk
import customtkinter
from .records import Records
from .appearance import Appearance

class ShowStockSplitDataWindow(customtkinter.CTkFrame):
    '''class to show the stock split history on treeview'''
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
        self.tree_scroll = ttk.Scrollbar(self.main_view, orient="vertical",
                                         command=self.my_tree.yview,
                                         style='arrowless.Vertical.TScrollbar')
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # configure scrollbar
        self.my_tree.configure(yscrollcommand=self.tree_scroll.set)


        self.style.theme_use('default')

        self.style.layout('arrowless.Vertical.TScrollbar', [('Vertical.Scrollbar.trough',
        {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])

        # set style based upon style selection
        self.ap.change_appearance_mode(self.master.appearance_options.get())

        # data
        # add columns for transactions
        self.my_tree['columns'] = ("History ID", "Name", "Ticker", "Split Amount", "Date of Split")
        # format columns
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        columns = ["History ID", "Name", "Ticker", "Split Amount", "Date of Split"]
        for i in columns:
          self.my_tree.column(f"{i}", anchor='w' , width=0)
        # create headings
        self.my_tree.heading("#0", text="",anchor=tk.W)
        for i in columns:
          self.my_tree.heading(f"{i}", text=f"{i}", anchor='w')

        # insert transactions
        self.rc.query_database(self.master.db.get_stock_split_history)

        self.window_menu()

    def window_menu(self):
        # ================================= Tree View Menu =================================

        # add record entry boxes
        self.data_frame = customtkinter.CTkFrame(master=self.parent)
        self.data_frame.place(relx=0, rely=0.7, relheight=0.20, relwidth=1, anchor='nw')

        # column 1
        history_id_label = customtkinter.CTkLabel(self.data_frame, text="ID", anchor='w')
        history_id_label.place(relx=0.005, rely=0, relheight=0.4, relwidth=0.08, anchor=tk.NW)
        history_id_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        history_id_entry.place(relx=0.087, rely=0.1, relwidth=0.145, anchor=tk.NW)

        split_amount_label = customtkinter.CTkLabel(self.data_frame, text="Split Amount", anchor='w')
        split_amount_label.place(relx=0.005, rely=0.6, relheight=0.4, relwidth=0.08, anchor='nw')
        split_amount_entry = customtkinter.CTkEntry(self.data_frame, height = 25)
        split_amount_entry.place(relx=0.087, rely=0.7, relwidth=0.145, anchor='nw')

        # column 2

        security_label = customtkinter.CTkLabel(self.data_frame, text="Name", anchor='w')
        security_label.place(relx=0.362, rely=0, relheight=0.4, relwidth=0.08, anchor='nw')
        security_entry = customtkinter.CTkEntry(self.data_frame, height = 25)
        security_entry.place(relx=0.462, rely=0.1, relwidth=0.145, anchor=tk.NW)

        ticker_label = customtkinter.CTkLabel(self.data_frame, text="Ticker", anchor='w')
        ticker_label.place(relx=0.362, rely=0.6, relheight=0.4, relwidth=0.08, anchor=tk.NW)
        ticker_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        ticker_entry.place(relx=0.462, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 3

        date_label = customtkinter.CTkLabel(self.data_frame, text="Split Date", anchor='w')
        date_label.place(relx=0.75, rely=0, relheight=0.4, relwidth=0.08, anchor=tk.NW)
        date_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        date_entry.place(relx=0.85, rely=0.1, relwidth=0.145, anchor=tk.NW)

        # dictionary of entries
        history_entries={"security_entry":security_entry, "ticker_entry":ticker_entry,
        "history_id":history_id_entry, "timestamp": date_entry, "split_amount": split_amount_entry}

        # add buttons
        self.button_frame = customtkinter.CTkFrame(self.parent)
        self.button_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1, anchor=tk.NW)

        update_button = customtkinter.CTkButton(self.button_frame,text="Update Record",
                                                command=lambda:self.rc.update_record(history_entries))
        update_button.place(relx=0.005, rely=0.25, relwidth=0.225)

        rm_rec_button = customtkinter.CTkButton(self.button_frame, text="Remove Record",
                                                command=lambda:self.rc.delete_record(history_entries))
        rm_rec_button.place(relx=0.262, rely=0.25, relwidth=0.225)

        mm_button = customtkinter.CTkButton(self.button_frame, text="Delete All Records",
                                            command=self.rc.delete_all_data)
        mm_button.place(relx=0.519, rely=0.25, relwidth=0.225)

        ex_button = customtkinter.CTkButton(self.button_frame, text="Exit Program",
                                            command=self.master.on_closing)
        ex_button.place(relx=0.77, rely=0.25, relwidth=0.225)
        # bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", lambda event: self.rc.select_record(event, history_entries))
        self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.rc.select_record(event, history_entries))



