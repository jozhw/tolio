'''imports the insert_csv method from utils'''
from tkinter import filedialog
from utils import insert_csv


def to_import_csv() -> None:
    '''class method that opens a filedialog to select a .csv to import'''
    import_file_name = filedialog.askopenfilename(title="Select A CSV File", filetypes=(("csv files", "*.csv"),))
    if bool(import_file_name):
        insert_csv(import_file_name)