#include <ESP32Servo.h>

// === Servo Setup ===
Servo base, arm, elbow, grip;
int base_pin = 16, arm_pin = 17, elbow_pin = 18, grip_pin = 19;

// === Angle Tracking ===
int base_angle = 0, arm_angle = 90, elbow_angle = 90, grip_angle = 90;

// === Pose Structure ===
struct Pose {
  int base;
  int arm;
  int elbow;
  int grip;
};

// === Poses ===
Pose start_pose = {0, 90, 90, 110};
Pose wheel_ready = {0, 50, 150, 110};
Pose wheel_grip = {0, 50, 150, 50};
Pose cup_mid = {130, 90, 90, 50};
Pose cup_ready = {130, 140, 70, 50};
Pose cup_release = {130, 140, 70, 110};

// Named poses (expandable)
struct NamedPose {
  const char* name;
  Pose pose;
};

NamedPose poses[] = {
  {"start_pose", start_pose},
  {"wheel_ready", wheel_ready},
  {"wheel_grip", wheel_grip},
  {"cup_ready", cup_ready},
  {"cup_release", cup_release},
  {"cup_mid", cup_mid}
};

const int NUM_POSES = sizeof(poses) / sizeof(poses[0]);

// === Sequences ===
void runRangeCalib();  // forward declare
void runGrabGarnish();

struct Sequence {
  const char* name;
  void (*func)();
};

Sequence sequences[] = {
  {"range_calib", runRangeCalib},
  {"grab_garnish", runGrabGarnish}
};

const int NUM_SEQUENCES = sizeof(sequences) / sizeof(sequences[0]);

// === Setup ===
void setup() {
  Serial.begin(9600);

  base.attach(base_pin);
  arm.attach(arm_pin);
  elbow.attach(elbow_pin);
  grip.attach(grip_pin);

  moveToPose(start_pose);

  Serial.println("Enter manual commands (e.g., B90 A120), or use a pose/sequence name:");
  Serial.println("Available Sequences:");
  for (int i = 0; i < NUM_SEQUENCES; i++) {
    Serial.println("- " + String(sequences[i].name));
  }

  Serial.println("Available Poses:");
  for (int i = 0; i < NUM_POSES; i++) {
    Serial.println("- " + String(poses[i].name));
  }
}

// === Main Loop ===
void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    Serial.println("Processing command...");

    bool handled = false;

    // Match sequence
    for (int i = 0; i < NUM_SEQUENCES; i++) {
      if (input.equalsIgnoreCase(sequences[i].name)) {
        sequences[i].func();
        handled = true;
        break;
      }
    }

    // Match pose
    if (!handled) {
      for (int i = 0; i < NUM_POSES; i++) {
        if (input.equalsIgnoreCase(poses[i].name)) {
          moveToPose(poses[i].pose);
          handled = true;
          break;
        }
      }
    }

    // Manual input
    if (!handled) {
      processManualCommands(input);
    }

    Serial.println("Ready for next command.");
    Serial.println("Enter manual commands (e.g., B90 A120), or use a pose/sequence name:");
    Serial.println("Available Sequences:");
    for (int i = 0; i < NUM_SEQUENCES; i++) {
      Serial.println("- " + String(sequences[i].name));
    }

    Serial.println("Available Poses:");
    for (int i = 0; i < NUM_POSES; i++) {
      Serial.println("- " + String(poses[i].name));
    }
    Serial.println("Current Position: B"+String(base_angle)+" A"+String(arm_angle)+" E"+String(elbow_angle)+" G"+String(grip_angle));
  }

  delay(200);
}

