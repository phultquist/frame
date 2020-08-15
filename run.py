# This script uses a running while loop to run index.py every so often
# Totally honestly, I am not super proud of how this is done, but it must be done.

import time
import index
import schedule
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
import exceptions
import webbrowser

# initializes the last song so that way there is no error
last_song = exceptions.exc_object('off')
num_runs = 0

def job():
    global last_song
    global num_runs
    num_runs += 1
    try:
        last_song = index.main(last_song.get('image_url'))
    except Exception as e:
        print('############### Exception in job ################')
        print(e)
        time.sleep(5)

refresh_rate = 0.5 # seconds per refresh
schedule.every(refresh_rate).seconds.do(job)

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  print("Log server started: http://localhost:8000")
  webbrowser.open('http://localhost:8000/', new=0)
  server_address = ('localhost', 8000)
  httpd = server_class(server_address, handler_class)
  httpd.serve_forever()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        message = "<html><body><img src='"+last_song.get('fullsize_image_url')+"'><h1>"+last_song.get('name')+"</h1><h2>"+last_song.get('artist_names')+"</h2><h3>Reload for changes</h3><p>"+last_song.get('raw')+"</p></body></html>"
        self.wfile.write(message.encode())

def server():
    run(handler_class=Handler)

def music():
    while 1:
        schedule.run_pending()

if __name__=='__main__':
    musicThread = threading.Thread(target=music)
    musicThread.start()

    if (not index.setLeds) and (index.run_server):
        serverThread = threading.Thread(target=server)
        print("Play a song to get started")
        while (not last_song.get("ready")):
            pass
        serverThread.start()
