'''standardize_entry.py - houses the StandardizeEntry class'''
import re
from typing import Any, Dict

class StandardizeEntry:
    '''This class converts an entry_dic to the set standard for insertion into database'''
    def __init__(self, entry_dic: Dict):
        '''Inititalize the class with entry_dic argument'''
        self.entry_dic = entry_dic
        self.transaction_type_dic = {
            "Acquire": "A",
            "Dispose": "D",
            "Transfer": "T"
        }
        try:
            self.entry_dic["transaction_type"] = self.transaction_type_dic[self.entry_dic["transaction_type"]]
        except:
            raise ValueError("Incorrect transaction_type: {}.".format(self.entry_dic["transaction_type"]))

    def convert_case(self, match_obj: Any) -> str:
        '''Takes a match_obj and performs capitalize for the matches. This function operates
        within the regex_sub method'''
        if match_obj.group() is not None:
            return match_obj.group().capitalize()
        else:
            raise Exception("There were no matches.")

    def regex_sub(self) -> Dict:
        '''Takes self.entry_dic and modifies the value depending on key and returns
        the edited self.entry_dic'''
        sub_key_list = ["name", "institution_name", "to_institution_name"]
        self.entry_dic["ticker"] = self.entry_dic["ticker"].upper()
        for key, value in self.entry_dic.items():
            if key in sub_key_list:
                self.entry_dic[key] = re.sub(r"[a-zA-z]+\s*", self.convert_case, value)

        return self.entry_dic

    def change_value_sign(self) -> Dict:
        '''Takes self.entry_dic and changes the sign value of amount and price_usd depending on transaction type
        and returns the edited self.entry_dic'''
        try:
            self.entry_dic["amount"] = float(self.entry_dic["amount"])
            self.entry_dic["price_USD"] = float(self.entry_dic["price_USD"])
            # define variables for each of the above to make the code look nicer
            shares = self.entry_dic["amount"]
            price = self.entry_dic["price_USD"]
            transaction_type = self.entry_dic["transaction_type"]
        except:
            raise ValueError("Shares or Price cannot be converted into a float.")

        if self.entry_dic["transaction_type"] == "A":
            self.entry_dic["amount"] = abs(shares)
            self.entry_dic["price_USD"] = abs(price)

        elif transaction_type == "D":
            self.entry_dic["amount"] = abs(shares) * -1
            self.entry_dic["price_USD"] = abs(price) * -1

        return self.entry_dic

    def return_entry_dic(self) -> Dict:
        '''Implements both change_value_sign and regex_sub and returns the final edited self.entry_dic'''
        self.entry_dic = self.regex_sub(self.entry_dic)
        self.entry_dic = self.change_value_sign(self.entry_dic)
        return self.entry_dic