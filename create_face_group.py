#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2019, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# create_face_group.py
# Create face group in CHT IoT Platform
#
# Author : sosorry
# Date   : 2019/08/07
# Usage  : python3 create_face_group.py

import requests
import json
import base64
import configparser

config = configparser.ConfigParser()
config.read('cht.conf')
apiKey = config.get('demo-key', 'apiKey')

print(apiKey)

server = 'http://iot.cht.com.tw/apis/CHTIoT'
apiURL = 'https://iot.cht.com.tw/apis/CHTIoT/face/v2/FaceGroup'

headers = {
    "X-API-KEY": apiKey,
    "Content-Type": "application/json",
}

data = {
    "groupName":"He",
    "groupMetadata":"He"
}

response = requests.post(apiURL, headers=headers, data=json.dumps(data))
print(response.text)



