import urequests
from machine import Pin, ADC
import time
import os

RECEIVER_PIN = 34 # PIN 34 / GPIO15
signal_recv_pin = ADC(Pin(RECEIVER_PIN)) # Analog read on 34/ pin15

def loop():
  print("running main")
  break_loop = False
  while break_loop is not True:
      reading = signal_recv_pin.read()
      print(reading)
      time.sleep_us(100);
      
    
loop()