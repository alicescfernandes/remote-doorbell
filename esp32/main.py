import urequests
from machine import Pin, ADC
import time
import os

RECEIVER_PIN = 34 # PIN 34 / GPIO15
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

signal_recv_pin = ADC(Pin(RECEIVER_PIN)) # Analog read on 34/ pin15


os_creds = open("onesignal_creds.txt", "r").read().split(";");
os_key = os_creds[0]
os_app_id = os_creds[1]

  

def notifyOneSignal(api_key, os_app_id):
  headers = {
    "Authorization": "Basic " + api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
  }
  
  payload = '{ "app_id": "'+os_app_id+'", "included_segments": ["Subscribed Users"], "contents": {"en": "Someone is at the door"}, "name": "INTERNAL_CAMPAIGN_NAME" }'
  
  response = urequests.post("https://onesignal.com/api/v1/notifications", data=payload, headers=headers)      
  print(response.text)
  

def notifyOwn():
  ring_creds = open("ring_creds.txt", "r").read()

  headers = {
      "Authorization": "Basic " + ring_creds,
  }
  
  response = urequests.post("https://ring.alicescfernandes.pt", headers=headers)      
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
    if(timeInSeconds > 2.0): # Needs to wait 2s between dings to trigger
      print("Sending notification");
      # notifyOneSignal(onesignal_key)
  
def loop():
  print("running main")
  while True:
    detectHigh()
    time.sleep(1);
    
loop()