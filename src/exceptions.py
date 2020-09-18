PAUSED_IMAGE = 'assets/paused.png'
ERROR_IMAGE = 'assets/error.png'
OFF_IMAGE = 'assets/off.png'
# TIME_IMAGE = 'assets/time.png'

def exc_object(type, raw="reload for updates"):
    imgurl = PAUSED_IMAGE
    force_reload = False

    if type=='error':
        imgurl = ERROR_IMAGE
    elif type=='off':
        imgurl = OFF_IMAGE
    elif type=='paused':
        imgurl = PAUSED_IMAGE
    elif type.startswith('time'):
        # imgurl = TIME_IMAGE
        imgurl = "time//"+raw
    elif type.startswith('errorcode'):
        imgurl = 'assets/codes/'+type.split('_')[1] + '.png'
        
    return {
        "image_url": imgurl,
        "name": 'Not Playing',
        "fullsize_image_url": imgurl,
        "artist_names": '--',
        "raw": raw,
        "ready": False,
        "playing": False,
        "force": force_reload,
        "exception": True,
        "type": type
    }
