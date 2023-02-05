import json


def get_previous_setting(json_path: str, transition_menu: bool = False, appearance_option: bool = False) -> str:
  with open(json_path) as f:
    data = json.load(f)
  if transition_menu == True:
    return data["transitionMenu"]
  elif appearance_option == True:
    return data["appearanceOption"]

# save the previous setting before exiting the program
def save_previous_setting(json_path: str, transition_menu: str, appearance_option: str) -> None:
  with open(json_path, "r") as f:
    data = json.load(f)
  data["transitionMenu"] = transition_menu
  data["appearanceOption"] = appearance_option
  with open(json_path, "w") as f:
    json.dump(data, f, indent= 2)