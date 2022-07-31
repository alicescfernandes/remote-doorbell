#define TX_PIN 6
#define BIT_PERIOD 750
#define TIMES 18

// here's an array (in seconds) where each "1" begins in the signal
float times[TIMES] = {
  0, .00952, .0110, .0126, .0141, .0164, .0210, .0256, .0317, .0363, .0417, .0439, .0485, .0554, .0585, .0623, .0669, .0715 };

unsigned int last = 0;

void send_bits(){
  // go through each "1" bit
  for (int i = 0; i < TIMES-1; i++)
  {
    // calculate microseconds (us) from the second
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

  /// more awesome code  
}

void send_bits3(){
   digitalWrite(TX_PIN, HIGH);
      delayMicroseconds(500);
         digitalWrite(TX_PIN, LOW);
      delayMicroseconds(500);
}


void setup(){
  pinMode(TX_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop(){
  delay(5000);
  Serial.println("Send");
  send_bits();
  send_bits();
  send_bits();
  send_bits();
  send_bits();
}
