const int MotorIn3 = 5;  // IN3 on L298N → D5 on Uno
const int MotorIn4 = 4;  // IN4 on L298N → D4 on Uno

void setup() {
  pinMode(MotorIn3, OUTPUT);
  pinMode(MotorIn4, OUTPUT);
  
  Serial.begin(9600);
  Serial.println("Type 'on' to start demo.");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "on") {

      Serial.println("Demo starting in 5 seconds... Get ready!");
      delay(5000);

      // Start motor
      digitalWrite(MotorIn4, LOW);
      analogWrite(MotorIn3, 70);  // Low speed
      Serial.println("Motor running...");

      delay(7000);  // Run for 7 seconds

      // Stop motor
      digitalWrite(MotorIn3, LOW);
      digitalWrite(MotorIn4, LOW);
      Serial.println("Motor stopped. Demo complete.");
    } 
    else {
      Serial.println("Type 'on' to start the demo.");
    }
  }
}
