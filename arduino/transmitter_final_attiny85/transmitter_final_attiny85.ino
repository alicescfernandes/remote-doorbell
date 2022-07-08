#define TX_PIN 6
#define BIT_PERIOD 750
#define TIMES 24
#define PIEZO_PIN 1
#define THRESHOLD 80
#include <DigiUSB.h>
#define DIGISPARK_USB true

unsigned long GRACE_PERIOD = 5000; // 10 seconds between knocks

// here's an array (in seconds) where each "1" begins in the signal
float times[TIMES] = {
  0, .00952, .0110, .0126, .0141, .0164, .0210, .0256, .0317, .0363, .0417, .0439, .0485, .0554, .0585, .0623, .0669, .0715, .0769, .0814, .0853, .0899};
unsigned long lastTimeNotified = 0;

unsigned int last = 0;

void setup() {
  DigiUSB.begin();
  pinMode(TX_PIN, OUTPUT);
  pinMode(PIEZO_PIN, INPUT);
}


void loop(){
  DigiUSB.delay(10);
  
  int piezo_read = analogRead(PIEZO_PIN); 
  // Perform notification of the bell
  if(piezo_read >= THRESHOLD){
    unsigned long currentMillis = millis();
     if((currentMillis - lastTimeNotified) > GRACE_PERIOD){
      lastTimeNotified = millis();
        Serial.println("auto dong");
        //send_bits();
        //send_bits();
        // send_bits();
        // send_bits();
        // send_bits();
        // send_bits();
     }
      
  }
 
  if(DigiUSB.available()){
    int str = DigiUSB.read();

    if(str == 49){ //49 equals to char 1
      DigiUSB.println("Ding");
      // send_bits();
      // send_bits();
      // send_bits();
      // send_bits();
      // send_bits();
      // send_bits();
    }
  }

  DigiUSB.println(piezo_read);
  delay(50); // Wait some time to not have this consuming alot of energy
}


void send_bits(){
  // go through each "1" bit903

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
