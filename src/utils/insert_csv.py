import tolio

def insert_csv(self, csv_path: str, db_path: str = "files/data/portfolio.db") -> None:
    tolio.insert_csv_to_db(db_path, csv_path)

  