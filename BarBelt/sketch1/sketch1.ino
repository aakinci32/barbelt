void setup() {
  Serial.begin(9600);
  pinMode(13,OUTPUT);
  // put your setup code here, to run once:

}

void loop() {
  if(Serial.available() > 0){
    char command = Serial.read();
    if command == '1'{
      digitalWrite(OUTPUT,HIGH);

    }
    else if (command == '0'){
      digitalWrite(OUTPUT,LOW);
    }
  }
  // put your main code here, to run repeatedly:

}
