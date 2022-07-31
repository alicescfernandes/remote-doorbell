#define RECEIVER_PIN A2


void setup() {
  // initialize serial communication at 115200 bits per second:
  Serial.begin(9600);
 
  //set the resolution to 12 bits (0-4096)
  pinMode(RECEIVER_PIN, INPUT);
}

void loop() {
  // read the analog / millivolts value for pin 2:
  int analogValue = analogRead(RECEIVER_PIN);
  
  // print out the values you read:
  Serial.println(analogValue);
}
