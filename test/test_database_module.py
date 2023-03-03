

from pathlib import Path
import sys
import os
import sqlite3

path = str(Path(".").parent.absolute())
sys.path.insert(0, path)


import unittest

from src.database import Database

# to pass run pytest instead of this test individually

class TestDatabaseModule(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabaseModule, self).__init__(*args, **kwargs)
        # create a directory for where the local database will be stored if not present
        target_dir = os.path.expanduser("files/data/test_portfolio.db")
        os.remove(target_dir)

        self.connection = sqlite3.connect(target_dir)
        self.cur = self.connection.cursor()

        self.Database = Database(db_path = target_dir, sql_path="test/queries/test_py_db_query.sql")


# ============================== test: get methods ==============================

    def test_get_table_values(self):
        security_name_list = self.Database.get_table_value("security_name")
        self.assertListEqual(security_name_list, ["S&P500", "Tesla"])

    def test_get_transactions_table(self):
        get_transactions = self.Database.get_transactions_table()
        self.assertIn((1, "S&P500", "SPY", "Fidelity", "2022-01-01", "Acquire", None, None, 100, 10, 1, 10), get_transactions)

    def test_get_institutions_held_table(self):
        get_institutions_held_table = self.Database.get_institutions_held_table()
        self.assertIn(("Fidelity", "Tesla", 10, 100, 10, 10, 0, 0 ), get_institutions_held_table)

    def test_get_security_table(self):
        get_security_table = self.Database.get_security_table()
        self.assertIn(("Tesla", "TSLA", 20, 100, 5, 20, None, None), get_security_table)

    def test_get_table_value(self):
        security_name = self.Database.get_table_value("security_name")
        self.assertIn("Tesla", security_name)

  # ============================== test: insert methods ==============================

    def test_insert_acquire_or_dipose(self):
        entry_dic = {
            "timestamp": "2014-07-03",
            "amount": 10.0,
            "price_USD": 2000.00,
            "security_name": "Tesla",
            "security_ticker": "TSLA",
            "institution_name": "Computershare",
            "transaction_abbreviation": "A" }
        self.Database.insert_acquire_or_dispose(entry_dic)
        most_recent = self.cur.execute("""SELECT transaction_id, security_id, institution_id, timestamp, transaction_abbreviation, amount, price_USD 
        FROM transactions
        WHERE transaction_id = (SELECT MAX(transaction_id) FROM transactions);""").fetchall()[0]
        self.assertEqual((4, 2, 2, '2014-07-03', 'A', 10.0, 2000.0), most_recent)

if __name__ == "__main__":
    unittest.main()