import socket
 
from machine import Pin
import network

import esp
esp.osdebug(None)
import ssl
import gc
gc.collect()


file = open("creds.txt", "r")

code_creds = file.read()
led = Pin(2, Pin.OUT)

code_creds = code_creds.split(";")

ssid = code_creds[0]
password = code_creds[1]


station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

print('Connecting', ssid, password)


while station.isconnected() == False:
  pass

  
print('Connection successful')
print("Hey");
print(station.ifconfig())

led.on()











