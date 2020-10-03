# This script uses a running while loop to run index.py every so often
# Totally honestly, I am not super proud of how this is done, but it must be done.

import time
import index
import schedule
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
import exceptions
import ip
import requests
from secrets import FRAME_ID

# initializes the last song so that way there is no error
last_song = exceptions.exc_object('off')
num_runs = 0
stored_ip_address = ''

def job():
    global last_song
    global num_runs
    # print('job called')
    num_runs += 1
    last_song = index.main(last_song.get('image_url'))

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
    # requests.get()

refresh_interval = 0.5 # seconds per refresh
schedule.every(refresh_interval).seconds.do(job)

schedule.every(1).minutes.do(send_ip_to_server)

def music():
    send_ip_to_server()
    while 1:
        schedule.run_pending()

if __name__=='__main__':
    musicThread = threading.Thread(target=music)
    musicThread.start()