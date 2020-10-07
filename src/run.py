# This script uses a running while loop to run index.py every so often
# Totally honestly, I am not super proud of how this is done, but it must be done.

import time
import index
import schedule
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
import exceptions
import publiship

# initializes the last song so that way there is no error
last_song = exceptions.exc_object('off')
num_runs = 0

def job():
    global last_song
    global num_runs
    # print('job called')
    num_runs += 1
    last_song = index.main(last_song.get('image_url'))

def send_ip_to_server():
    publiship.send_ip_to_server()

refresh_interval = 0.5 # seconds per refresh
schedule.every(refresh_interval).seconds.do(job)

schedule.every(1).minutes.do(send_ip_to_server)

def music():
    while 1:
        schedule.run_pending()

if __name__=='__main__':
    musicThread = threading.Thread(target=music)
    musicThread.start()