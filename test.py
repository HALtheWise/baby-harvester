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
import base64

try:
    from gpiozero import Button
except Exception:
    print("Unable to start GPIO, you may not be running on a Raspberry Pi.")
    Button = None

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

_HOMESCREEN = """
<div style="width: 100%; height: 100%; text-align: center;font-size: 70;">
<img style="height: 100%; margin: auto;" src="https://halthewise.github.io/baby-harvester/homescreen.svg"/>
</div>
"""

_HOMESCREEN_URL = "data:text/html;base64," + base64.b64encode(_HOMESCREEN.encode()).decode()
if _HOMESCREEN_URL:
    driver.get(_HOMESCREEN_URL)

_PRINTER_PORT = "usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"

try:
    printer = Adafruit_Thermal(str("/dev/serial/by-id/{}".format(_PRINTER_PORT)), 9600, timeout=5)
except SerialException as e:
    print("Problem accessing printer", e)
    printer = lambda: None
    printer.println = lambda s: print("Printer would have printed '{}'".format(s))
    printer.feed = lambda n: None

mqtt_url = str(os.environ["MQTT_URL"])
dev_name = str(os.environ["DEVICE_NAME"])
app_secret = str(os.environ["APP_SECRET"])
api_root = str(os.environ["API_ROOT"])

conn_url = urlparse(mqtt_url)


def change_token():
    """Should hit the gateway, and the gateway will return a print of the new auth token"""
    print("changing token")
    requests.get(api_root + '/changetoken', auth=(dev_name, app_secret))


def shutdown():
    run(['sudo', 'poweroff'])


if Button:
    button = Button(2, hold_time=3)
    button.when_released = change_token
    button.when_held = shutdown
else:
    button = None


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
    elif msg.topic == (dev_name + "/display/clear"):
        driver.get(_HOMESCREEN_URL)
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

if len(sys.argv) > 1 and sys.argv[1] == 'auth':
    from threading import Timer
    Timer(5, change_token).start()

client.loop_forever()
