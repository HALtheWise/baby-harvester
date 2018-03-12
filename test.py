from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from Adafruit_Thermal import *
from serial.serialutil import SerialException
import paho.mqtt.client as mqtt
from urllib.parse import urlparse

try:
    printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
except SerialException:
    print("Problem accessing printer")

mqtt_url = os.environ["MQTT_URL"]
mqtt_user = os.environ["MQTT_USER"]
mqtt_pass = os.environ["MQTT_PASS"]

conn_url = urlparse(mqtt_url)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("harvey/print/text")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(client_id="testlaptop")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(mqtt_user, password=mqtt_pass)
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
