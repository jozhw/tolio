from pathlib import Path
import sys
# add path to so python can retrieve packages
path = str(Path(".").parent.absolute())
sys.path.insert(0, path)


import unittest

from src.utils import StandardizeEntry

class TestStandardizedEntries(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestStandardizedEntries, self).__init__(*args, **kwargs)
        ###################### corrected values ########################
        self.correct_acquire_entry_dic = {
            "timestamp": "2014-07-03",
            "amount": 10.0,
            "price_USD": 10.00,
            "name": "Tesla Motors & S & P500",
            "ticker": "TSLA",
            "institution_name": "Computershare",
            "transaction_type": "A"
        }

        self.correct_dispose_entry_dic = {
                "timestamp": "2014-07-03",
                "amount": -10.0,
                "price_USD": -10.00,
                "name": "Tesla",
                "ticker": "TSLA",
                "institution_name": "Computershare",
                "transaction_type": "D"
            }

        self.correct_regex_entry_dic = {
            "timestamp": "2014-07-03",
            "amount": 10.0,
            "price_USD": 10.00,
            "name": "Tesla Motors & S & P500",
            "ticker": "TSLA",
            "institution_name": "Computershare",
            "transaction_type": "A"


        }

        ###################### incorrected values ########################
        self.acquire_entry_dic = {
            "timestamp": "2014-07-03",
            "amount": -10.00,
            "price_USD": -10.00,
            "name": "Tesla Motors & S & P500",
            "ticker": "TSLA",
            "institution_name": "Computershare",
            "transaction_type": "Acquire"
        }

        self.dispose_entry_dic = {
                "timestamp": "2014-07-03",
                "amount": 10.00,
                "price_USD": 10.00,
                "name": "Tesla",
                "ticker": "TSLA",
                "institution_name": "Computershare",
                "transaction_type": "Dispose"
        }

        self.regex_entry_dic = {
            "timestamp": "2014-07-03",
            "amount": 10.00,
            "price_USD": 10.00,
            "name": "TEsla Motors & S & p500",
            "ticker": "TsLA",
            "institution_name": "computerShare",
            "transaction_type": "Acquire"

        }

        ###################### create class objects to be tested ########################
        self.acquire_standardize = StandardizeEntry(self.acquire_entry_dic)
        self.dispose_standardize = StandardizeEntry(self.dispose_entry_dic)
        self.regex_standardize = StandardizeEntry(self.regex_entry_dic)

    def test_regex_sub(self):
        self.assertEqual(self.regex_standardize.regex_sub(), self.correct_regex_entry_dic)


    def test_change_value_sign(self):
        self.assertEqual(self.acquire_standardize.change_value_sign(), self.correct_acquire_entry_dic)
        self.assertEqual(self.dispose_standardize.change_value_sign(), self.correct_dispose_entry_dic)

if __name__ == "__main__":
    unittest.main()