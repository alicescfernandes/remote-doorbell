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
- Seeeduino XIAO
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