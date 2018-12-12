#! /usr/bin/env python3
import paho.mqtt.client as paho 
import time
import json
from pmsensor import co2sensor

broker = 'yourmqttbroker'
port = 1883
topic = 'devices/raspi/co2sensor'
state_topic = 'devices/raspi/co2sensor/state'
serial_port = '/dev/serial0'
mqtt_user = 'username'
mqtt_passwd = 'passwd'

client = paho.Client("co2sensor")
client.will_set(state_topic,
	payload="offline", qos=0, retain=False)

def onConnect(client, userdata, flags, rc):
    if rc == 0:
        print("connected...")
        client.publish(state_topic, 'online', retain=True)
    else:
        print("conneciton problem: code", rc)

client.on_connect = onConnect
client.username_pw_set(
        username=mqtt_user, password=mqtt_passwd)
client.connect(broker, port)
time.sleep(5)
client.loop_start()

while True:
    co2level, temp = co2sensor.read_mh_z19_with_temperature(serial_port)
    print("Co2 level is at", co2level, "temp", temp)
    payload = json.dumps({"ppm": co2level, "temperature": temp})
    client.publish(topic, payload)
    time.sleep(10)
