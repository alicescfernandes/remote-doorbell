#define RECEIVER_PIN A0
#define RECEIVER_PIN_2 3
#define SIGNAL_TRESHOLD 700
#define BIT_PERIOD 750

int previousValue = 0;
int currentValue = 0;
unsigned int bitStartTime = 0;
boolean counting = false;
byte times = 0;
unsigned int timeLastNotification = 0;

// TODO: Detect the whole signal 

void setup() {
  Serial.begin(9600);
  pinMode(RECEIVER_PIN, INPUT);
}

void detectHigh(){
  int reading = analogRead(RECEIVER_PIN);
  
  previousValue = currentValue;
  currentValue = reading;
  
  // from low to high
  if(previousValue < SIGNAL_TRESHOLD && currentValue > SIGNAL_TRESHOLD){
    bitStartTime = micros();
    counting = true;
  }else if(counting && currentValue  < SIGNAL_TRESHOLD && previousValue > SIGNAL_TRESHOLD){ // from high to low
    unsigned int calculatedBitPeriod = micros() - bitStartTime;
    bitStartTime = micros();
    counting = false;
    
    if(calculatedBitPeriod > BIT_PERIOD - 50  and calculatedBitPeriod < BIT_PERIOD + 50  ){
       times = times +1;
    }else{
      times = 0;
    }  
    
  }

  if(times >= 3){
    unsigned int timeDiff = (millis()- timeLastNotification );
    float timeInSeconds = timeDiff / 1000;
    timeLastNotification = millis();
    times = 0;
    if(timeInSeconds > 15.0){ // Needs to wait 15s between dings to trigger
      Serial.println("ring ring");
    }
    
  }

}

void detectHighInterrupt(){
  
}

void loop(){
  detectHigh();
}
