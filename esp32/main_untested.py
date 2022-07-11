import urequests
from machine import Pin, ADC
from time import ticks_us, ticks_ms, ticks_diff

RECEIVER_PIN = 0
SIGNAL_TRESHOLD = 700
BIT_PERIOD = 750

previousValue = 0
currentValue = 0
bitStartTime = 0
counting = False
times = 0
timeLastNotification = 0

signal_recv_pin = Pin(0) # Analog read on A0

fcm_file = open("fcm_creds.txt", "r")
fcm_creds = fcm_file.read()
fcm_creds = fcm_creds.split(";") 
fcm_url = fcm_creds[0]
fcm_server_key = fcm_creds[1]



def notify(fcm_project_key,fcm_server_key):
  print( "notify") 
  headers = {
  "Content-Type": "application/json",
  "Authorization": "key="+fcm_server_key
  }

  payload = """{
     "message":{
       "topic" : "doorbell",
        "notification":{
          "body":"Someone is at the doorbell",
          "title":"The doorbell ringed!!"
        }
     }
  }"""

  response = urequests.post("https://fcm.googleapis.com/v1/projects/{0}/messages:send".format(fcm_project_key), data=payload, headers=headers)      
  print(response.text)

def detectHigh():
  reading = signal_recv_pin.read()
  
  previousValue = currentValue
  currentValue = reading
  
  # From low to high
  if(previousValue < SIGNAL_TRESHOLD and currentValue > SIGNAL_TRESHOLD):
    bitStartTime = ticks_us()
    counting = True
  # From high to low
  elif(counting and currentValue  < SIGNAL_TRESHOLD and previousValue > SIGNAL_TRESHOLD): # from high to low
    calculatedBitPeriod = ticks_us() - bitStartTime
    bitStartTime = ticks_us()
    counting = False
    
    if(calculatedBitPeriod > BIT_PERIOD - 50  and calculatedBitPeriod < BIT_PERIOD + 50  ):
       times = times +1
    else:
      times = 0
      
    
  # Detect ringing and trigger notification
  if(times >= 3):
    timeDiff = ticks_diff(ticks_ms(), timeLastNotification)
    timeInSeconds = timeDiff / 1000
    timeLastNotification = ticks_ms()
    times = 0
    if(timeInSeconds > 15.0): # Needs to wait 15s between dings to trigger
      print("Ring ring")


def loop():
      while True:
        detectHigh()