# remote-doorbell

## TLDR;
I kept missing packages from the post office, so i've build a couple of devices that can notify me whenever someone rings the doorbell or knocks on my front door.

## Why?
I kept missing  deliveries on the packages when i'm home. I work remotely and am always on noise-cancelling headphones so when the mailman rings the bell, i sometimes don't listen and end up missing the delivery. If somehow i could get notified when someone rings at my door, then i would be able to receive all the mail and packages that come to my house

Bonus points if i can transform a knock on the door into a ring sound, because sometimes the mailman doesn't ring the bell, but instead knocks on the door, so it would be cool if whenever someone knocks on the door, the "ring receiver" would ring automatically

## How?
My doorbell system is not wired, meaning that is a two set piece that communicates via the 433mhz frequency range. The transmitter is placed outside, and the receiver sits inside the house close to the door. If this system communicates via radio frequencies then it should be possible to hijack the receiver and transmitter comunication. The ideia is that with a microcontroller and a cheap 433mhz transmitter/receiver, it should be possible to receive and transmit the same signals that the doorbell system uses, and make the doorbell ring when i need to. 

Having a microcontroller equiped with a Wifi chip, then it should be possible to read/write those signals, and call some endpoints that can trigger notifications on mobile devices, even when i'm outside. For the knock sensor, a piezo trigger should be enough to capture the vibrations of a knock

**It turns out that all of this is possible, and its awesome** 

The doorbell system uses a OOK/ASK signal type, which means that there's only really two values being transmitted, either a 1 or 0. By counting the duration of the 1s and 0s, it should be possible to detect the exact signal that the transmitter is sending. The transmitter carrier frequency depends on the device that is sending the signal, and the 1s are detectable when the signal is not flatlining, but has a nice sine wave going on.

In order to capture the "original" signal from the doorbell system, i used a RTLSDR and Universal Radio Hacker to detect and capture the bits and bit period, then with the help of some other code and arduino its possible to control a 433mhz transmitter to send that same signal. To send the values i just need to set the arduino pin to HIGH/LOW for some microseconds. The 433mhz transmitter then sends the signal with the carrier wave by itself.

On the receiver end, a ESP32 and a 433mhz receiver should be enough to read the 4333mhz range. The module i'm using decodes the signal for me, and returns only the bit value, so the pin is either HIGH/LOW during a couple of microseconds. And because a ESP32 has wifi built-in, i can call any endpoint without exposing my device on the public internet. So i created a python service that the ESP can call whenever it wants, and that server will then send the notifications to my phone (see images below).

![The San Juan Mountains are beautiful!](/requests.png "San Juan Mountains")
![The San Juan Mountains are beautiful!](/pushes.png "San Juan Mountains")


## Hardware

### Transmitter
#### Parts List
- Seeeduino XIAO SAMD21
- Piezo + 1M ohm resistor
- 433 MHZ Transmitter (Whadda Makers)
- Battery Pack

### Receiver
#### Parts List
- ESP32 (Micropython)
- 433 MHZ Reciever (Whadda Makers)
- Battery Pack

## Web
Web code for this project is in another repo, check this one


## Improvements list
- Replace Xiao with Attiny85 or Pico W
- Replace ESP32S with Pico W
- Power circuit inside casing
- Apply FIR filter to atenuate unwanted frequencies on the Receiver

# More info
[How to work with 433MHZ Wireless](https://lastminuteengineers.com/433mhz-rf-wireless-arduino-tutorial/)

[ESP32 Deep sleep](https://randomnerdtutorials.com/micropython-esp32-deep-sleep-wake-up-sources/)

[Hacking a RF Doorbell](https://samy.pl/dingdong/)
