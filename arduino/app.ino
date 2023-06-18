#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600);
  servo1.attach(D1);  // Connect servo1 to D1 pin
  servo2.attach(D2);  // Connect servo2 to D2 pin
}

void loop() {
  if (Serial.available() >= 5) {
    String input = Serial.readStringUntil('\n');
    int spaceIndex = input.indexOf(' ');
    if (spaceIndex != -1) {
      String servoValues[2];
      servoValues[0] = input.substring(0, spaceIndex);
      servoValues[1] = input.substring(spaceIndex + 1);

      int panPosition = servoValues[0].toInt();
      int tiltPosition = servoValues[1].toInt();

      // Control servo movements
      if (panPosition >= 0 && panPosition <= 180) {
        servo1.write(panPosition);
      }
      if (tiltPosition >= 0 && tiltPosition <= 180) {
        servo2.write(tiltPosition);
      }
    }
  }
}