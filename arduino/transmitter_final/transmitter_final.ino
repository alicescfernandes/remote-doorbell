#define TX_PIN 7
#define BIT_PERIOD 750
#define TIMES 24
#define PIEZO_PIN A5
#include "RunningAverage.h"
#define THRESHOLD 80
unsigned long GRACE_PERIOD = 5000; // 10 seconds between knocks

// here's an array (in seconds) where each "1" begins in the signal
float times[TIMES] = {
  0, .00952, .0110, .0126, .0141, .0164, .0210, .0256, .0317, .0363, .0417, .0439, .0485, .0554, .0585, .0623, .0669, .0715, .0769, .0814, .0853, .0899};
unsigned long lastTimeNotified = 0;
RunningAverage myRA(5);

unsigned int last = 0;

void send_bits(){
  // go through each "1" bit
  for (int i = 0; i < TIMES-1; i++)
  {
    // calculinate microseconds (us) from the second
    int us = times[i] * 1000000;

    // don't delay before the first "1"
    // (this would be a negative amount for the first iteration anwyay)
    // this essentially produces a "0"/low all the way from our last "1" to our current "1"
    if (i != 0)
      delayMicroseconds(us - last - BIT_PERIOD);

    // send a "1" for our BIT_PERIOD which is around 700-800us                         
    digitalWrite(TX_PIN, HIGH);
    delayMicroseconds(BIT_PERIOD);
    digitalWrite(TX_PIN, LOW);

    last = us;
  }  
}


void setup(){
  pinMode(TX_PIN, OUTPUT);
  Serial.begin(9600);
  pinMode(PIEZO_PIN, INPUT);
  Serial.println("ready");
}

void loop(){
  int piezo_read = analogRead(PIEZO_PIN); 
  myRA.addValue(piezo_read);
  
  // Perform notification of the bell
  if(myRA.getAverage() >= THRESHOLD){
    unsigned long currentMillis = millis();
     if((currentMillis - lastTimeNotified) > GRACE_PERIOD){
      lastTimeNotified = millis();
        Serial.println("auto dong");
        send_bits();
        send_bits();
        send_bits();
          send_bits();
        send_bits();
        send_bits();
     }
      
  }
  
  if(Serial.available()){
    String str = Serial.readString();
    Serial.println(str);
    if(str.equals("ding")){
      send_bits();
      send_bits();
      send_bits();
        send_bits();
        send_bits();
        send_bits();
    }
  }
  // Serial.println(myRA.getAverage());
  delay(50); // Wait some time to not have this consuming alot of energy
}
