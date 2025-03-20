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
  delay(2000);  // Wait 2 seconds for the serial connection to establish
  Serial.println("in setup");
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
    Serial.println("Garnish before");
    String command = Serial.readStringUntil('\n');  // Read command from serial
    Serial.println("Command is " +  command);
    // Serial.println("Garnish1");

   
    if (command.startsWith("Garnish")){
      Serial.println("Garnish command")
      digitalWrite(LED_BUILTIN, HIGH);
      delay(5000);
      digitalWrite(LED_BUILTIN, LOW);
      int garnishAngle = command.substring(8).toInt(); 
      Serial.println("Garnish 2");

       // Extract the angle
      Serial.print("Garnish Angle: ");
      Serial.println(garnishAngle);
      rotateByDegrees(garnishAngle, true);  // Rotate wheel forward 90 degrees
      Serial.println("Garnish 3");


      delay(5000);  // TODO: Fix this after we get the total time for the robot
      Serial.println("Garnish 4");

      rotateByDegrees(garnishAngle, false); // Rotate wheel back to original position
      Serial.println("Garnish after");


    }
    else{
      Serial.println("Ingredient command")
      String params = command.substring(11);
      // Example format: pin_number,state,delay_time (e.g., "13,1,2" for HIGH on pin 13 for 2 seconds)
      Serial.println("Before");
      int commaIndex1 = params.indexOf(',');
      int commaIndex2 = params.indexOf(',', commaIndex1 + 1);
      Serial.println("After");
      if (commaIndex1 != -1 && commaIndex2 != -1) {
        int pin = command.substring(0, commaIndex1).toInt();  // Extract pin number
        Serial.print("pin");
        Serial.println(pin);
        int state = command.substring(commaIndex1 + 1, commaIndex2).toInt();  // Extract state (1 or 0)
        float delay_time = command.substring(commaIndex2 + 1).toFloat();  // Extract delay time (in seconds)

        pinMode(pin, OUTPUT);  // Set the pin mode to OUTPUT
        Serial.println("Hello world");


        if (state == 1) {
          Serial.println("set pin to high");
          digitalWrite(pin, HIGH);  // Open valve
          
          Serial.println(" set to HIGH (Valve Open).");


          delay(delay_time * 1000);  // Wait for the specified delay time (convert seconds to milliseconds)

        } else {
          Serial.println("set pin to low");
          digitalWrite(pin, LOW);  // Close valve
          Serial.print("Pin ");
          Serial.print(pin);
          Serial.println(" set to LOW (Valve Closed).");
        }
      }
    }

  }
    
}


