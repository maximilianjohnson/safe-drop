void setup() {
  Serial.begin(9600);
  pinMode(13,HIGH); /*Sets the onboard pin to active.*/
}

void loop() {
  if(Serial.available() > 0) /*Checks to see if there's any data being sent by Python*/
  {
    int temp=Serial.read(); /*Read the data being sent by Python*/
    if(temp>=0)
      digitalWrite(13,HIGH); /*Basic Blink to check if Python and Arduino are communicating.*/
      delay(1000);
      digitalWrite(13,LOW);
      delay(1000);
      
}
}
