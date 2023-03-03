import tkinter as tk
import customtkinter
import darkdetect

class Appearance(customtkinter.CTkFrame):
    def __init__(self, master, my_tree, style):
        super().__init__(master)
        self.master = master
        self.my_tree = my_tree
        self.style = style

    def change_appearance_mode(self, new_appearance_mode: str) -> None:
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
            self.style.map("Treeview.Heading", background=[('active', '#515A5A')])

            self.style.configure("arrowless.Vertical.TScrollbar",
                                 troughcolor="#4A235A",
                                 bd=0,
                                 bg="#9B59B6")

            # create strip row tags
            self.my_tree.tag_configure('oddrow', background='#565b5e')
            self.my_tree.tag_configure('evenrow', background='#5B2C6F') # purple

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
            self.my_tree.tag_configure('oddrow', background='white')
            self.my_tree.tag_configure('evenrow', background='#FADBD8')

    def delay_appearance(self):
        '''method that allows treeview to auto-transition style on the system style setting'''
        self.after(500, self.delay_appearance)
        if self.master.appearance_options.get() == "System":
            self.change_appearance_mode(self.master.appearance_options.get())


