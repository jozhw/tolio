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
    "security_name": "Tesla Motors & S & P500",
    "security_ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "Acquire",
    "transaction_abbreviation": "A"
}

correct_dispose_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": -10.0,
    "price_USD": -10.00,
    "security_name": "Tesla",
    "security_ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_abbreviation": "D",
    "transaction_type": "Dispose"
    }

correct_regex_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": 10.0,
    "price_USD": 10.00,
    "security_name": "Tesla Motors & S & P500",
    "security_ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_abbreviation": "A",
    "transaction_type": "Acquire"


}

###################### incorrected values ########################
acquire_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": -10.00,
    "price_USD": -10.00,
    "security_name": "Tesla Motors & S & P500",
    "security_ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "Acquire"
}

dispose_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": 10.00,
    "price_USD": 10.00,
    "security_name": "Tesla",
    "security_ticker": "TSLA",
    "institution_name": "Computershare",
    "transaction_type": "Dispose"
}

regex_entry_dic = {
    "timestamp": "2014-07-03",
    "amount": 10.00,
    "price_USD": 10.00,
    "security_name": "TEsla Motors & S & p500",
    "security_ticker": "TsLA",
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