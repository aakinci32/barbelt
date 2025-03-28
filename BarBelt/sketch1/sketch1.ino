#include <Arduino.h>

#define dirPin 2
#define stepPin 3

const float stepsPerDegree = 1600.0 / 360.0;  // 4.44 steps per degree
const int stepDelay = 2000;  // Adjust for speed (higher = slower)
int currentAngle = 0;
int garnishAngle;

void setup() {
  Serial.begin(9600);  // Start serial communication
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  delay(2000);  // Wait 2 seconds for the serial connection to establish
}
void rotateByDegrees(int degrees, bool clockwise) {
  int steps = degrees * stepsPerDegree;
  digitalWrite(dirPin, clockwise ? HIGH : LOW);  // HIGH = CW, LOW = CCW

  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(stepDelay);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(stepDelay);
  }

  currentAngle += (clockwise ? degrees : -degrees);
  if (clockwise) {
    Serial.println("Wheel done");
  }
}



void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read command from serial
    Serial.print("command: ");
    Serial.println(command);


    if (command.startsWith("Garnish")) {
      if (command.equals("Garnish Finish")) {
        rotateByDegrees(garnishAngle, false);
        Serial.println("rotate back");
      } else {
        Serial.println("Garnish command");
        garnishAngle = command.substring(8).toInt();

        // Extract the angle
        rotateByDegrees(garnishAngle, true);  // Rotate wheel forward x  degrees

      }
      Serial.println("exit if statement");

    }
    else {
      Serial.println("Ingredient command");
      String params = command.substring(11);
      Serial.println(params);
      // Example format: pin_number,state,delay_time (e.g., "13,1,2" for HIGH on pin 13 for 2 seconds)
      int commaIndex1 = params.indexOf(',');
      int commaIndex2 = params.indexOf(',', commaIndex1 + 1);
      if (commaIndex1 != -1 && commaIndex2 != -1) {
        int pin = params.substring(0, commaIndex1).toInt();  // Extract pin number
        int state = params.substring(commaIndex1 + 1, commaIndex2).toInt();  // Extract state (1 or 0)
        float delay_time = params.substring(commaIndex2 + 1).toFloat();  // Extract delay time (in seconds)
        Serial.print("Pin:");
        Serial.println(pin);
        Serial.print("state:");
        Serial.println(state);
        Serial.print("Delay:");
        Serial.println(delay_time);

        pinMode(pin, OUTPUT);  // Set the pin mode to OUTPUT

        if (state == 1) {
          digitalWrite(pin, HIGH);  // Open valve
          Serial.println(" set to HIGH (Valve Open).");
          delay(delay_time * 1000);  // Wait for the specified delay time (convert seconds to milliseconds)
          Serial.println("Ingredient Poured");
        } else {
          Serial.println("set pin to low");
          digitalWrite(pin, LOW);  // Close valve
          Serial.println("Ingredient Finished");
        }

      }

      

    }

  }

}