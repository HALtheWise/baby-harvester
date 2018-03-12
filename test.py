from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from Adafruit_Thermal import *
from serial.serialutil import SerialException
import pika, os

try:
    printer = Adafruit_Thermal("/dev/serial0", 9600, timeout=5)
except SerialException:
    print("Problem accessing printer")

url = os.environ["CLOUDAMQP_URL"]
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

#channel.queue_declare(queue='amq.harvey/print/text')

def callback(ch, method, properties, body):
  print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='amq.harvey/print/text',
                      no_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()

#chrome_options = Options()
#chrome_options.add_argument("--kiosk")
#
#driver = webdriver.Chrome(chrome_options=chrome_options)
#
#driver.get('https://google.com')
