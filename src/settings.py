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

def setTrigger(name):
    global parsed
    get()
    f = open("./mobile/server/settings.json", "w")
    parsed[name] = not(parsed[name])
    json.dump(parsed, f, indent=4)
    f.close()
    return