from pathlib import Path
import sys
# add path to so python can retrieve packages
path = str(Path(".").parent.absolute())
sys.path.insert(0, path)


import unittest

from src.gui_bridge import GuiBridge

class TestGuiFunctionalities(unittest.TestCase):
    gb = GuiBridge()

# ================================= tests: insert _ into database functionalities =================================

  
    # check for the syntax of transaction entry
    def test_check_correct_values(self):
        entry_dic_pass = {
            "timestamp": "2014-07-03",
            "amount": 10,
            "price_USD": 10.00,
            "name": "S&P500",
            "ticker": "SPY",
            "institution_name": "Computershare"
        }

        entry_dic_fail_timestamp = {
            "timestamp": "2014-0C-03",
            "amount": 10,
            "price_USD": 10.00,
            "name": "S&P500",
            "ticker": "SPY",
            "institution_name": "Computershare"
        }

        entry_dic_fail_amount = {
            "timestamp": "2014-07-03",
            "amount": "C",
            "price_USD": 10.00,
            "name": "S&P500",
            "ticker": "SPY",
            "institution_name": "Computershare"
        }

        entry_dic_fail_price = {
            "timestamp": "2014-07-03",
            "amount": 10,
            "price_USD": "C",
            "name": "S&P500",
            "ticker": "SPY",
            "institution_name": "Computershare"
        }

        entry_dic_fail_name = {
            "timestamp": "2014-07-03",
            "amount": 10,
            "price_USD": 10,
            "name": "",
            "ticker": "SPY",
            "institution_name": "Computershare"
        }

        entry_dic_fail_to_institution = {
            "timestamp": "2014-07-03",
            "amount": 10,
            "price_USD": 10,
            "name": "S&P500",
            "ticker": "SPY",
            "institution_name": "Computershare",
            "to_institution_name": "Computershare",
        }


        self.assertTrue(self.gb.check_correct_values(entry_dic_pass))
        
        self.assertRaises(ValueError, self.gb.check_correct_values, entry_dic_fail_timestamp)

        self.assertRaises((ValueError,TypeError), self.gb.check_correct_values, entry_dic_fail_amount)

        self.assertRaises((ValueError,TypeError), self.gb.check_correct_values, entry_dic_fail_price)

        self.assertRaises(ValueError, self.gb.check_correct_values, entry_dic_fail_name)

        self.assertRaises(ValueError, self.gb.check_correct_values, entry_dic_fail_to_institution, transfer = True)


if __name__ == "__main__":
    unittest.main()
