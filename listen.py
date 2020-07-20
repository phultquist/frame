import json
import requests
import base64
from PIL import ImageFile

image_file= open('./samples/newslaves.m4a',"rb")
image_data_binary = image_file.read()
image_data = (base64.b64encode(image_data_binary))

data = {
    'return': 'apple_music,spotify',
    'api_token': '0295a1c0139a030849dd81359d92122a',
    'audio': image_data
}

# print(image_data)

result = requests.post('https://api.audd.io/', data=data)


response = json.loads(result.text)
print(response['result']['title'])
print(response['result']['artist'])
print(response['result']['spotify']['album']['images'][0]['url'])
