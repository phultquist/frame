# This script uses a running while loop to run index.py every 3 seconds
# Totally honestly, I am not super proud of how this is done, but it must be done.

import time
import index
import schedule
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
import exceptions
import webbrowser

# initializes the last song so that way there is no error
last_song = exceptions.exc_object(False)

def job():
    global last_song
    last_song = index.main(last_song.get('image_url'))

schedule.every(0.5).seconds.do(job)

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

    def do_POST(self):
        print(self.rfile.read())

def server():
    run(handler_class=Handler)

def music():
    while 1:
        schedule.run_pending()

if __name__=='__main__':
    serverThread = threading.Thread(target=server)
    musicThread = threading.Thread(target=music)

    musicThread.start()
    time.sleep(2)
    serverThread.start()
