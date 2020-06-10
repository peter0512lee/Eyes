#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2019, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# add_face_to_facegroup.py
# Add face to facegroup in CHT IoT Platform
#
# Author : sosorry
# Date   : 2019/08/07
# Usage  : python3 add_face_to_facegroup.py <img>

import requests
import json
import base64
import sys
import os
import configparser

config = configparser.ConfigParser()
config.read('cht.conf')
apiKey = config.get('demo-key', 'apiKey')
server = 'http://iot.cht.com.tw/apis/CHTIoT'
apiURL = "{}{}{}".format(server, '/face/v2/FaceGroup/', 'FG201908271446409611823211')

headers = {
    "X-API-KEY": apiKey,
    "Content-Type": "application/json",
}

imagePath = sys.argv[1]
files = {"name": open(imagePath, "rb")}
fileName = os.path.basename(imagePath)
imgData = base64.b64encode(files["name"].read()).decode('utf-8')

data = {
    "imgData":imgData,
    "faceMetadata": os.path.splitext(fileName)[0]
}

response = requests.post(apiURL, headers = headers, data=json.dumps(data))
print(response.text)
