import subprocess
import threading
import board
import neopixel

pixels = neopixel.NeoPixel(board.D12, 30)

pixels[0] = (0, 0, 255)

def server():
    subprocess.call(['bash', 'server.sh'])

def display():
    subprocess.call(['bash', 'display.sh'])

def site():
    subprocess.call(['bash', 'site.sh'])

server_thread = threading.Thread(target=server)
display_thread = threading.Thread(target=display)
site_thread = threading.Thread(target=site)

# server_thread.start()
display_thread.start()
# site_thread.start()