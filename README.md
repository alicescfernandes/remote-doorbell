# remote-doorbell
Remote Doorbell: Hacking my doorbell into IoT


# TODO:
- [ ] Add converter to verify if the board is able to read the signals
- [x] Create code with piezzos to detect a knock
- [ ] Create frontend to received the notification from
  - [x] Get a basic demo
  - [ ] Vercel app with basic auth


# Hardware

## Transmitter
### Parts List
- Seeeduino XIAO SAMD21
- Piezo + 1M ohm resistor
- 433 MHZ Transmitter
- Battery Pack

## Receiver
### Parts List
- ESP
- Step Up Converter
- 433 MHZ Reciever
- Battery Pack


# Sofware

## Receiver
- OneSignal App 

## Web
- OneSignal App
- Vercel for Webpush


# Improvements list
- Replace Xiao with Attiny85 or Pico W
- Replace ESP32S  with Pico W
- Power circuit inside casing


# More info
[How to work with 433MHZ Wireless](https://lastminuteengineers.com/433mhz-rf-wireless-arduino-tutorial/)
[ESP32 Deep sleep](https://randomnerdtutorials.com/micropython-esp32-deep-sleep-wake-up-sources/)
[Hacking a RF Doorbell](https://samy.pl/dingdong/)