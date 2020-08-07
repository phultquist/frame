PAUSED_IMAGE = 'https://i.ibb.co/8NYjgQy/Group-2-1.png'
ERROR_IMAGE = 'https://raw.githubusercontent.com/phultquist/smart-album-cover/spotify-listener/assets/error.png'

def exc_object(error, raw="reload for updates"):
    imgurl = PAUSED_IMAGE
    if error:
        imgurl = ERROR_IMAGE
    return {
        "image_url": imgurl,
        "name": 'Not Playing',
        "fullsize_image_url": imgurl,
        "artist_names": 'Paused/Stopped',
        "raw": raw
    }
