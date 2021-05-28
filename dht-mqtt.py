#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import board
import adafruit_dht
from configparser import ConfigParser
import json

HOSTNAME = '192.168.178.5'
PORT = 1883
TIMEOUT = 60
TOPIC = 'home/sensoren/temphum4'
PIN = board.D4
INTERVAL = 60
DECIMAL_DIGITS = 4

dhtDevice = adafruit_dht.DHT22(PIN, use_pulseio=False)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.connect(HOSTNAME, PORT, TIMEOUT)
client.loop_start()

while True:
    temperature, humidity = None, None
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
    except:
        pass
    print(humidity, temperature)

    if humidity is not None and temperature is not None:
        data = {'temperature': round(temperature, DECIMAL_DIGITS),
                'humidity': round(humidity, DECIMAL_DIGITS)}

        client.publish(TOPIC, json.dumps(data))

        print('Published. Sleeping ...')
    else:
        print('Failed to get reading. Skipping ...')

    time.sleep(INTERVAL)
