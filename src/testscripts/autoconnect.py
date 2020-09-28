import ip
import requests

FRAME_ID = 'addison-test'

stored_ip_address = ''

def send_ip_to_server():
    global stored_ip_address
    #the ip is used in the app
    latest_ip_address = ip.get_ip_address()
    if not (latest_ip_address == stored_ip_address):
        ip_address_url = "http://"+latest_ip_address+":3000/"

        # the code for this is not open source. It basically just stores the global and local ip
        r = requests.get("https://patrick.today/frame/set", params={'ip': ip_address_url, 'frameId': FRAME_ID})

        if r.status_code == 200:
            # successful update
            print("global ip updated")
            pass
        else:
            print("there was an error updating the global ip")
        
        stored_ip_address = latest_ip_address