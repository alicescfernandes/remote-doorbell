# Main code
# Compatible with any ESP32 device

import urequests
from machine import Pin, ADC
import time
import os

RECEIVER_PIN = 34 # PIN 34 / GPIO15
SIGNAL_TRESHOLD = 800
BIT_PERIOD = 750
board = os.uname().sysname
previousValue = 0
currentValue = 0
bitStartTime = 0
counting = False
times = 0
timeLastNotification = 0
signal_recv_pin = ADC(Pin(RECEIVER_PIN)) # Analog read on 34/ pin15

def notifyOwn():
  print("notify user")
  ring_creds = open("ring_creds.txt", "r").read()

  headers = {
      "Authorization": "Basic " + ring_creds,
  }
  
  response = urequests.post("https://ring.alicescfernandes.pt/notify", headers=headers)      
  print(response.text)
  
  
def detectHigh():
  global previousValue
  global currentValue 
  global bitStartTime 
  global counting
  global times
  global timeLastNotification
  global onesignal_key
  
  reading = signal_recv_pin.read()
  previousValue = currentValue
  currentValue = reading
 
 # From low to high
  if(previousValue < SIGNAL_TRESHOLD and currentValue > SIGNAL_TRESHOLD):
    bitStartTime = time.ticks_us()
    counting = True
    
  # From high to low
  elif(counting and currentValue  < SIGNAL_TRESHOLD and previousValue > SIGNAL_TRESHOLD): # from high to low
    calculatedBitPeriod = time.ticks_us() - bitStartTime
    bitStartTime = time.ticks_us()
    counting = False
    if(calculatedBitPeriod > BIT_PERIOD - 20  and calculatedBitPeriod < BIT_PERIOD + 20  ):
      times = times +1
    else:
      times = 0
      
    
  # Detect ringing and trigger notification
  if(times >= 7):
    timeDiff = time.ticks_diff(time.ticks_ms(), timeLastNotification)
    timeInSeconds = timeDiff / 1000
    timeLastNotification = time.ticks_ms()
    times = 0
    if(timeInSeconds > 2.0): # Needs to wait 2s between dings to trigger
      print("Sending notification");
      notifyOwn()
  
  
def loop():
  print("running main")
  while True:
      break_loop = detectHigh()

      
    
loop()