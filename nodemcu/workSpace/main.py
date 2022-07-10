import urequests
from machine import Pin, ADC

import time
import os

RECEIVER_PIN = 0
SIGNAL_TRESHOLD = 700
BIT_PERIOD = 750
board = os.uname().sysname
previousValue = 0
currentValue = 0
bitStartTime = 0
counting = False
times = 0
timeLastNotification = 0
signal_recv_pin = None

if board == 'esp32':
  signal_recv_pin = ADC(Pin(34)) # Analog read on 34
else:
  signal_recv_pin = ADC(0)


os_creds = open("onesignal_creds.txt", "r").split(";")

os_key = os_creds[0]
os_app_id = os_creds[1]

def notify(api_key):  
  headers = {
    "Authorization": "api_key="+api_key
  }
  
  payload = "title=Your%20Title&message=Your%20Message&icon=http://yourwebsite.com/icon.png&url=https://yourwebsite.com"
  
  response = urequests.post("https://api.pushalert.co/rest/v1/send", data=payload, headers=headers)      
  print(response.text)
  

def notifyOneSignal(api_key):  
  headers = {
    "Authorization": "Basic " + api_key,
    "Content-Type": "application/json",
    "Aceppt": "application/json"
  }
  
  payload = '{ "app_id": "'+os_app_id+'", "included_segments": ["Subscribed Users"], "contents": {"en": "Someone is at the door"}, "name": "INTERNAL_CAMPAIGN_NAME" }'

  response = urequests.post("https://onesignal.com/api/v1/notifications", data=payload, headers=headers)      
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
    print(calculatedBitPeriod)
    if(calculatedBitPeriod > BIT_PERIOD - 50  and calculatedBitPeriod < BIT_PERIOD + 50  ):
      times = times +1
    else:
      times = 0
      
    
  # Detect ringing and trigger notification
  if(times >= 3):
    timeDiff = time.ticks_diff(time.ticks_ms(), timeLastNotification)
    timeInSeconds = timeDiff / 1000
    timeLastNotification = time.ticks_ms()
    times = 0
    if(timeInSeconds > 15.0): # Needs to wait 15s between dings to trigger
      print("Sending notification");
      # notifyOneSignal(onesignal_key)
  
def loop():
  print("running main");
  while True:
    detectHigh()
    
loop()





