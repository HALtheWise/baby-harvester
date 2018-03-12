from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from Adafruit_Thermal import *
from serial.serialutil import SerialException
from urllib.parse import urlparse
import asyncio
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1, QOS_2

try:
    printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
except SerialException:
    print("Problem accessing printer")

mqtt_url = os.environ["MQTT_URL"]
# mqtt_user = os.environ["MQTT_USER"]
# mqtt_pass = os.environ["MQTT_PASS"]

conn_url = urlparse(mqtt_url)

C = MQTTClient()

@asyncio.coroutine
def test_coro():
   yield from C.connect(uri=mqtt_url)
   yield from C.subscribe([
             ('harvey/print/text', QOS_1),
             ('harvey/display/url', QOS_1),
         ])
   while True:
         # Wait until next PUBLISH message arrives
         message = yield from C.deliver_message()
         packet = message.publish_packet
         if packet.variable_header.topic_name == 'harvey/print/text':
             print("%d:  %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
         elif packet.variable_header.topic_name == 'harvey/display/url':
             print("Todo display")
         yield from C.acknowledge_delivery(packet.variable_header.packet_id)
   yield from C.disconnect()


if __name__ == '__main__':
    loop=asyncio.get_event_loop()
    loop.run_until_complete(test_coro())

#chrome_options = Options()
#chrome_options.add_argument("--kiosk")
#
#driver = webdriver.Chrome(chrome_options=chrome_options)
#
#driver.get('https://google.com')
