#include <servo/cobot.h>

CobotServo servo1(2); // Cambia el pin según tu conexión

void setup() {
  Serial.begin(115200);
  servo1.begin();
}

void loop() {
  servo1.moveTo(0);
  delay(500);
  servo1.moveTo(90);
  delay(500);
  servo1.moveTo(180);
  delay(500);
}