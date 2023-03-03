from pathlib import Path
import sys
# add path to so python can retrieve packages
path = str(Path(".").parent.absolute())
sys.path.insert(0, path)


import unittest

from src.utils import StandardizeEntry


###################### corrected values ########################
correct_acquire_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": 10.0,
    "price_USD": 10.00,
    "name": "Tesla Motors & S & P500",
    "ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "A"
}

correct_dispose_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": -10.0,
    "price_USD": -10.00,
    "name": "Tesla",
    "ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "D"
    }

correct_regex_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": 10.0,
    "price_USD": 10.00,
    "name": "Tesla Motors & S & P500",
    "ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "A"


}

###################### incorrected values ########################
acquire_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": -10.00,
    "price_USD": -10.00,
    "name": "Tesla Motors & S & P500",
    "ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "Acquire"
}

dispose_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": 10.00,
    "price_USD": 10.00,
    "name": "Tesla",
    "ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "Dispose"
}

regex_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": 10.00,
    "price_USD": 10.00,
    "name": "TEsla Motors & S & p500",
    "ticker": "TsLA",
    "institution_name": "computerShare",
    "transaction_type": "Acquire"

}

acquire_standardize = StandardizeEntry(acquire_entry_dic)
dispose_standardize = StandardizeEntry(dispose_entry_dic)
regex_standardize = StandardizeEntry(regex_entry_dic)

class TestStandardizedEntries(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestStandardizedEntries, self).__init__(*args, **kwargs)

        ###################### create class objects to be tested ########################

    def test_regex_sub(self):
        self.assertEqual(regex_standardize.regex_sub(), correct_regex_entry_dic)


    def test_change_value_sign(self):
        self.assertEqual(acquire_standardize.change_value_sign(), correct_acquire_entry_dic)
        self.assertEqual(dispose_standardize.change_value_sign(), correct_dispose_entry_dic)

if __name__ == "__main__":
    unittest.main()