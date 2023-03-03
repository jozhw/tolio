import tolio

def insert_csv(self, csv_path: str, db_path: str = "files/data/portfolio.db") -> None:
    '''takes the path to the csv file to insert and inserts into the database'''
    tolio.insert_csv_to_db(db_path, csv_path)