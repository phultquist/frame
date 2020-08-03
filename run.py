# This script uses a running while loop to run index.py every 3 seconds
# Totally honestly, I am not super proud of how this is done, but it must be done.

import time
import index
import schedule

last_image_url = 'None'

def job():
    global last_image_url
    last_image_url = index.main(last_image_url)

schedule.every(1).seconds.do(job)

while 1:
    schedule.run_pending()