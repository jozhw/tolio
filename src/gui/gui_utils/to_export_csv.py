'''imports the export_csv method from utils'''
from tkinter import messagebox
from utils import export_csv

def to_export_csv() -> None:
    '''class method that opens a filedialog to select where to export .csv'''
    answer = messagebox.askyesno(title="Export Database",
                                message="Would you like to export the database to a .csv file?")
    if answer == True:
            export_csv()
            messagebox.showinfo(title="Database Exported", message="Your database was exported.")
    else:
            messagebox.showinfo(title="Canceled Export", message="Your database was not exported.")