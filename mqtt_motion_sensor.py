import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASSWORD")

time.sleep(5)
print(wlan.isconnected())

sensor = Pin(14, Pin.IN, Pin.PULL_DOWN)

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
while True:
    if sensor.value() == 1:
        client.publish(topic_pub, topic_msg)
        time.sleep(3)
    else:
        pass
