import urequests
from machine import Pin, ADC
import time
from machine import ADC
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


fcm_file = open("fcm_creds.txt", "r")
fcm_server_key = fcm_file.read()

def notify(api_key):  
  headers = {
    "Authorization": "api_key="+api_key
  }
  
  payload = "title=Your%20Title&message=Your%20Message&icon=http://yourwebsite.com/icon.png&url=https://yourwebsite.com"
  
  response = urequests.post("https://api.pushalert.co/rest/v1/send", data=payload, headers=headers)      
  print(response.text)
  
  
def detectHigh():
  global previousValue
  global currentValue 
  global bitStartTime 
  global counting
  global times
  global timeLastNotification
  global fcm_server_key
  
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
    timeDiff = time.ticks_diff(ticks_ms(), timeLastNotification)
    timeInSeconds = time.timeDiff / 1000
    timeLastNotification = time.ticks_ms()
    times = 0
    if(timeInSeconds > 15.0): # Needs to wait 15s between dings to trigger
      notify(fcm_server_key)
  
def loop():
  print("running main");
  while True:
    detectHigh()
    
loop()





