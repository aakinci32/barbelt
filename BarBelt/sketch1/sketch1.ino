#include <Arduino.h>

#define dirPin 2
#define stepPin 3

#define MotorIn3 5  // IN3 on L298N → D5 on Uno
#define MotorIn4 4  // IN4 on L298N → D4 on Uno

const float stepsPerDegree = 1600.0 / 360.0;  // 4.44 steps per degree
const int stepDelay = 2000;  // Adjust for speed (higher = slower)
int currentAngle = 0;
int garnishAngle;

void setup() {
  Serial.begin(9600);  // Start serial communication
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(MotorIn3, OUTPUT);
  pinMode(MotorIn4, OUTPUT);
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
    String command = Serial.readStringUntil('\n');
    Serial.print("command: ");
    Serial.println(command);

    // GARNISH COMMANDS
    if (command.startsWith("Garnish")) {
      if (command.equals("Garnish Finish")) {
        rotateByDegrees(garnishAngle, false);
        Serial.println("rotate back");
      } else {
        Serial.println("Garnish command");
        garnishAngle = command.substring(8).toInt();  // Extract angle
        rotateByDegrees(garnishAngle, true);         // Rotate forward
      }
      Serial.println("exit if statement");
    }

    // START POUR MULTIPLE PINS
    else if (command.startsWith("StartPour ")) {
      String pins_str = command.substring(10);  // Get "5,6,9"
      while (pins_str.length() > 0) {
        int commaIndex = pins_str.indexOf(',');
        String pinStr;
        if (commaIndex == -1) {
          pinStr = pins_str;
          pins_str = "";
        } else {
          pinStr = pins_str.substring(0, commaIndex);
          pins_str = pins_str.substring(commaIndex + 1);
        }

        int pin = pinStr.toInt();
        pinMode(pin, OUTPUT);
        digitalWrite(pin, HIGH);
        Serial.println("Ingredient Poured " + String(pin));
      }
    }

    // LOW COMMAND FOR INDIVIDUAL PIN
    else if (command.startsWith("Ingredient ")) {
      String params = command.substring(11);  // Strip "Ingredient "
      Serial.println(params);

      int commaIndex1 = params.indexOf(',');
      int commaIndex2 = params.indexOf(',', commaIndex1 + 1);

      if (commaIndex1 != -1 && commaIndex2 != -1) {
        int pin = params.substring(0, commaIndex1).toInt();
        int state = params.substring(commaIndex1 + 1, commaIndex2).toInt();

        pinMode(pin, OUTPUT);  // Ensure pin is ready

        if (state == 0) {
          digitalWrite(pin, LOW);
          Serial.println("set pin to low");
          Serial.println("Ingredient Finished " + String(pin));
        }
      }
    }

    // Stirring Motor Spin
    else if (command.startsWith("Stir ")) {
      delay(2000);

      // Start motor
      digitalWrite(MotorIn4, LOW);
      analogWrite(MotorIn3, 90);
      Serial.println("Spinning...");

      delay(6500);

      // Stop motor
      digitalWrite(MotorIn3, LOW);
      digitalWrite(MotorIn4, LOW);
      delay(2000);

      Serial.println("Stirring Complete");
    }
  }
}
