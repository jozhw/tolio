

from pathlib import Path
import sys, os

path = str(Path(".").parent.absolute())
sys.path.insert(0, path)


import unittest

from src.database import Database



class TestDatabaseModule(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestDatabaseModule, self).__init__(*args, **kwargs)
    target_dir = os.path.expanduser("files/data/test_portfolio.db")
    os.remove(target_dir)
    self.Database = Database(db_path = target_dir, sql_path="test/queries/test_py_db_query.sql")

    # perform the stock_split; the rust_extension stock split has already passed all of the tests. Any issues will be due to the parent function
    self.Database.all_shares_table()
    self.Database.stock_split(1, "S&P500", "SPY", 5, "2023-12-31", target_dir=target_dir)

# ============================== test: get methods ==============================
  
  def test_get_specific_value(self):
    
    # test security_id
    security_id = self.Database.get_specific_value(security_name="S&P500", security_ticker="SPY")
    self.assertEqual(security_id, 1)

    # test security_name and security_ticker
    security_name, security_ticker = self.Database.get_specific_value(security_id=1)
    self.assertEqual(security_name, "S&P500")
    self.assertEqual(security_ticker, "SPY")

    # test institution_name
    institution_name = self.Database.get_specific_value(institution_id=2)
    self.assertEqual(institution_name, "Computershare")

    # test institution_id
    institution_id = self.Database.get_specific_value(institution_name="Computershare")
    self.assertEqual(institution_id, 2)
  
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
  
  def test_get_specific_value(self):
    security_name = self.Database.get_specific_value(security_id=1)
    self.assertEqual(("S&P500", "SPY"), security_name)
  
  def test_get_most_recent_transaction(self):
    most_recent = self.Database.get_most_recent_transaction()
    self.assertEqual((4, 1, None, '2023-12-31', 'SS', 5.0, None, None, None, None, None), most_recent)

# ============================== test: stock_split ==============================

  def test_stock_split(self):
    # due to read-only issue the stock-split was performed at initiation
    self.assertEqual(40, len(self.Database.get_all_shares()))


    





if __name__ == "__main__":
  unittest.main()