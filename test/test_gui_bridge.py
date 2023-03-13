from src.gui_bridge import check_correct_values
from pathlib import Path
import sys
# add path to so python can retrieve packages
path = str(Path(".").parent.absolute())
sys.path.insert(0, path)

import unittest

entry_dic_pass = {
    "timestamp": "2014-07-03",
    "amount": 10,
    "price_USD": 10.00,
    "security_name": "S&P500",
    "security_ticker": "SPY",
    "institution_name": "Computershare",
    "transaction_type": "Acquire"
}

entry_dic_fail_timestamp = {
    "timestamp": "2014-0C-03",
    "amount": 10,
    "price_USD": 10.00,
    "security_name": "S&P500",
    "security_ticker": "SPY",
    "institution_name": "Computershare",
    "transaction_type": "Acquire"
}

entry_dic_fail_amount = {
    "timestamp": "2014-07-03",
    "amount": "C",
    "price_USD": 10.00,
    "security_name": "S&P500",
    "security_ticker": "SPY",
    "institution_name": "Computershare",
    "transaction_type": "Acquire"
}

entry_dic_fail_price = {
    "timestamp": "2014-07-03",
    "amount": 10,
    "price_USD": "C",
    "security_name": "S&P500",
    "security_ticker": "SPY",
    "institution_name": "Computershare",
    "transaction_type": "Acquire"
}


entry_dic_fail_name = {
    "timestamp": "2014-07-03",
    "amount": 10,
    "price_USD": 10,
    "security_name": "",
    "security_ticker": "SPY",
    "institution_name": "Computershare",
    "transaction_type": "Acquire"
}

entry_dic_fail_to_institution = {
    "timestamp": "2014-07-03",
    "amount": 10,
    "price_USD": 10,
    "security_name": "S&P500",
    "security_ticker": "SPY",
    "institution_name": "Computershare",
    "from_institution": "Computershare",
    "to_institution_name": "Computershare",
    "transaction_type": "Transfer"
}


class TestGuiFunctionalities(unittest.TestCase):
    '''class to test gui functionalities'''

    # ================================= tests: insert _ into database functionalities =================================

    # check for the syntax of transaction entry
    def test_check_correct_values(self):

        self.assertTrue(check_correct_values(entry_dic_pass))

        self.assertRaises(ValueError, check_correct_values, entry_dic_fail_timestamp)

        self.assertRaises((ValueError,TypeError), check_correct_values, entry_dic_fail_amount)

        self.assertRaises((ValueError,TypeError), check_correct_values, entry_dic_fail_price)

        self.assertRaises(ValueError, check_correct_values, entry_dic_fail_name)

        self.assertRaises(ValueError, check_correct_values, entry_dic_fail_to_institution)


if __name__ == "__main__":
    unittest.main()