from pathlib import Path
import sys
# add path to so python can retrieve packages
path = str(Path(Path("gui_functionalities.py").parent.absolute()))
sys.path.insert(0, path)

import unittest


from src import gui_functionalities

class TestGuiFunctionalities(unittest.TestCase):

# ================================= tests: insert _ into database functionalities =================================

  # when inserting into transaction, change the sign according to transaction type
  def test_change_value_sign(self):
        trans_type = ["A", "D"]
        self.assertEqual(gui_functionalities.GuiFunction().change_value_sign(trans_type[0], 10, 10), (10, 10))
        self.assertEqual(gui_functionalities.GuiFunction().change_value_sign(trans_type[1], -10, -10), (-10,-10))
        self.assertEqual(gui_functionalities.GuiFunction().change_value_sign(trans_type[1], 10, -10), (-10,-10))
        self.assertEqual(gui_functionalities.GuiFunction().change_value_sign(trans_type[1], -10, 10), (-10,-10))
    
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


        self.assertTrue(gui_functionalities.GuiFunction().check_correct_values(entry_dic_pass))
        
        self.assertRaises(ValueError, gui_functionalities.GuiFunction().check_correct_values, entry_dic_fail_timestamp)

        self.assertRaises((ValueError,TypeError), gui_functionalities.GuiFunction().check_correct_values, entry_dic_fail_amount)

        self.assertRaises((ValueError,TypeError), gui_functionalities.GuiFunction().check_correct_values, entry_dic_fail_price)

        self.assertRaises(ValueError, gui_functionalities.GuiFunction().check_correct_values, entry_dic_fail_name)

        self.assertRaises(ValueError, gui_functionalities.GuiFunction().check_correct_values, entry_dic_fail_to_institution, transfer = True)

 # ================================= tests: previous settings =================================
    
  # get values from json file set_settings.json
  def test_get_previous_setting(self):
        self.assertIsNotNone(gui_functionalities.GuiFunction().get_previous_setting(gui_functionalities.GuiFunction().resource_path("config/set_settings.json"),transition_menu=True))
        self.assertIsNotNone(gui_functionalities.GuiFunction().get_previous_setting(gui_functionalities.GuiFunction().resource_path("config/set_settings.json"), appearance_option=True))


 # ================================= tests: General functionalities =================================

  # standardize the values for the name, ticker, and institution name
  def test_edit_entry_dic(self):
    entry_dic_pass = {
            "timestamp": "2014-07-03",
            "amount": 10,
            "price_USD": 10.00,
            "name": "S&P500",
            "ticker": "SPY",
            "institution_name": "Computershare"
        }

    entry_dic_pass_2 = {
            "timestamp": "2014-07-03",
            "amount": 10,
            "price_USD": 10.00,
            "name": "Tesla",
            "ticker": "TSLA",
            "institution_name": "Computershare"
        }

    entry_dic_adjust_2 = {
        "timestamp": "2014-07-03",
        "amount": 10,
        "price_USD": 10.00,
        "name": "TeSla",
        "ticker": "TSLA",
        "institution_name": "Computershare"
    }

    entry_dic_spaces_adjust = {
        "timestamp": "2014-07-03",
        "amount": 10,
        "price_USD": 10.00,
        "name": "TeSla motors & s & p500",
        "ticker": "TSLA",
        "institution_name": "Computershare"
    }

    entry_dic_spaces_correct = {
        "timestamp": "2014-07-03",
        "amount": 10,
        "price_USD": 10.00,
        "name": "Tesla Motors & S & P500",
        "ticker": "TSLA",
        "institution_name": "Computershare"
    }


    self.assertEqual(gui_functionalities.GuiFunction().edit_entry_dic(entry_dic_pass), entry_dic_pass)
    self.assertEqual(gui_functionalities.GuiFunction().edit_entry_dic(entry_dic_pass_2), entry_dic_pass_2)
    self.assertEqual(gui_functionalities.GuiFunction().edit_entry_dic(entry_dic_adjust_2), entry_dic_pass_2)
    self.assertEqual(gui_functionalities.GuiFunction().edit_entry_dic(entry_dic_spaces_adjust), entry_dic_spaces_correct)
    


if __name__ == "__main__":
  unittest.main()
