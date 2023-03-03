'''main.py file'''
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from typing import Dict, Any, Callable, List
import customtkinter 
import darkdetect
from PIL import Image
from utils import ResourcePath, get_previous_setting, save_previous_setting, export_csv, insert_csv
from database import Database
from gui_bridge import GuiBridge

class App(customtkinter.CTk):
    '''class for the gui of the application'''

    # aesthetics
    style_resource_path = ResourcePath("src/assets/styling/")
    icon_resource_path = ResourcePath("src/assets/icons/")
    set_settings_resource_path = style_resource_path.resource_path("set_settings.json")
    customtkinter.set_appearance_mode(get_previous_setting(set_settings_resource_path, appearance_option = True))
    customtkinter.set_default_color_theme(style_resource_path.resource_path("style.json"))
    WIDTH = 1300
    HEIGHT = 600

    # define class objects
    db = Database()
    gb = GuiBridge()
    
    def __init__(self):
        super().__init__()
        self.title("Tolio - Portfolio Tracker")
        logo_path = tk.PhotoImage(file=self.icon_resource_path.resource_path("tolio_icon.png"))
        self.iconphoto(False,logo_path)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # not resizable
        self.minsize(App.WIDTH,App.HEIGHT)
        self.maxsize(App.WIDTH,App.HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # call .on_closing() when app gets closed

        # ================================= create two frames (menu bar & activity bar) ===============================

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frame_left = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")
        
        self.frame_right = customtkinter.CTkFrame(self, corner_radius=10)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ================================= menu bar =================================

        # all image icons for menu
        self.add_icon = customtkinter.CTkImage(dark_image=Image.open(self.icon_resource_path.resource_path("add_dark.png")),
                                                        light_image=Image.open(self.icon_resource_path.resource_path("add_light.png")))

        self.refresh_icon = customtkinter.CTkImage(dark_image=Image.open(self.icon_resource_path.resource_path("refresh_dark.png")),
                                                        light_image=Image.open(self.icon_resource_path.resource_path("refresh_light.png")))

        self.transfer_icon = customtkinter.CTkImage(dark_image=Image.open(self.icon_resource_path.resource_path("transfer_dark.png")),
                                                        light_image=Image.open(self.icon_resource_path.resource_path("transfer_light.png"))
                                                        )
        self.ss_icon = customtkinter.CTkImage(dark_image = Image.open(self.icon_resource_path.resource_path("ss_dark.png")),
                                                        light_image=Image.open(self.icon_resource_path.resource_path("ss_light.png")))

        self.documentation_icon = customtkinter.CTkImage(dark_image=Image.open(self.icon_resource_path.resource_path("doc_dark.png")),
                                                        light_image=Image.open(self.icon_resource_path.resource_path("doc_light.png")))

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(8, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(9, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        # menu label
        self.menu_label = customtkinter.CTkLabel(self.frame_left,
                                                text="Menu",
                                                font=("Roboto Medium", -20))  # font name and size in px
        self.menu_label.grid(row=1, column=0, pady=10, padx=10)

        # refresh button
        self.refresh_button = customtkinter.CTkButton(self.frame_left,
                                                text="Refresh",
                                                border_color = "black",
                                                command=self.refresh_page,
                                                image=self.refresh_icon,
                                                anchor="w")
        self.refresh_button.grid(row=2, column=0, pady=15, padx=20)

        # add transaction button
        self.add_transaction_button = customtkinter.CTkButton(self.frame_left,
                                                text="Add",
                                                border_color="black",
                                                command=self.window_add_transaction,
                                                image=self.add_icon,
                                                anchor="w"
                                                )
        self.add_transaction_button.grid(row=3, column=0, pady=15, padx=20)

        # transfer institution button
        self.transfer_institution_button = customtkinter.CTkButton(self.frame_left,
                                                text="Transfer",
                                                border_color="black",
                                                command=self.window_transfer_institution,
                                                image=self.transfer_icon,
                                                anchor="w"
                                                )
        self.transfer_institution_button.grid(row=4, column=0, pady=15, padx=20)

        # stock split button
        self.stock_split_button = customtkinter.CTkButton(self.frame_left,
                                                text="Stock Split",
                                                border_color = "black",
                                                image = self.ss_icon,
                                                anchor="w",
                                                command=self.window_stock_split
                                                )
        self.stock_split_button.grid(row=5, column=0, pady=15, padx=20)

        # upload csv button
        self.import_file_dial_button = customtkinter.CTkButton(self.frame_left,
                                                text="Upload CSV",
                                                border_color="black",
                                                image=self.documentation_icon,
                                                anchor="w",
                                                command=self.window_import_filedialog
                                                )
        self.import_file_dial_button.grid(row=6, column=0, pady=15, padx=20)

        # export csv button
        self.export_file_dial_button = customtkinter.CTkButton(self.frame_left,
                                                text="Export to CSV",
                                                border_color="black",
                                                image=self.documentation_icon,
                                                anchor="w",
                                                command=self.window_export_filedialog
                                                )
        self.export_file_dial_button.grid(row=7, column=0, pady=15, padx=20)


        # set color scheme
        self.appearance_mode = customtkinter.CTkLabel(self.frame_left,
                                                text="Appearance Mode:")
        self.appearance_mode.grid(row=10,column=0,pady=0,padx=20,sticky="w")

        self.appearance_options_set = customtkinter.StringVar(value=get_previous_setting(self.set_settings_resource_path,appearance_option=True))  # set initial value

        self.appearance_options = customtkinter.CTkOptionMenu(self.frame_left,
                                                            values=["System", "Dark", "Light"],
                                                            command=self.change_appearance_mode,
                                                            variable=self.appearance_options_set)
        self.appearance_options.grid(row=11, column=0, pady=10, padx=20, sticky="w")
      
        # ================================= data section - right frame section =================================
        # create multibutton to select different data to display
        self.transition_menu = customtkinter.CTkSegmentedButton(self.frame_right, values=["Transactions", "Institutions Held", "Securities", "Stock Split History"]) # to add for non-beta version "Individual Shares" tab
        self.transition_menu.place(relx=0,rely=0,relwidth=1,anchor="nw")
        self.transition_menu.set(get_previous_setting(self.set_settings_resource_path,transition_menu=True))
        self.transition_menu.configure(command=self.tab_selection)
        self.tab_selection(get_previous_setting(self.set_settings_resource_path,transition_menu=True))
            
    # ================================= data section window displays =================================

    # select tab for the following four menus
    def tab_selection(self, value:str) -> None:
        if value == "Transactions":
            self.show_transaction_window()
        elif value == "Institutions Held":
            self.show_institutions_held_window()
        elif value == "Securities":
            self.show_securities_window()
        elif value == "Stock Split History":
            self.show_stock_split_data_window()

    # menu for showing all transactions in the database
    def show_transaction_window(self) -> None:
        '''class method to show transactions treeview'''

        # ================================= Tree View =================================

        # create treeview
        self.main_view = customtkinter.CTkFrame(self.frame_right)
        self.main_view.place(relx=0,rely=0.05,relheight=0.65,relwidth=1, anchor="nw")
        # create tree
        self.my_tree=ttk.Treeview(self.main_view, selectmode="extended")
        self.my_tree.place(relx=0, rely=0, relheight=1, relwidth=1, anchor="nw")
        # scrollbar
        self.tree_scroll=ttk.Scrollbar(self.main_view,orient="vertical", command=self.my_tree.yview, style='arrowless.Vertical.TScrollbar')
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # configure scrollbar
        self.my_tree.configure(yscrollcommand=self.tree_scroll.set)
        
        # treeview styling 
        self.style=ttk.Style()
        self.style.theme_use('default')

        self.style.layout('arrowless.Vertical.TScrollbar', [('Vertical.Scrollbar.trough', 
        {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])

        # set style based upon style selection
        self.change_appearance_mode(self.appearance_options.get())

        # data
        self.my_tree['columns']=("ID", "Name","Ticker", "Institution","Date","Type","From","To","Price","Amount","Age","Long" )
        # format columns
        self.my_tree.column("#0", width=0,stretch='no')
        columns=["ID", "Name","Ticker", "Institution","Date","Type","From","To","Price","Amount","Age","Long" ]
        for i in columns:
            self.my_tree.column(f"{i}", anchor='w' ,width=0)
        # create headings
        self.my_tree.heading("#0", text="", anchor='w')
        for i in columns:
            self.my_tree.heading(f"{i}", text=f"{i}", anchor='w')

        # insert transactions
        self.query_database(self.db.get_transactions_table)

        # ================================== Tree View Menu =================================

        # add record entry boxes
        self.data_frame=customtkinter.CTkFrame(master=self.frame_right)
        self.data_frame.place(relx=0, rely=0.7, relheight=0.20, relwidth=1, anchor='nw')

        # column 1
        id_label=customtkinter.CTkLabel(self.data_frame,text="ID", anchor='w')
        id_label.place(relx=0.005, rely=0, relheight=0.4, relwidth=0.06, anchor='nw')
        id_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        id_entry.place(relx=0.085, rely=0.1, relwidth=0.145, anchor='nw')

        date_label=customtkinter.CTkLabel(self.data_frame, text="Date", anchor='w')
        date_label.place(relx=0.005, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        date_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        date_entry.place(relx=0.085, rely=0.4, relwidth=0.145, anchor=tk.NW)

        price_label=customtkinter.CTkLabel(self.data_frame,text="Price", anchor='w')
        price_label.place(relx=0.005, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        price_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        price_entry.place(relx=0.085, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 2

        n_label=customtkinter.CTkLabel(self.data_frame, text="Name", anchor='w')
        n_label.place(relx=0.262,rely=0,relheight=0.4, relwidth=0.06, anchor=tk.NW)
        n_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        n_entry.place(relx=0.342, rely=0.1, relwidth=0.145, anchor=tk.NW)

        type_label=customtkinter.CTkLabel(self.data_frame, text="Type", anchor='w')
        type_label.place(relx=0.262, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        type_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        type_entry.place(relx=0.342, rely=0.4, relwidth=0.145, anchor=tk.NW)

        amount_label=customtkinter.CTkLabel(self.data_frame, text="Amount", anchor='w')
        amount_label.place(relx=0.262, rely=0.6, relheight=0.4, relwidth=0.06, anchor='nw')
        amount_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        amount_entry.place(relx=0.342, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 3

        ticker_label=customtkinter.CTkLabel(self.data_frame, text="Ticker", anchor='w')
        ticker_label.place(relx=0.519, rely=0, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        ticker_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        ticker_entry.place(relx=0.599, rely=0.1, relwidth=0.145, anchor=tk.NW)

        from_label=customtkinter.CTkLabel(self.data_frame,text="From", anchor='w')
        from_label.place(relx=0.519, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        from_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        from_entry.place(relx=0.599, rely=0.4, relwidth=0.145, anchor=tk.NW)

        age_label=customtkinter.CTkLabel(self.data_frame, text="Age", anchor='w')
        age_label.place(relx=0.519, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        age_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        age_entry.place(relx=0.599, rely=0.7, relwidth=0.145, anchor=tk.NW)

        # column 4

        institution_label=customtkinter.CTkLabel(self.data_frame,text="Institution", anchor='w')
        institution_label.place(relx=0.77, rely=0, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        institution_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        institution_entry.place(relx=0.85, rely=0.1, relwidth=0.145, anchor=tk.NW)

        to_label=customtkinter.CTkLabel(self.data_frame,text="To", anchor='w')
        to_label.place(relx=0.77, rely=0.3, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        to_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        to_entry.place(relx=0.85, rely=0.4, relwidth=0.145, anchor=tk.NW)

        long_label=customtkinter.CTkLabel(self.data_frame, text="Long", anchor='w')
        long_label.place(relx=0.77, rely=0.6, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        long_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        long_entry.place(relx=0.85, rely=0.7, relwidth=0.145, anchor=tk.NW)
        
        # dictionary of entries
        transaction_entries={"id_entry":id_entry,"n_entry":n_entry,"ticker_entry":ticker_entry,
        "institution_entry":institution_entry,"date_entry":date_entry,"type_entry":type_entry,
        "from_entry":from_entry,"to_entry":to_entry,"price_entry":price_entry,"amount_entry":amount_entry,
        "age_entry":age_entry,"long_entry":long_entry}
        
        # add buttons
        self.button_frame=customtkinter.CTkFrame(self.frame_right)
        self.button_frame.place(relx=0,rely=0.9,relheight=0.1,relwidth=1,anchor=tk.NW)

        update_button=customtkinter.CTkButton(self.button_frame,text="Update Record",command=lambda:self.update_record(transaction_entries))
        update_button.place(relx=0.005, rely=0.25, relwidth=0.225)

        rm_rec_button=customtkinter.CTkButton(self.button_frame,text="Remove Record",command=lambda:self.delete_record(transaction_entries))
        rm_rec_button.place(relx=0.262, rely=0.25, relwidth=0.225)

        mm_button=customtkinter.CTkButton(self.button_frame,text="Delete All Records", command=self.delete_all_data)
        mm_button.place(relx=0.519, rely=0.25, relwidth=0.225)

        ex_button=customtkinter.CTkButton(self.button_frame,text="Exit Program",command=self.on_closing)
        ex_button.place(relx=0.77,rely=0.25, relwidth=0.225)
      
        self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.select_record(event,transaction_entries))
        self.my_tree.bind("<ButtonRelease-1>", lambda event: self.select_record(event,transaction_entries))
        

    # menu for showing all securities held for each particular institution
    def show_institutions_held_window(self) -> None:
        # ================================= Tree View =================================

        # create treeview
        self.main_view = customtkinter.CTkFrame(self.frame_right)
        self.main_view.place(relx=0, rely=0.05, relheight=0.65, relwidth=1, anchor="nw")
        # create tree
        self.my_tree = ttk.Treeview(self.main_view, selectmode="extended")
        self.my_tree.place(relx=0, rely=0, relheight=1, relwidth=1, anchor="nw")
        # scrollbar
        self.tree_scroll = ttk.Scrollbar(self.main_view,orient="vertical",command=self.my_tree.yview, style='arrowless.Vertical.TScrollbar')
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # configure scrollbar
        self.my_tree.configure(yscrollcommand=self.tree_scroll.set)
        

        # treeview styling 
        self.style=ttk.Style()
        self.style.theme_use('default')

        self.style.layout('arrowless.Vertical.TScrollbar', [('Vertical.Scrollbar.trough', 
        {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])

        # set style based upon style selection
        self.change_appearance_mode(self.appearance_options.get())

        # data
        # add columns for transactions
        self.my_tree['columns']=("Institution", "Security", "Amount", "Total Cost", "Cost Basis", "Number Long", "Total Price Sold", "Average Price Sold" )
        # format columns
        self.my_tree.column("#0", width=0,stretch=tk.NO)
        columns = ["Institution", "Security", "Amount", "Total Cost", "Cost Basis", "Number Long", "Total Price Sold", "Average Price Sold"]
        for i in columns:
            self.my_tree.column(f"{i}", anchor='w' ,width=0)
        # create headings
        self.my_tree.heading("#0",text="",anchor=tk.W)
        for i in columns:
            self.my_tree.heading(f"{i}",text=f"{i}",anchor='w')

        # insert transactions
        self.query_database(self.db.get_institutions_held_table)

        # ================================= Tree View Menu =================================

        # add record entry boxes
        self.data_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.data_frame.place(relx=0, rely=0.7, relheight=0.20, relwidth=1, anchor='nw')

        # column 1
        institution_label = customtkinter.CTkLabel(self.data_frame,text="Institution", anchor='w')
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

        number_long_label=customtkinter.CTkLabel(self.data_frame,text="Long", anchor='w')
        number_long_label.place(relx=0.262,rely=0.6,relheight=0.4,relwidth=0.06,anchor=tk.NW)
        number_long_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        number_long_entry.place(relx=0.342,rely=0.7,relwidth=0.145,anchor=tk.NW)

        # column 3
        cost_basis_label = customtkinter.CTkLabel(self.data_frame, text="Cost Basis", anchor='w')
        cost_basis_label.place(relx=0.519, rely=0,relheight=0.4, relwidth=0.06, anchor=tk.NW)
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
        self.button_frame = customtkinter.CTkFrame(self.frame_right)
        self.button_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1, anchor=tk.NW)

        ex_button=customtkinter.CTkButton(self.button_frame, text="Exit Program", command=self.on_closing)
        ex_button.place(relx=0.77, rely=0.25, relwidth=0.225)
        # bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", lambda event: self.select_record(event,transaction_entries))
        self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.select_record(event,transaction_entries))

    # menu for showing the summaries of the securities (does not include institutions)
    def show_securities_window(self) -> None:

        # ================================= Tree View =================================

        # create treeview
        self.main_view = customtkinter.CTkFrame(self.frame_right)
        self.main_view.place(relx=0, rely=0.05, relheight=0.65, relwidth=1, anchor="nw")
        # create tree
        self.my_tree = ttk.Treeview(self.main_view, selectmode="extended")
        self.my_tree.place(relx=0, rely=0, relheight=1, relwidth=1, anchor="nw")
        # scrollbar
        self.tree_scroll = ttk.Scrollbar(self.main_view,orient="vertical", command=self.my_tree.yview, style='arrowless.Vertical.TScrollbar')
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # configure scrollbar
        self.my_tree.configure(yscrollcommand=self.tree_scroll.set)
        
        # treeview styling 
        self.style = ttk.Style()
        self.style.theme_use('default')

        self.style.layout('arrowless.Vertical.TScrollbar', [('Vertical.Scrollbar.trough', 
        {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])

        # set style based upon style selection
        self.change_appearance_mode(self.appearance_options.get())

        # data
        # add columns for transactions
        self.my_tree['columns'] = ("Security", "Ticker", "Amount", "Total Cost", "Cost Basis", "Number Long", "Total Price Sold", "Average Price Sold" )
        # format columns
        self.my_tree.column("#0", width=0, stretch=tk.NO)
        columns=["Security", "Ticker", "Amount", "Total Cost", "Cost Basis", "Number Long", "Total Price Sold", "Average Price Sold"]
        for i in columns:
            self.my_tree.column(f"{i}", anchor='w' ,width=0)
        # create headings
        self.my_tree.heading("#0",text="",anchor=tk.W)
        for i in columns:
            self.my_tree.heading(f"{i}", text=f"{i}", anchor='w')

        # insert transactions
        self.query_database(self.db.get_security_table)

        # ================================= Tree View Menu =================================

        # add record entry boxes
        self.data_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.data_frame.place(relx=0, rely=0.7, relheight=0.20, relwidth=1, anchor='nw')

        # column 1
        security_label = customtkinter.CTkLabel(self.data_frame,text="Security", anchor='w')
        security_label.place(relx=0.005 ,rely=0, relheight=0.4, relwidth=0.06, anchor=tk.NW)
        security_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        security_entry.place(relx=0.085, rely=0.1, relwidth=0.145, anchor=tk.NW)

        ticker_label = customtkinter.CTkLabel(self.data_frame,text="Ticker", anchor='w')
        ticker_label.place(relx=0.005, rely=0.6, relheight=0.4, relwidth=0.06, anchor='nw')
        ticker_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        ticker_entry.place(relx=0.085, rely=0.7, relwidth=0.145, anchor='nw')

        # column 2
        amount_label=customtkinter.CTkLabel(self.data_frame,text="Amount", anchor='w')
        amount_label.place(relx=0.262,rely=0,relheight=0.4,relwidth=0.06,anchor='nw')
        amount_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        amount_entry.place(relx=0.342,rely=0.1,relwidth=0.145,anchor=tk.NW)

        number_long_label=customtkinter.CTkLabel(self.data_frame,text="Long", anchor='w')
        number_long_label.place(relx=0.262,rely=0.6,relheight=0.4,relwidth=0.06,anchor=tk.NW)
        number_long_entry=customtkinter.CTkEntry(self.data_frame, height=25)
        number_long_entry.place(relx=0.342,rely=0.7,relwidth=0.145,anchor=tk.NW)

        # column 3
        total_cost_label = customtkinter.CTkLabel(self.data_frame,text="Total Cost", anchor='w')
        total_cost_label.place(relx=0.519,rely=0,relheight=0.4,relwidth=0.06,anchor=tk.NW)
        total_cost_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        total_cost_entry.place(relx=0.599,rely=0.1,relwidth=0.145,anchor=tk.NW)

        cost_basis_label = customtkinter.CTkLabel(self.data_frame,text="Cost Basis", anchor='w')
        cost_basis_label.place(relx = 0.519,rely = 0.6, relheight=0.4, relwidth = 0.06, anchor = tk.NW)
        cost_basis_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        cost_basis_entry.place(relx = 0.599, rely = 0.7, relwidth = 0.145, anchor = tk.NW)

        # column 4
        total_price_sold_label = customtkinter.CTkLabel(self.data_frame, text="T.P. Sold", anchor='w')
        total_price_sold_label.place(relx=0.77,rely=0,relheight=0.4,relwidth=0.06,anchor=tk.NW)
        total_price_sold_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        total_price_sold_entry.place(relx=0.85,rely=0.1,relwidth=0.145,anchor=tk.NW)

        average_price_sold_label = customtkinter.CTkLabel(self.data_frame,text="A.P. Sold", anchor='w')
        average_price_sold_label.place(relx=0.77,rely=0.6,relheight=0.4,relwidth=0.06,anchor=tk.NW)
        average_price_sold_entry = customtkinter.CTkEntry(self.data_frame, height=25)
        average_price_sold_entry.place(relx=0.85,rely=0.7,relwidth=0.145,anchor=tk.NW)

        # dictionary of entries
        transaction_entries={"security_entry":security_entry, "ticker_entry":ticker_entry,
        "amount_entry":amount_entry, "total_cost_entry":total_cost_entry, "cost_basis_entry":cost_basis_entry,
        "long_entry":number_long_entry, "total_price_sold":total_price_sold_entry,"average_price_sold":average_price_sold_entry}
        
        # add buttons
        self.button_frame = customtkinter.CTkFrame(self.frame_right)
        self.button_frame.place(relx = 0, rely = 0.9, relheight = 0.1, relwidth = 1, anchor = tk.NW)

        # recalculate_button=customtkinter.CTkButton(self.button_frame,text="Recalculate Securities", command= Database().refresh_individual_shares)
        # recalculate_button.place(relx=0.005, rely=0.25, relwidth=0.225)

        ex_button=customtkinter.CTkButton(self.button_frame,text="Exit Program",command=self.on_closing)
        ex_button.place(relx=0.77,rely=0.25,relwidth=0.225)
        # bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", lambda event: self.select_record(event,transaction_entries))
        self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.select_record(event,transaction_entries))


    # menu for showing the stock split history
    def show_stock_split_data_window(self) -> None:

        # ================================= Tree View =================================

        # create treeview
        self.main_view = customtkinter.CTkFrame(self.frame_right)
        self.main_view.place(relx=0, rely=0.05, relheight=0.65, relwidth=1, anchor="nw")
        # create tree
        self.my_tree = ttk.Treeview(self.main_view, selectmode="extended")
        self.my_tree.place(relx=0, rely=0, relheight=1, relwidth=1, anchor="nw")
        # scrollbar
        self.tree_scroll = ttk.Scrollbar(self.main_view,orient="vertical",command=self.my_tree.yview, style='arrowless.Vertical.TScrollbar')
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        # configure scrollbar
        self.my_tree.configure(yscrollcommand=self.tree_scroll.set)
        

        # treeview styling 
        self.style = ttk.Style()
        self.style.theme_use('default')

        self.style.layout('arrowless.Vertical.TScrollbar', [('Vertical.Scrollbar.trough', 
        {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])

        # set style based upon style selection
        self.change_appearance_mode(self.appearance_options.get())

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
        self.query_database(self.db.get_stock_split_history)

        # ================================= Tree View Menu =================================

        # add record entry boxes
        self.data_frame = customtkinter.CTkFrame(master=self.frame_right)
        self.data_frame.place(relx=0, rely=0.7, relheight=0.20, relwidth=1, anchor='nw')

        # column 1
        history_id_label = customtkinter.CTkLabel(self.data_frame, text="ID", anchor='w')
        history_id_label.place(relx=0.005, rely=0, relheight=0.4, relwidth=0.08, anchor=tk.NW)
        history_id_entry=customtkinter.CTkEntry(self.data_frame, height=25)
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
        self.button_frame = customtkinter.CTkFrame(self.frame_right)
        self.button_frame.place(relx=0, rely=0.9, relheight=0.1, relwidth=1, anchor=tk.NW)

        update_button = customtkinter.CTkButton(self.button_frame,text="Update Record",command=lambda:self.update_record(history_entries))
        update_button.place(relx=0.005, rely=0.25, relwidth=0.225)

        rm_rec_button = customtkinter.CTkButton(self.button_frame, text="Remove Record", command=lambda:self.delete_record(history_entries))
        rm_rec_button.place(relx=0.262, rely=0.25, relwidth=0.225)

        mm_button = customtkinter.CTkButton(self.button_frame, text="Delete All Records", command=self.delete_all_data)
        mm_button.place(relx=0.519, rely=0.25, relwidth=0.225)

        ex_button = customtkinter.CTkButton(self.button_frame, text="Exit Program", command=self.on_closing)
        ex_button.place(relx=0.77, rely=0.25, relwidth=0.225)
        # bind the treeview
        self.my_tree.bind("<ButtonRelease-1>", lambda event: self.select_record(event,history_entries))
        self.my_tree.bind("<<TreeviewSelect>>", lambda event: self.select_record(event,history_entries))

  
    # ================================= menu button functionalities =================================

    # click for the add transaction window to pop up
    def window_add_transaction(self) -> None:
        self.transaction_window = customtkinter.CTkToplevel(self)
        self.transaction_window.title("Add Transaction")

        width = 1000
        height = 500
        self.transaction_window.geometry(f"{width}x{height}")
        self.transaction_window.minsize(width,height)
        self.transaction_window.maxsize(width,height)

        self.transaction_window.grid_rowconfigure(0, weight=1)
        window = customtkinter.CTkFrame(master=self.transaction_window, width=960, height=460)
        window.grid(row=0, column=0, padx=20, pady=20)

        # create title
        title=customtkinter.CTkLabel(window,text="Transaction Entry", corner_radius=10)
        title.configure(font=("Arial Bold", 17))
        title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        # labels: name, ticker, institution_name, time of transaction, amount, price_USD
        label_rely = 0.1
        labels = ["Name of Security", "Ticker", "Institution Name", "Time of Transaction", "Amount of Shares", "Price in USD", "Transaction Type"]
        for i in labels:
          my_label=customtkinter.CTkLabel(window, text=i, anchor=tk.W)
          my_label.configure(font=('Arial Bold',13))
          my_label.place(relx=0.01, rely=label_rely, relwidth=0.2, relheight=0.1)
          label_rely = label_rely + 0.1

        # all entries but it is in combo box style
        name_of_security_entry = customtkinter.CTkComboBox(window, values=self.db.get_table_value("security_name"))
        name_of_security_entry.set(value = "")
        name_of_security_entry.place(relx=0.16,rely=0.125,relwidth=0.82, relheight=0.05)

        ticker_entry = customtkinter.CTkComboBox(window, values=self.db.get_table_value("security_ticker"))
        ticker_entry.set(value="")
        ticker_entry.place(relx=0.16, rely=0.225, relwidth=0.82, relheight=0.05)

        institution_name_entry = customtkinter.CTkComboBox(window, values=self.db.get_table_value("institution"))
        institution_name_entry.set(value="")
        institution_name_entry.place(relx=0.16, rely=0.325, relwidth=0.82, relheight=0.05)

        tot_text = "Input in the format \"YYYY-MM-DD\" with each character being an integer or leave this field empty for current date and time."
        time_of_transaction_entry = customtkinter.CTkEntry(window, placeholder_text=tot_text)
        time_of_transaction_entry.place(relx=0.16,rely=0.425, relwidth=0.82, relheight=0.05)

        amount_of_shares_entry = customtkinter.CTkEntry(window, placeholder_text="Input only a number.")
        amount_of_shares_entry.place(relx=0.16, rely=0.525, relwidth=0.82, relheight=0.05)

        price_usd_entry = customtkinter.CTkEntry(window, placeholder_text="Input only a number. Do not input the currency.")
        price_usd_entry.place(relx=0.16, rely=0.625, relwidth=0.82, relheight=0.05)

        transaction_type_entry = customtkinter.CTkOptionMenu(window, values =["Acquire", "Dispose"], fg_color =("#F9F9FA", "#343638"),
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
        entry_button = customtkinter.CTkButton(window, text="Enter", command=lambda: self.gb.insert_transaction_into_database(entry_dic))
        entry_button.place(relx=0, rely=0.825, relwidth=1, relheight=0.05)

        # return to main menu and exit button
        return_main_button = customtkinter.CTkButton(window, text="Close Window", command=self.transaction_window.destroy)
        exit_button=customtkinter.CTkButton(window, text="Exit Program", command=self.on_closing)

        return_main_button.place(relx=0, rely=0.924, relwidth=0.2, relheight=0.075)
        exit_button.place(relx=0.8, rely=0.924, relwidth=0.2, relheight=0.075)

    def window_transfer_institution(self) -> None:
        self.tranfer_window_pop = customtkinter.CTkToplevel(self)
        self.tranfer_window_pop.title("Transfer Institution")

        width = 1000
        height = 500
        self.tranfer_window_pop.geometry(f"{width}x{height}")
        self.tranfer_window_pop.minsize(width,height)
        self.tranfer_window_pop.maxsize(width,height)

        self.tranfer_window_pop.grid_rowconfigure(0, weight=1)
        window = customtkinter.CTkFrame(master=self.tranfer_window_pop, width=960, height=460)
        window.grid(row=0,column=0, padx=20, pady=20)

        # create title
        title = customtkinter.CTkLabel(window,text="Transfer Institution Entry", corner_radius=10)
        title.configure(font = ("Arial Bold", 17))
        title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        # labels: name, ticker, institution_name, time of transaction, amount, price_usd
        label_rely = 0.1
        labels = ["Name of Security", "Ticker", "From Institution Name", "Time of Transaction", "Amount of Shares", "To Institution Name", "Transaction Type"]
        for i in labels:
            my_label=customtkinter.CTkLabel(window, text=i , anchor=tk.W)
            my_label.configure(font = ('Arial Bold',13))
            my_label.place(relx=0.01, rely=label_rely, relwidth=0.2, relheight=0.1)
            label_rely = label_rely + 0.1

        # all entries but it is in combo box style
        
        name_of_security_entry = customtkinter.CTkComboBox(window, values=self.db.get_table_value("name"))
        name_of_security_entry.set(value="")
        name_of_security_entry.place(relx=0.16, rely=0.125, relwidth=0.82, relheight=0.05)

        ticker_entry = customtkinter.CTkComboBox(window, values=self.db.get_table_value("ticker"))
        ticker_entry.set(value="")
        ticker_entry.place(relx=0.16, rely=0.225, relwidth=0.82, relheight=0.05)

        from_institution_name_entry = customtkinter.CTkComboBox(window, values=self.db.get_table_value("institution"))
        from_institution_name_entry.set(value = "")
        from_institution_name_entry.place(relx=0.16, rely=0.325, relwidth=0.82, relheight=0.05)

        time_of_transaction_entry = customtkinter.CTkEntry(window, placeholder_text="Input in the format \"YYYY-MM-DD\" with each character being an integer or leave this field empty for current date and time.")
        time_of_transaction_entry.place(relx=0.16, rely=0.425, relwidth=0.82, relheight=0.05)

        amount_of_shares_entry = customtkinter.CTkEntry(window, placeholder_text="Input only a number.")
        amount_of_shares_entry.place(relx=0.16, rely=0.525, relwidth=0.82, relheight=0.05)

        to_institution_name_entry = customtkinter.CTkComboBox(window, values=self.db.get_table_value("institution"))
        to_institution_name_entry.set(value="")
        to_institution_name_entry.place(relx=0.16, rely=0.625, relwidth=0.82, relheight=0.05)

        set_transaction_type_entry = customtkinter.StringVar(value="Transfer")
        transaction_type_entry = customtkinter.CTkEntry(window, textvariable=set_transaction_type_entry)
        transaction_type_entry.configure(state="disabled")
        
        transaction_type_entry.place(relx=0.16, rely=0.725, relwidth=0.82, relheight=0.05)

        set_price_usd_entry = customtkinter.StringVar(value=0)
        price_usd_entry = customtkinter.CTkEntry(window, textvariable=set_price_usd_entry)


        # dictionary of entries
        entry_dic = {"name": name_of_security_entry, "ticker": ticker_entry,
            "institution_name": from_institution_name_entry, "timestamp": time_of_transaction_entry,
            "amount": amount_of_shares_entry, "to_institution_name": to_institution_name_entry,
            "transaction_type": transaction_type_entry, "price_USD": price_usd_entry
        }

        # entry button
        entry_button=customtkinter.CTkButton(window, text="Enter", command=lambda: self.gb.insert_transaction_into_database(entry_dic, transfer= True))
        entry_button.place(relx=0, rely=0.825, relwidth=1, relheight=0.05)

        # return to main menu and exit button
        return_main_button=customtkinter.CTkButton(window, text="Close Window", command=self.tranfer_window_pop.destroy)
        exit_button=customtkinter.CTkButton(window, text="Exit Program", command=self.on_closing)

        return_main_button.place(relx=0, rely=0.924, relwidth=0.2, relheight=0.075)
        exit_button.place(relx=0.8, rely=0.924, relwidth=0.2, relheight=0.075)

    def window_stock_split(self) -> None:
        self.ss_window_pop = customtkinter.CTkToplevel(self)
        self.ss_window_pop.title("Stock Split")

        width = 750
        height = 400
        self.ss_window_pop.geometry(f"{width}x{height}")
        self.ss_window_pop.minsize(width,height)
        self.ss_window_pop.maxsize(width,height)


        self.ss_window_pop.grid_rowconfigure(0,weight=1)
        window = customtkinter.CTkFrame(master=self.ss_window_pop, width=720, height=360)
        window.grid(row=0,column=0, padx=15, pady=15)

        # create title
        title=customtkinter.CTkLabel(window,text="Stock Split Adjustment", corner_radius=10)
        title.configure(font=("Arial Bold", 17))
        title.place(relx=0, rely=0, relwidth=1, relheight=0.1)

            # labels: name, ticker, institution_name, time of transaction, amount, price_USD
        label_rely=0.1
        labels=["Name of Security", "Ticker", "Time of Split", "Split Amount", "Transaction Type"]
        for i in labels:
            my_label=customtkinter.CTkLabel(window, text=i, anchor=tk.W)
            my_label.configure(font=('Arial Bold',13))
            my_label.place(relx=0.01,rely=label_rely, relwidth=0.2, relheight=0.175)
            label_rely=label_rely+0.13

        # all entries but it is in combo box style
        
        name_of_security_entry = customtkinter.CTkOptionMenu(window, values=self.db.get_table_value("security_name"), fg_color=("#F9F9FA", "#343638"),
        button_color=("#979DA2", "#565B5E"),
        button_hover_color=("#6E7174", "#7A848D"))

        name_of_security_entry.set(value="")
        name_of_security_entry.place(relx=0.18,rely=0.155,relwidth=0.8,relheight=0.07)

        ticker_entry = customtkinter.CTkOptionMenu(window, values=self.db.get_table_value("security_ticker"), fg_color=("#F9F9FA", "#343638"),
        button_color=("#979DA2", "#565B5E"),
        button_hover_color=("#6E7174", "#7A848D"))

        ticker_entry.set(value="")
        ticker_entry.place(relx=0.18, rely=0.285, relwidth=0.8, relheight=0.07)

        time_of_transaction_entry = customtkinter.CTkEntry(window, placeholder_text="Leave empty or input in the format \"YYYY-MM-DD\" with each character being an integer.")
        time_of_transaction_entry.place(relx=0.18, rely=0.415, relwidth=0.8, relheight=0.07)

        amount_of_shares_entry = customtkinter.CTkEntry(window, placeholder_text="Input only a whole number.")
        amount_of_shares_entry.place(relx=0.18, rely=0.545, relwidth=0.8, relheight=0.07)

        set_transaction_type_entry = customtkinter.StringVar(value="Stock Split")
        transaction_type_entry = customtkinter.CTkEntry(window, textvariable=set_transaction_type_entry)
        transaction_type_entry.configure(state="disabled")
        
        transaction_type_entry.place(relx=0.18, rely=0.675, relwidth=0.8, relheight=0.07)

        # dictionary of entries
        entry_dic = {"name": name_of_security_entry, "ticker": ticker_entry,
            "timestamp": time_of_transaction_entry,
            "amount": amount_of_shares_entry,
            "transaction_type": transaction_type_entry
        }
        # entry button
        entry_button=customtkinter.CTkButton(window, text="Enter", command=lambda: self.gb.insert_transaction_into_database(entry_dic, split=True))
        entry_button.place(relx=0,rely=0.8,relwidth=1,relheight=0.07)

        # return to main menu and exit button
        return_main_button=customtkinter.CTkButton(window, text="Close Window", command=self.ss_window_pop.destroy)
        exit_button=customtkinter.CTkButton(window, text="Exit Program", command=self.on_closing)

        return_main_button.place(relx=0, rely=0.919, relwidth=0.2, relheight=0.08)
        exit_button.place(relx=0.8, rely=0.919, relwidth=0.2, relheight=0.08)

    def window_import_filedialog(self) -> None:
    
        self.import_file_name = filedialog.askopenfilename(title="Select A CSV File", filetypes=(("csv files", "*.csv"),))
        insert_csv(self.import_file_name)
    
    def window_export_filedialog(self) -> None:
        answer = messagebox.askyesno(title="Export Database",
                                    message="Would you like to export the database to a .csv file?")
        if answer == True:
             export_csv()
             messagebox.showinfo(title="Database Exported", message="Your database was exported.")
        else:
             messagebox.showinfo(title="Canceled Export", message="Your database was not exported.")

    # ================================= data section functionalities =================================

      # delete all data from database
    def delete_all_data(self) -> None:
        answer = messagebox.askyesno(title="Delete All Records", 
                                  message="""Would you like to delete all of your records? 
                                  """)
        if answer == True:
            answer_2 = messagebox.askyesno(title="Delete All Records",
                                      message="This action cannot be undone. Would you still like to continue?")
            if answer_2 == True:
                messagebox.showinfo(title="All Records Deleted", message="All your records have been deleted.")
                Database.delete_all_data()
                self.remove_all()
            else:
                messagebox.showinfo(title="Records Not Deleted", message="Your records were not deleted.")
        else:
            messagebox.showinfo(title="Records Not Deleted", message="Your records were not deleted.")

      # function to select record
    def select_record(self, event, entry_dic: Dict[str, Any], *args: List[str]) -> None:
        # change to normal state in case of later bind
        for entry in entry_dic.values():
            entry.configure(state="normal")
            entry.delete(0,tk.END)
        # grab records
        selected=self.my_tree.focus()
        # grab record value
        values=self.my_tree.item(selected,'values')
        count=0
        
        # insert into entry box
        for name,entry in entry_dic.items():
            if name == "id_entry" or name == "age_entry" or name == "long_entry" or name == "history_id":
                entry.insert(count,values[count])
                entry.configure(state="disabled") 
                count+=1
            else:
                entry.insert(count,values[count])
                count+=1
                
  # remove all records from treeview
    def remove_all(self) -> None:
        for record in self.my_tree.get_children():
            print(record)
            self.my_tree.delete(record)

    def delete_record(self,entry_dic: Dict[str, Any]) -> None:
        to_delete_or_not = messagebox.askyesno("Delete Record", "Are you sure you would like to delete this record?")
        if to_delete_or_not == 1:
            selected = self.my_tree.focus()
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
          
            self.db.delete_row(id_value)
            messagebox.showinfo("Deleted!", "Your record has been deleted.")
        else:
            messagebox.showinfo("Not Deleted.", "Your record was not deleted.")

    def update_record(self,entry_dic: Dict[str, Any]) -> None:
        selected=self.my_tree.focus()

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

        to_update_or_not = messagebox.askyesno("Update Record", "Are you sure you would like to update this record?")
        if to_update_or_not == 1:
            self.db.update_table(
            value_dic
          )
            messagebox.showinfo("Data Updated", "Your transaction has been updated.")
        else:
            messagebox.showinfo("Not Updated.", "Your record was not updated.")

    # standardized function to get database info
    def query_database(self,func: Callable) -> None:
      count=0
      records=func()
      for record in records:
          rec=[record[i] for i in range(len(record))]
          rec=tuple(rec)

          if count % 2 == 0:
            self.my_tree.insert(parent='',index='end',text="",values=rec,tags=('evenrow',))
          else:
            self.my_tree.insert(parent='',index='end',text="",values=rec,tags=('oddrow',))
          count += 1

      # ================================= main functionalities =================================

    def on_closing(self) -> None:
        save_previous_setting(self.set_settings_resource_path, self.transition_menu.get(), self.appearance_options.get() )
        self.destroy()
      
    def refresh_page(self) -> None:
        value = self.transition_menu.get()
        self.main_view.destroy()
        self.data_frame.destroy()
        self.button_frame.destroy()
        self.gb.refresh_database()
        self.tab_selection(value)

    # ================================= appearance functionalities =================================
    def change_appearance_mode(self, new_appearance_mode: str) -> None:
        '''method that allows for treeview to style match setting'''
        customtkinter.set_appearance_mode(new_appearance_mode)
        
        if new_appearance_mode == "System":
            new_appearance_mode = darkdetect.theme()
        
        # for the widgets that are not affected by customtkinter
        if new_appearance_mode == "Dark":
            self.style.configure("Treeview",
                            background="#2a2d2e",
                            foreground="white",
                            rowheight=25,
                            fieldbackground="#515A5A",
                            bordercolor="#343638",
                            borderwidth=0)
            self.style.map('Treeview', background=[('selected', '#AF7AC5')])

            self.style.configure("Treeview.Heading",
                            background="#424949",
                            font=('Arial Bold', 12),
                            foreground="white",
                            relief="flat")
            self.style.map("Treeview.Heading",
                        background=[('active', '#515A5A')])
            
            self.style.configure("arrowless.Vertical.TScrollbar", troughcolor="#4A235A", bd=0,bg="#9B59B6")

            # create strip row tags
            self.my_tree.tag_configure('oddrow',background='#565b5e')
            self.my_tree.tag_configure('evenrow',background='#5B2C6F') # purple
            
        elif new_appearance_mode == "Light":
            self.style.configure("Treeview",
                            background="#2a2d2e",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="#343638",
                            bordercolor="#343638",
                            borderwidth=0)
            self.style.map('Treeview', background=[('selected', '#F1948A')])

            self.style.configure("Treeview.Heading",
                            background="#F2F3F4",
                            foreground="black",
                            font=('Arial Bold', 12),
                            relief="flat")
            self.style.map("Treeview.Heading",
                        background=[('active', '#3484F0')])
            
            self.style.configure("arrowless.Vertical.TScrollbar", troughcolor="#FDEDEC")
            # create strip row tags
            self.my_tree.tag_configure('oddrow',background='white')
            self.my_tree.tag_configure('evenrow',background='#FADBD8')

    # get it so that the appearance changes automatically on System for widgets that are not supported by custom tkinter
    def delay_appearance(self):    
        '''method that allows treeview to auto-transition style on the system style setting'''
        self.after(500, self.delay_appearance)   
        if self.appearance_options.get() == "System":  
            self.change_appearance_mode(self.appearance_options.get())

if __name__ == "__main__":
    app = App()
    # allow for treeview to auto change depending on the os appearance
    app.after(500, app.delay_appearance)
    app.mainloop()
    app.gb.refresh_database()