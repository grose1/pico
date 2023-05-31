import select
import sys
from machine import Pin
import time


pin_button = Pin(14, Pin.IN, Pin.PULL_DOWN)


while True:
    if pin_button.value() == 1:
        print('on')
        time.sleep(1.2)
    else:
        print('off')
        time.sleep(1.2)