// === Move to Pose ===
void moveToPose(Pose targetPose) {
  Serial.println("Moving to pose...");
  int stepSize = 5;
  bool reached = false;

  while (!reached) {
    reached = true;

    // Base
    if (abs(base_angle - targetPose.base) > stepSize) {
      base_angle += (base_angle < targetPose.base) ? stepSize : -stepSize;
      reached = false;
    } else {
      base_angle = targetPose.base;
    }

    // Arm
    if (abs(arm_angle - targetPose.arm) > stepSize) {
      arm_angle += (arm_angle < targetPose.arm) ? stepSize : -stepSize;
      reached = false;
    } else {
      arm_angle = targetPose.arm;
    }

    // Elbow
    if (abs(elbow_angle - targetPose.elbow) > stepSize) {
      elbow_angle += (elbow_angle < targetPose.elbow) ? stepSize : -stepSize;
      reached = false;
    } else {
      elbow_angle = targetPose.elbow;
    }

    // Grip
    if (abs(grip_angle - targetPose.grip) > stepSize) {
      grip_angle += (grip_angle < targetPose.grip) ? stepSize : -stepSize;
      reached = false;
    } else {
      grip_angle = targetPose.grip;
    }

    base.write(base_angle);
    arm.write(arm_angle);
    elbow.write(elbow_angle);
    grip.write(grip_angle);

    delay(30);
  }

  Serial.println("Pose reached.");
}


// === Manual Input Handler (e.g., "B90 A120") ===
void processManualCommands(String input) {
  int lastIndex = 0;
  while (lastIndex < input.length()) {
    int spaceIndex = input.indexOf(' ', lastIndex);
    if (spaceIndex == -1) spaceIndex = input.length();

    String command = input.substring(lastIndex, spaceIndex);
    command.trim();

    if (command.length() >= 2) {
      char servoID = command.charAt(0);
      int newAngle = command.substring(1).toInt();

      if (newAngle >= 0 && newAngle <= 180) {
        switch (servoID) {
          case 'B': base.write(newAngle); base_angle = newAngle; Serial.println("Base updated."); break;
          case 'A': arm.write(newAngle); arm_angle = newAngle; Serial.println("Arm updated."); break;
          case 'E': elbow.write(newAngle); elbow_angle = newAngle; Serial.println("Elbow updated."); break;
          case 'G': grip.write(newAngle); grip_angle = newAngle; Serial.println("Grip updated."); break;
          default: Serial.println("Invalid servo ID: " + command); break;
        }
      } else {
        Serial.println("Invalid angle: " + command);
      }
    }

    lastIndex = spaceIndex + 1;
  }
}

// === Sweep Helper (Used in Calibration) ===
void sweepServo(Servo& servo, int& angle, const char* label, int min_angle = 0, int max_angle = 180) {
  Serial.println(String("Sweeping ") + label);
  for (int i = min_angle; i <= max_angle; i += 5) {
    servo.write(i);
    delay(50);
  }
  for (int i = max_angle; i >= min_angle; i -= 5) {
    servo.write(i);
    delay(50);
  }
}

// === Sequence: Range Calibration ===
void runRangeCalib() {
  Serial.println("Running range calibration sequence...");
  sweepServo(base, base_angle, "Base"); delay(500); moveToPose(start_pose); delay(500);
  sweepServo(arm, arm_angle, "Arm"); delay(500); moveToPose(start_pose); delay(500);
  sweepServo(elbow, elbow_angle, "Elbow"); delay(500); moveToPose(start_pose); delay(500);
  sweepServo(grip, grip_angle, "Grip", 70, 150); delay(500); moveToPose(start_pose); delay(500);
  hardReturn();
  Serial.println("Calibration complete!");
}

void runGrabGarnish() {
  Serial.println("Grabbing test Garnish");
  moveToPose(wheel_ready); delay(300);
  grip_angle = 50;
  grip.write(grip_angle); delay(300);
  moveToPose(cup_mid); delay(300);
  moveToPose(cup_ready); delay(300);
  moveToPose(cup_release); delay(300);
  moveToPose(start_pose); delay(100);
  hardReturn();
  Serial.println("Garnish added!");
}

void hardReturn() {
  base_angle = 0;
  base.write(base_angle);
  arm_angle = 90;
  arm.write(arm_angle);
  elbow_angle = 90;
  elbow.write(elbow_angle);
  grip_angle = 110;
  grip.write(grip_angle);
}
