import exceptions
import ip
import index
import time

lasturl = exceptions.exc_object('off')

def job():
    iplist = list(ip.ip)
    for i in range(len(iplist)):
        show('errorcode_'+str(iplist[i]))
        time.sleep(1)
        show('off')
        time.sleep(0.5)
    show('error')
    time.sleep(2)
    show('off')

def show(code):
    ref = exceptions.exc_object(str(code))
    px = index.manipulate(ref.get('image_url'))
    index.update_pixels(px)

job()