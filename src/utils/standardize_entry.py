import re
from typing import Any, Dict

class StandardizeEntry:
  def __init__(self, entry_dic: Dict):
    self.entry_dic = entry_dic
    self.transaction_type_dic = {
       "Acquire": "A",
       "Dispose": "D",
       "Transfer": "T"
    }
    try:
      self.entry_dic["transaction_type"] = self.transaction_type_dic[self.entry_dic["transaction_type"]]
    except:
       raise ValueError("Incorrect transaction_type.")
    

  def convert_case(self, match_obj: Any) -> str:
    if match_obj.group() is not None:
      return match_obj.group().capitalize()
    else:
      raise Exception("There were no matches.")
    
  def regex_sub(self) -> Dict:
    sub_key_list = ["name", "ticker", "institution_name", "to_institution_name"]
    for key,value in self.entry_dic.items():
      if type(value) is not str and key in sub_key_list:
        raise TypeError("Key: {key}, has a non-string value: {value}".format(key=key, value=value))
      elif key == "ticker":
         self.entry_dic[key] = value.upper()
      elif key in sub_key_list:
        self.entry_dic[key] = re.sub(r"[a-zA-z]+\s*", self.convert_case, value)
    return self.entry_dic
    
  
  def change_value_sign(self) -> Dict:
    try:
      self.entry_dic["amount"] = float(self.entry_dic["amount"])
      self.entry_dic["price_USD"] = float(self.entry_dic["price_USD"])
      # define variables for each of the above to make the code look nicer
      shares = self.entry_dic["amount"]
      price = self.entry_dic["price_USD"]
      transaction_type = self.entry_dic["transaction_type"]
    except:
      raise ValueError("Shares: {shares} or Price: {price} cannot be converted into a float.".format
                      (shares=self.entry_dic["amount"], price=self.entry_dic["price_USD"]))

    if self.entry_dic["transaction_type"] =="A" and (shares < 0 or price < 0):
      if shares < 0 and price < 0:
          self.entry_dic["amount"]=shares*(-1)
          self.entry_dic["price_USD"]=price*(-1)
      elif shares > 0 and price < 0:
          self.entry_dic["price_USD"]=price*(-1)
      elif shares < 0 and price > 0:
          self.entry_dic["amount"]=shares*(-1)
    elif transaction_type == "D" and (shares > 0 or price > 0):
      if shares > 0 and price > 0:
          self.entry_dic["amount"]=shares*(-1)
          self.entry_dic["price_USD"]=price*(-1)  
      elif shares < 0 and price > 0:
          self.entry_dic["price_USD"]=price*(-1)
      elif shares > 0 and price < 0:
          self.entry_dic["amount"]=shares*(-1)
    return self.entry_dic
  
  def return_entry_dic(self) -> Dict:
     self.entry_dic = self.regex_sub(self.entry_dic)
     self.entry_dic = self.change_value_sign(self.entry_dic)
     return self.entry_dic
  
  
  
  