import requests
import json
import base64
import sys
import os
import configparser
import time
import paho.mqtt.client as mqtt
import numpy as np
from urllib.request import urlretrieve

from subprocess import call

import subprocess

config = configparser.ConfigParser()
config.read('cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
sensorId   = config.get('device-key', 'sensorId')
thingId    = config.get('device-key', 'thingId')
cameraId   = config.get('device-key', 'cameraId')
helpId   = config.get('device-key', 'helpId')
apiKey = config.get('demo-key', 'apiKey')
server = 'http://iot.cht.com.tw/apis/CHTIoT'
apiURL = "{}{}{}{}".format(server, '/face/v2/FaceGroup/', 'FG201908271446409611823211', '/Match')

host = "iot.cht.com.tw"

topic = '/v1/device/' + deviceId + '/rawdata'
print(topic)

user, password = projectKey, projectKey

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

headers = {
    "X-API-KEY": apiKey,
    "Content-Type": "application/json",
}

imagePath = sys.argv[1]
files = {"name": open(imagePath, "rb")}
fileName = os.path.basename(imagePath)
imgData = base64.b64encode(files["name"].read()).decode('utf-8')

data = {
    "queryData":imgData,
}

response = requests.post(apiURL, headers = headers, data=json.dumps(data))
print(response.text)

print(response.text[44:48])

score = response.text[44:48]

score = float(score)

buffer = '0'

f = open('name.txt', 'w')

if score >= 0.95 and score <= 1.00:
    buffer = 'Ho Chang Hong'
    
else:
    buffer = 'stranger'
    
f.write(buffer)
t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

payload = [{"id":"person","value":[buffer], "time":t}]
print(payload)
client.publish(topic, "%s" % ( json.dumps(payload) ))
