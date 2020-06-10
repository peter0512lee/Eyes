import requests
import urllib
import json
import os

from urllib.request import urlretrieve

apiURL = 'http://iot.cht.com.tw/apis/CHTIoT/tts/v1/ch/synthesis'

#my_data = {'inputText': ''cm, 'outputName': 'out.mp3'} 
#r = requests.post(apiURL, data = my_data)
#f = json.loads(r.text)['file']

#urlretrieve(f, "out.mp3") 
os.system("aplay out.mp3")

