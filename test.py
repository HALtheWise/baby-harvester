#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from Adafruit_Thermal import *
from serial.serialutil import SerialException
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from subprocess import run
import requests

try:
    from gpiozero import Button
except Exception:
    print("Unable to start GPIO")

# Monkey patch Adadruit_Thermal
old_write = Adafruit_Thermal.write


def newWrite(self, *data):
    data = [s.encode() for s in data]
    old_write(self, *data)

def newWriteBytes(self, *args):
    if self.writeToStdout:
        for arg in args:
            sys.stdout.write(chr(arg))
    else:
        self.timeoutWait()
        self.timeoutSet(len(args) * self.byteTime)
        for arg in args:
            super(Adafruit_Thermal, self).write([arg])

Adafruit_Thermal.write = newWrite
Adafruit_Thermal.writeBytes = newWriteBytes

chrome_options = Options()
chrome_options.add_argument("--kiosk")
chrome_options.add_argument("--disable-infobars")
driver = webdriver.Chrome(chrome_options=chrome_options)

# Created from homescreen.html using http://dataurl.net/#dataurlmaker
_HOMESCREEN_URL = "data:text/html;base64,PGRpdiBzdHlsZT0id2lkdGg6IDEwMCU7IGhlaWdodDogMTAwJTsgdGV4dC1hbGlnbjogY2VudGVyO2ZvbnQtc2l6ZTogNTAiPldlbGNvbWUgdG8gdGhlIEJhYnkgSGFydmVzdGVyITwvZGl2Pg=="
if _HOMESCREEN_URL:
    driver.get(_HOMESCREEN_URL)

_PRINTER_PORT = "usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"

try:
    printer = Adafruit_Thermal(str("/dev/serial/by-id/{}".format(_PRINTER_PORT)), 9600, timeout=5)
except SerialException as e:
    print("Problem accessing printer", e)

mqtt_url = str(os.environ["MQTT_URL"])
dev_name = str(os.environ["DEVICE_NAME"])
app_secret = str(os.environ["APP_SECRET"])

conn_url = urlparse(mqtt_url)

def change_token():
    """Should hit the gateway, and the gateway will return a print of the new auth token"""
    print("changing token")
    requests.get('https://baby-harvester-gateway.herokuapp.com/changetoken', auth=(dev_name, app_secret))

def shutdown():
        run(['sudo', 'poweroff'])

button = Button(2, hold_time=3)
button.when_released = change_token
button.when_held = shutdown

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe(dev_name + "/print/text")
    client.subscribe(dev_name + "/display/url")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    body = msg.payload.decode('utf-8')
    print(msg.topic + " " + body)
    if msg.topic == (dev_name + "/print/text"):
        print("printing")
        printer.println(body)
        printer.feed(3)
        # with open(str(_PRINTER_PORT), "w") as printbuf:
        #    printbuf.write(body+"\\n")
        #    printbuf.write("\\n\\n")
        print("printed")
    elif msg.topic == (dev_name + "/display/url"):
        print(body)
        driver.get(body)
    else:
        pass



client = mqtt.Client(client_id=dev_name)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(conn_url.username, password=conn_url.password)
# client.enable_logger(logger=None)
print('connecting...')
client.connect(conn_url.hostname, conn_url.port, 60)
print('connected')
client.loop_forever()
