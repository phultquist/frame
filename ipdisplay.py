import exceptions
import ip
import index
import time

lasturl = exceptions.exc_object('off')

def job():
    iplist = list(ip.ip)
    for i in range(len(iplist)):
        show(iplist[i])
        time.sleep(2)
    # show(1)
    # time.sleep(1)
    # show(2)
    # time.sleep(1)
    # show(3)

def show(code):
    ref = exceptions.exc_object('errorcode_'+str(code))
    px = index.manipulate(ref.get('image_url'))
    index.update_pixels(px)
job()