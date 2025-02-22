void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:

}

void loop() {
  if(Serial.available() > 0){
    char command = Serial.readStringUntil('\n');

    // Example format: pin_number,state (e.g., "13,1" for HIGH, "13,0" for LOW)
    int commaIndex = command.indexOf(',');
    
    if (commaIndex != -1) {
      int pin = command.substring(0, commaIndex).toInt();  // Extract pin number
      int state = command.substring(commaIndex + 1).toInt();  // Extract state (1 or 0)

      pinMode(pin, OUTPUT);  // Set the pin mode to OUTPUT if it's not already
      if (state == 1) {
        digitalWrite(pin, HIGH);  // Set pin HIGH
      } else {
        digitalWrite(pin, LOW);  // Set pin LOW
      }
      
      Serial.print("Pin ");
      Serial.print(pin);
      Serial.print(" set to ");
      Serial.println(state == 1 ? "HIGH" : "LOW");
    
    }
  // put your main code here, to run repeatedly:

  }

    
      
}
