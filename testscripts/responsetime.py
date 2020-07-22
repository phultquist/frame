import requests
from datetime import datetime

small = 'https://i.scdn.co/image/67407947517062a649d86e06c7fa17670f7f09eb'
big = 'https://i.scdn.co/image/d3acaeb069f37d8e257221f7224c813c5fa6024e'

s = datetime.now()

count = 100

for i in range(count):
    imgresp = requests.get(small)
print('Time to get '+str(count)+' of small: ' + str(datetime.now() - s))

b = datetime.now()

for i in range(count):
    imgresp = requests.get(big)
print('Time to get '+str(count)+' of big: ' + str(datetime.now() - b))
