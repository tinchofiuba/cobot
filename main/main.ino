
#include <Servo.h>
#include "../lib/movimiento.h"

Servo hombro;
Servo antebrazo;
Servo brazo;
Servo muneca;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== INICIALIZANDO COBOT ===");
  
  // Conectar servos
  hombro.attach(2);
  antebrazo.attach(3);
  brazo.attach(4);
  muneca.attach(5);
  
  delay(1000);
  
  Serial.println("Servos conectados:");
  Serial.println("- Hombro: Pin 2");
  Serial.println("- Antebrazo: Pin 3");
  Serial.println("- Brazo: Pin 4");
  Serial.println("- Muñeca: Pin 5");
  
}

void loop() {

  delay(5000);
}