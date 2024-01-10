import json
import os


class ffsettings:
    def __init__(self, content=None, mod_id="example_id") -> None:
        if content == None:
            self.mod_id = mod_id
        else:
            self.mod_id = content["mod_id"]

    
    def __str__(self) -> str:
        return f"ffsettings(mod_id={self.mod_id})"
    

def is_valid_json(input_str):
    try:
        json_object = json.loads(input_str)
        return True
    except ValueError as e:
        return False
    

def ffsparser(content):
    if is_valid_json(content):
        return ffsettings(json.loads(content))
    else:
        return ffsettings()
    

def get_settings():
    settings = None
    if os.path.exists(".ffsettings"):
        readcontent = ""
        with open(".ffsettings") as file:
            readcontent = file.read()

        settings = ffsparser(readcontent)
    else:
        settings = ffsettings()
    return settings


settings = get_settings()