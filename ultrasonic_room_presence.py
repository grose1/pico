# for use with HC-SR04 ultrasonic sensor. Detects objects closer than 120cm and sends an MQTT message 
import network
import time
import utime
from machine import Pin
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASSWORD")

time.sleep(5)
print(wlan.isconnected())

mqtt_server = 'MQTT_SERVER'
client_id = b'pico'
topic_pub = b'picoout'
topic_msg = b'Movement Detected'

def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, port=1883, user=b'user', password=b'password', keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)
def ultra():
   global distance
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print("The distance from object is ",distance,"cm")
   time.sleep(.5)
   
while True:
    ultra()
    utime.sleep(1)
    if distance < 120:
           client.publish(topic_pub, topic_msg)
    else:
        pass
