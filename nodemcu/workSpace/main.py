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


def loop():
  while True:
      pot_value = signal_recv_pin.read()
      print(pot_value)



loop();