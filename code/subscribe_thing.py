import paho.mqtt.client as mqtt

host = "iot.cht.com.tw"

topic = '/v1/device/' + '18332286480' + '/sensor/' + 'person' + '/rawdata'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {}".format(str(rc)))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(str(msg.payload)[82:len(str(msg.payload))-4])

client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message

user, password = 'PKH4BB3Y714ZH7KXZS', 'PKH4BB3Y714ZH7KXZS' 
client.username_pw_set(user, password) 
client.connect(host, 1883, 60)

client.loop_forever()

