'''app.py file'''
import tkinter as tk

import customtkinter
import darkdetect

from PIL import Image
from utils import ResourcePath, get_previous_setting, save_previous_setting
from database import Database
from gui_bridge import GuiBridge

from gui.window import window_add_transaction
from gui.window import window_stock_split
from gui.window import window_transfer
from gui.show import show_institutions_held_window
from gui.show import show_securities_window
from gui.show import show_stock_split_window
from gui.show import show_transaction_window
from gui.gui_utils import to_export_csv
from gui.gui_utils import to_import_csv


class App(customtkinter.CTk):
    '''class for the gui of the application'''

    # aesthetics
    style_resource_path = ResourcePath("src/assets/styling/")
    icon_resource_path = ResourcePath("src/assets/icons/")
    set_settings_resource_path = style_resource_path.resource_path("set_settings.json")
    pre_set = get_previous_setting(set_settings_resource_path, appearance_option = True)
    customtkinter.set_appearance_mode(pre_set)
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
        self.iconphoto(False, logo_path)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # not resizable
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)
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
                                                    light_image=Image.open(self.icon_resource_path.resource_path("transfer_light.png")))
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
                                                              image=self.add_icon,anchor="w")
        self.add_transaction_button.grid(row=3, column=0, pady=15, padx=20)

        # transfer institution button
        self.transfer_institution_button = customtkinter.CTkButton(self.frame_left,
                                                                   text="Transfer",
                                                                   border_color="black",
                                                                   command=self.window_transfer,
                                                                   image=self.transfer_icon,
                                                                   anchor="w")
        self.transfer_institution_button.grid(row=4, column=0, pady=15, padx=20)

        # stock split button
        self.stock_split_button = customtkinter.CTkButton(self.frame_left,
                                                          text="Stock Split",
                                                          border_color="black",
                                                          image=self.ss_icon,
                                                          anchor="w",
                                                          command=self.window_stock_split)
        self.stock_split_button.grid(row=5, column=0, pady=15, padx=20)

        # upload csv button
        self.import_file_dial_button = customtkinter.CTkButton(self.frame_left,
                                                               text="Upload CSV",
                                                               border_color="black",
                                                               image=self.documentation_icon,
                                                               anchor="w",
                                                               command=to_import_csv)
        self.import_file_dial_button.grid(row=6, column=0, pady=15, padx=20)

        # export csv button
        self.export_file_dial_button = customtkinter.CTkButton(self.frame_left,
                                                               text="Export to CSV",
                                                               border_color="black",
                                                               image=self.documentation_icon,
                                                               anchor="w",
                                                               command=to_export_csv)
        self.export_file_dial_button.grid(row=7, column=0, pady=15, padx=20)


        # set color scheme
        self.appearance_mode = customtkinter.CTkLabel(self.frame_left,
                                                text="Appearance Mode:")
        self.appearance_mode.grid(row=10,column=0,pady=0,padx=20,sticky="w")

        self.appearance_options_set = customtkinter.StringVar(value=get_previous_setting(self.set_settings_resource_path,
                                                                                         appearance_option=True))  # set initial value

        self.appearance_options = customtkinter.CTkOptionMenu(self.frame_left,
                                                              values=["System", "Dark", "Light"],
                                                              command=self.change_appearance_mode,
                                                              variable=self.appearance_options_set)
        self.appearance_options.grid(row=11, column=0, pady=10, padx=20, sticky="w")

        # ================================= data section - right frame section =================================
        # create multibutton to select different data to display
        self.transition_menu = customtkinter.CTkSegmentedButton(self.frame_right,
                                                                values=["Transactions", "Institutions Held", "Securities", "Stock Split History"]) # to add for non-beta version "Individual Shares" tab
        self.transition_menu.place(relx=0, rely=0 ,relwidth=1, anchor="nw")
        self.transition_menu.set(get_previous_setting(self.set_settings_resource_path, transition_menu=True))
        self.transition_menu.configure(command=self.tab_selection)
        self.tab_selection(get_previous_setting(self.set_settings_resource_path, transition_menu=True))

    # ================================= data section window displays =================================

    # select tab for the following four menus
    def tab_selection(self, value: str) -> None:
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
        show_transaction_window.ShowTransactionWindow(self, self.frame_right)


    # menu for showing all securities held for each particular institution
    def show_institutions_held_window(self) -> None:
        '''class method to show securities held at institutions on treeview'''
        show_institutions_held_window.ShowInstitutionsHeldWindow(self, self.frame_right)

    # menu for showing the summaries of the securities (does not include institutions)
    def show_securities_window(self) -> None:
        '''class to show the data for all the particular securities'''
        show_securities_window.ShowSecuritiesWindow(self, self.frame_right)

    # menu for showing the stock split history
    def show_stock_split_data_window(self) -> None:
        '''class method to show the stock split history on treeview'''
        show_stock_split_window.ShowStockSplitDataWindow(self, self.frame_right)

    # ================================= menu button functionalities =================================

    # click for the add transaction window to pop up
    def window_add_transaction(self) -> None:
        window_add_transaction.WindowAddTransaction(self)

    def window_transfer(self) -> None:
        '''class method that opens a new window for inputing a transfer transaction'''
        window_transfer.WindowTransfer(self)

    def window_stock_split(self) -> None:
        '''class method that opens a new window to input a stock split transaction'''
        window_stock_split.WindowStockSplit(self)

    # ================================= main functionalities =================================

    def on_closing(self) -> None:
        '''class method that is called at closing of gui that will save style settings'''
        save_previous_setting(self.set_settings_resource_path, self.transition_menu.get(), self.appearance_options.get())
        self.destroy()

    def refresh_page(self) -> None:
        '''needs development'''
        value = self.transition_menu.get()
        self.gb.refresh_database()
        self.tab_selection(value)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "System":
            new_appearance_mode = darkdetect.theme()
