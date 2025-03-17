void setup() {
  Serial.begin(9600);  // Start serial communication
  // You can initialize pin modes here if you know which pins you're using
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read command from serial

    // Example format: pin_number,state,delay_time (e.g., "13,1,2" for HIGH on pin 13 for 2 seconds)
    int commaIndex1 = command.indexOf(',');
    int commaIndex2 = command.indexOf(',', commaIndex1 + 1);

    if (commaIndex1 != -1 && commaIndex2 != -1) {
      int pin = command.substring(0, commaIndex1).toInt();  // Extract pin number
      int state = command.substring(commaIndex1 + 1, commaIndex2).toInt();  // Extract state (1 or 0)
      int delay_time = command.substring(commaIndex2 + 1).toInt();  // Extract delay time (in seconds)

      pinMode(pin, OUTPUT);  // Set the pin mode to OUTPUT if it's not already

      // Set pin to HIGH or LOW
      if (state == 1) {
        digitalWrite(pin, HIGH);  // Set pin HIGH
        Serial.print("Pin ");
        Serial.print(pin);
        Serial.print(" set to HIGH for ");
        Serial.print(delay_time);
        Serial.println(" seconds.");
        delay(delay_time * 1000);  // Wait for the specified delay time (convert seconds to milliseconds)
      } else {
        digitalWrite(pin, LOW);  // Set pin LOW
        Serial.print("Pin ");
        Serial.print(pin);
        Serial.println(" set to LOW.");
      }
    }
  }
}
