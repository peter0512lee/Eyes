import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import configparser

import urllib
import requests
import os

from urllib.request import urlretrieve

from subprocess import call

import subprocess

import random

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

config = configparser.ConfigParser()
config.read('cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
sensorId   = config.get('device-key', 'sensorId')
thingId    = config.get('device-key', 'thingId')
cameraId   = config.get('device-key', 'cameraId')
helpId   = config.get('device-key', 'helpId')

host = "iot.cht.com.tw"

topic = '/v1/device/' + deviceId + '/rawdata'
print(topic)

user, password = projectKey, projectKey

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

TRIG = 23
ECHO = 24
BUTTON = 17
BUTTON_HELP = 26

print ("Distance Measurement In Progress")

#######################play sound#########################       
            
apiURL = 'http://iot.cht.com.tw/apis/CHTIoT/tts/v1/ch/synthesis'

text = 'push button' 
            
my_data = {'inputText': text, 'outputName': 'button.mp3'} 
r = requests.post(apiURL, data = my_data)
f = json.loads(r.text)['file']

urlretrieve(f, "button.mp3") 
os.system("aplay button.mp3")

##########################################################

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(BUTTON_HELP, GPIO.IN)

prev_input = 1
i = 0

try:
    while True:
            
    
        if GPIO.input(BUTTON_HELP) == False:
        
            print("BUTTON_HELP")

            value = random.randint(0,50)
            t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

            payload = [{"id":helpId,"value":[value], "time":t}]
            print(payload)
            client.publish(topic, "%s" % ( json.dumps(payload) ))

            time.sleep(0.5)
            
            value = 51
            t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))
        
            payload = [{"id":helpId,"value":[value], "time":t}]
            print(payload)
            client.publish(topic, "%s" % ( json.dumps(payload) ))
        
            time.sleep(0.5)

        else:

            input_state = GPIO.input(BUTTON)

            if (input_state == False):
            
                GPIO.output(TRIG, False)
    
                
                print ("Waiting For Sensor To Settle")
                time.sleep(1)
                
                GPIO.output(TRIG, True)
                time.sleep(0.000001)
                GPIO.output(TRIG, False)
                
                while GPIO.input(ECHO) == 0:
                    pulse_start = time.time()
                    
                while GPIO.input(ECHO) == 1:
                    pulse_end = time.time()
                    
                pulse_duration = pulse_end - pulse_start
                
                distance = pulse_duration * 17150
                
                distance = round(distance, 2)
                
                print ("Distance:", distance, "cm")

                ###########################################################

                print('take photo')
                call('fswebcam m.jpg', shell=True)

                print('move photo to darknet')
                call('mv m.jpg ../darknet/data', shell=True)

                print('move into darknet')
                os.chdir("../darknet")
                
                #####################initialization#############################
                
                things = '000000'
                t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

                payload = [{"id":"thing","value":[things], "time":t}]
                print(payload)
                client.publish(topic, "%s" % ( json.dumps(payload) ))     
                
                #####################detection###################################

                cmd = './darknet detector test cfg/voc.data cfg/yolov2-tiny-voc.cfg yolov2-tiny-voc.weights data/m.jpg'

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

                (output, err) = p.communicate()

                p_status = p.wait()
                
                print(output)
                
                print("Command output : ", output[44:len(output) - 6])
            
                print('move predictions.jpg to test')
                call('mv predictions.jpg ../test', shell=True)     
                
                print('move into test')
                os.chdir("../test")
                
                ##########################################################
                
                buffer1 = str(output[44:len(output) - 6])
                
                print(buffer1)
                
                buffer2 = "b'person'"
                
                print(buffer2)
                
                if buffer1[2:8] == "person":
                    call('python3 recognize_face_in_facegroup.py predictions.jpg', shell=True)
                    f = open('name.txt','r')
                    buffer1 = f.read()
                    #myCmd = os.popen('python3 recognize_face_in_facegroup.py test.jpg').read()
                    #print(myCmd[269:len(myCmd) - 52])
		                        
                    #print(output)
                    #print(output[285:len(output) - 37])
                    
 
                #######################play sound#########################       
                            
                apiURL = 'http://iot.cht.com.tw/apis/CHTIoT/tts/v1/ch/synthesis'
                
                text = buffer1 + str(distance) + 'centimeter ' + 'ahead' 
                            
                my_data = {'inputText': text, 'outputName': 'out.mp3'} 
                r = requests.post(apiURL, data = my_data)
                f = json.loads(r.text)['file']

                urlretrieve(f, "out.mp3") 
                os.system("aplay out.mp3")
                
                ##################upload distance to IoT platform##########
                
                dist = str(int(distance))
                t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

                payload = [{"id":sensorId,"value":[dist], "time":t}]
                print(payload)
                client.publish(topic, "%s" % ( json.dumps(payload) ))
                
                ##################upload thing to IoT platform##########
                
                
                things = str(output[44:len(output) - 6])
                t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

                payload = [{"id":"thing","value":[things], "time":t}]
                print(payload)
                client.publish(topic, "%s" % ( json.dumps(payload) ))
                
                
                ####################upload photo to IoT platform#########            
                
                apiURL = 'http://iot.cht.com.tw/iot/v1/device/' + deviceId + '/snapshot'
                
                headers = { 
                    "CK":projectKey,
                    "accept":"application/json",
                }   
                
                files = {"img": ("test", open("predictions.jpg", "rb"), "image/jpeg"), "meta":(None, json.dumps({"id":cameraId,"value":["webcam"]}), 'application/json')}
                
                response = requests.post(apiURL, files=files, headers=headers)
                print(response.text)

                ########################################################
               
                
                prev_input = input
                
                time.sleep(0.05)

except KeyboardInterrupt:  
    
    print("STOP")
  
except:  
    
    print("Other error or exception occurred!" )
  
finally:  

    GPIO.cleanup()


