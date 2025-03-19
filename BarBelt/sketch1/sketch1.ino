#include <Arduino.h>

#define dirPin 2
#define stepPin 3

const float stepsPerDegree = 1600.0 / 360.0;  // 4.44 steps per degree
const int stepDelay = 2000;  // Adjust for speed (higher = slower)
int currentAngle = 0;

void setup() {
  Serial.begin(9600);  // Start serial communication
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
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
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read command from serial
    if (command.startsWith("Garnish")){
      int garnishAngle = command.substring(8).toInt(); 
       // Extract the angle
      Serial.print("Garnish Angle: ");
      Serial.println(garnishAngle);
      rotateByDegrees(garnishAngle, true);  // Rotate wheel forward 90 degrees
    }
    else{
      // Example format: pin_number,state,delay_time (e.g., "13,1,2" for HIGH on pin 13 for 2 seconds)
    int commaIndex1 = command.indexOf(',');
    int commaIndex2 = command.indexOf(',', commaIndex1 + 1);

    if (commaIndex1 != -1 && commaIndex2 != -1) {
      int pin = command.substring(0, commaIndex1).toInt();  // Extract pin number
      int state = command.substring(commaIndex1 + 1, commaIndex2).toInt();  // Extract state (1 or 0)
      int delay_time = command.substring(commaIndex2 + 1).toInt();  // Extract delay time (in seconds)

      pinMode(pin, OUTPUT);  // Set the pin mode to OUTPUT

      if (state == 1) {
        digitalWrite(pin, HIGH);  // Open valve
        Serial.print("Pin ");
        Serial.print(pin);
        Serial.println(" set to HIGH (Valve Open).");


        delay(delay_time * 1000);  // Wait for the specified delay time (convert seconds to milliseconds)

      } else {
        digitalWrite(pin, LOW);  // Close valve
        Serial.print("Pin ");
        Serial.print(pin);
        Serial.println(" set to LOW (Valve Closed).");
      }
    }
  }

    }
    
}

