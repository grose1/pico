# This code reads the motion sensor input on pin 14 and prints the state while also using usb serial connection to control pin output
# multithreading is being used to dedicate one core to the motion senser and another to serial pin control 

import select
import sys
from machine import Pin
import time
import _thread

# setup poll to read USB port
poll_object = select.poll()
poll_object.register(sys.stdin,1)
pin_button = Pin(14, Pin.IN, Pin.PULL_DOWN)
pin_relay = Pin(17, mode=Pin.OUT)

def core0_thread():
    while True:
        # check usb input
        if poll_object.poll(0):
            #read as character
            ch = sys.stdin.read(1)
            if ch == '1':
                print('Pin 17 ON')
                pin_relay.on()
                time.sleep(4)
                pin_relay.off()
                print('Pin 17 OFF')
            else:
                print('Bad Input')
          
def core1_thread():
    while True:
        if pin_button.value() == 1:
            print('on')
            time.sleep(1.2)
        
        else:
            print('off')
            time.sleep(1.2)
        
second_thread = _thread.start_new_thread(core1_thread, () )
core0_thread()
