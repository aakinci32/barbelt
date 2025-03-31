#define MotorIn3 5  // IN3 on L298N → D5 on Uno
#define MotorIn4 4  // IN4 on L298N → D4 on Uno

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

      Serial.println("Demo starting in 2 seconds... Get ready!");
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

      Serial.println("Stirring Finished");
    } 
    else {
      Serial.println("Type 'on' to start the demo.");
    }
  }
}
