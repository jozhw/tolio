import tkinter as tk
from tkinter import ttk
import customtkinter
from .records import Records
from .appearance import Appearance

class ShowInstitutionsHeldWindow(customtkinter.CTkFrame):
    '''class method to show securities held at institutions on treeview'''
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


        # treeview styling
        self.style = ttk.Style()
        self.style.theme_use('default')

        self.style.layout('arrowless.Vertical.TScrollbar',
                          [('Vertical.Scrollbar.trough',
                            {'children': [('Vertical.Scrollbar.thumb',
                                           {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])

        # set style based upon style selection
        self.ap.change_appearance_mode(self.master.appearance_options.get())

        # data
        # add columns for transactions
        self.my_tree['columns'] = ("Institution", "Security", "Amount", "Total Cost",
                                   "Cost Basis", "Number Long", "Total Price Sold",
                                   "Average Price Sold" )
        # format columns
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        columns = ["Institution", "Security", "Amount", "Total Cost", "Cost Basis",
                   "Number Long", "Total Price Sold", "Average Price Sold"]
        for i in columns:
            self.my_tree.column(f"{i}", anchor='w', width=0)
        # create headings
        self.my_tree.heading("#0",text="",anchor=tk.W)
        for i in columns:
            self.my_tree.heading(f"{i}", text=f"{i}", anchor='w')

        # insert transactions
        self.rc.query_database(self.master.db.get_institutions_held_table)

        self.window_menu()

    def window_menu(self):
        # ================================= Tree View Menu =================================

        # add record entry boxes
        self.data_frame = customtkinter.CTkFrame(master=self.parent)
        self.data_frame.place(relx=0, rely=0.7, relheight=0.20, relwidth=1, anchor='nw')

        # column 1
        institution_label = customtkinter.CTkLabel(self.data_frame, text="Institution", anchor='w')
        institution_label.place(relx=0.005, rely=0, relheight=0.4, relwidth=0.06, anchor='nw')
        institution_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        institution_entry.place(relx=0.085, rely=0.1, relwidth=0.145, anchor='nw')

        security_label = customtkinter.CTkLabel(self.data_frame,text="Security", anchor='w')
        security_label.place(relx=0.005, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        security_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        security_entry.place(relx=0.085, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 2
        amount_label = customtkinter.CTkLabel(self.data_frame, text="Amount", anchor='w')
        amount_label.place(relx=0.262, rely=0, relheight=0.4, relwidth=0.06, anchor='nw')
        amount_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        amount_entry.place(relx=0.342, rely=0.1, relwidth=0.145, anchor=tk.NW)

        number_long_label = customtkinter.CTkLabel(self.data_frame, text="Long", anchor='w')
        number_long_label.place(relx=0.262,rely=0.6,relheight=0.4, relwidth=0.06, anchor=tk.NW)
        number_long_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        number_long_entry.place(relx=0.342, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 3
        cost_basis_label = customtkinter.CTkLabel(self.data_frame, text="Cost Basis", anchor='w')
        cost_basis_label.place(relx=0.519, rely=0, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        cost_basis_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        cost_basis_entry.place(relx=0.599, rely=0.1, relwidth=0.145, anchor=tk.NW)

        total_cost_label = customtkinter.CTkLabel(self.data_frame, text="Total Cost", anchor='w')
        total_cost_label.place(relx=0.519, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        total_cost_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        total_cost_entry.place(relx=0.599, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 4
        average_price_sold_label = customtkinter.CTkLabel(self.data_frame, text="A.P. Sold", anchor='w')
        average_price_sold_label.place(relx=0.77, rely=0, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        average_price_sold_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        average_price_sold_entry.place(relx=0.85, rely=0.1, relwidth=0.145, anchor=tk.NW)

        total_price_sold_label = customtkinter.CTkLabel(self.data_frame, text="T.P. Sold", anchor='w')
        total_price_sold_label.place(relx=0.77, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        total_price_sold_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        total_price_sold_entry.place(relx=0.85, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # dictionary of entries
        transaction_entries={"institution_entry":institution_entry, "security_entry":security_entry, "amount_entry":amount_entry,
            "total_cost_entry":total_cost_entry,"cost_basis_entry":cost_basis_entry,"long_entry":number_long_entry,
            "total_price_sold":total_price_sold_entry,"average_price_sold":average_price_sold_entry}

        # add buttons
        self.button_frame = customtkinter.CTkFrame(self.parent)
        self.button_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1, anchor=tk.NW)

        ex_button=customtkinter.CTkButton(self.button_frame, text="Exit Program", command=self.master.on_closing)
        ex_button.place(relx=0.77, rely=0.25, relwidth=0.225)
        # bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", lambda event: self.rc.select_record(event,transaction_entries))
        self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.rc.select_record(event,transaction_entries))
