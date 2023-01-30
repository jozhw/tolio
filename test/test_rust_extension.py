
import unittest, sqlite3, os

import tolio

class TestRustExtension(unittest.TestCase):

  """
  Note in order to access the package, must in the command line use maturin build and then go into the target/wheels folder and 
  install the .whl file with pip3 install .whl
  
  """

  # Testing ext_db works
  def execute_sql_script(self, filename):
    file_open = open(filename, 'r')
    sql_file = file_open.read()
    file_open.close()

    sql_commands = sql_file.split(";")

    for command in sql_commands:
      try:
        self.cur.execute(command)
      except sqlite3.OperationalError as msg:
        print("Command skipped: ", msg)
        
  def test_insert_into_all_shares(self):

    target_dir = os.path.expanduser("test/db_test_portfolio.db")
    os.remove(target_dir)

    self.connection = sqlite3.connect(target_dir)
    self.cur = self.connection.cursor()
    self.execute_sql_script(os.path.expanduser("test/test_rs_db_query.sql"))

    self.connection.commit()

    tolio.insert_into_all_shares(target_dir)

    after_split_total = self.cur.execute("SELECT COUNT(amount) FROM all_shares WHERE security_id = ?;", '1').fetchone()[0]
    after_split_total_price = self.cur.execute("SELECT SUM(price_USD) FROM all_shares WHERE security_id =?;", '1').fetchone()[0]

    self.assertEqual(after_split_total, 6)
    self.assertEqual(after_split_total_price, 300)

   
   







if __name__ == "__main__":
    unittest.main()