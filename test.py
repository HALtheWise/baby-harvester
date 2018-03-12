#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from Adafruit_Thermal import *
from serial.serialutil import SerialException
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from subprocess import run

try:
    printer = Adafruit_Thermal(port="/dev/ttyUSB0".encode(), baudrate=9600, timeout=5)
except SerialException:
    print("Problem accessing printer")

mqtt_url = str(os.environ["MQTT_URL"])
dev_name = str(os.environ["DEVICE_NAME"])

conn_url = urlparse(mqtt_url)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(dev_name + "/print/text")
    client.subscribe(dev_name + "/display/url")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    body = str(msg.payload)
    print(msg.topic+" "+body)
    if msg.topic == (dev_name + "/print/text"):
        print("printing")
        # printer.println(body) #seems to just print to stdout
        with open('/dev/ttyUSB0', 'w') as printbuf:
            printbuf.write(body+"\\n\\n") 
        print("printed")
    else:
        pass

client = mqtt.Client(client_id=dev_name)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(conn_url.username, password=conn_url.password)
#client.enable_logger(logger=None)
print('connecting...')
client.connect(conn_url.hostname, conn_url.port, 60)
print('connected')
client.loop_forever()

#chrome_options = Options()
#chrome_options.add_argument("--kiosk")
#
#driver = webdriver.Chrome(chrome_options=chrome_options)
#
#driver.get('https://google.com')
