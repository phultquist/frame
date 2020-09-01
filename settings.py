import os
import json

# cur_path = os.path.dirname(__file__)
# new_path = os.path.relpath('./')
def get():
    f = open("./mobile/server/settings.json", "r")
    content = f.read()
    # print(content)
    parsed = json.loads(content)
    print(parsed["brightness"])
    f.close()
    return parsed

# get()