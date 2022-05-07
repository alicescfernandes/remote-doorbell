#define RECEIVER_PIN A0
#define RECEIVER_PIN_2 3

/*
  Simple example for receiving
  
  https://github.com/sui77/rc-switch/
*/


void setup() {
  Serial.begin(9600);
  //mySwitch.enableReceive(0);  // Receiver on interrupt 0 => that is pin #2
  Serial.println("ready");
  pinMode(RECEIVER_PIN, INPUT);
}

/*
void loop2() {
  if (mySwitch.available()) {
    
    Serial.print("Received ");
    Serial.print( mySwitch.getReceivedValue() );
    Serial.print(" / ");
    Serial.print( mySwitch.getReceivedBitlength() );
    Serial.print("bit ");
    Serial.print("Protocol: ");
    Serial.println( mySwitch.getReceivedProtocol() );

    mySwitch.resetAvailable();
  }
}
*/
void loop(){
  Serial.println(analogRead(RECEIVER_PIN));
}
