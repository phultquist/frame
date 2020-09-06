import os
import json

# cur_path = os.path.dirname(__file__)
# new_path = os.path.relpath('./')
parsed = ''
def get():
    global parsed
    f = open("./mobile/server/settings.json", "r")
    content = f.read()
    # print(content)
    try:
        parsed = json.loads(content)
    except:
        pass
    
    # print(parsed["brightness"])
    f.close()
    return parsed

# get()