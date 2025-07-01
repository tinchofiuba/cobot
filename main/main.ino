
#include <Servo.h>

Servo hombro;
Servo antebrazo;
Servo brazo;
Servo muneca;

///////////////////////////////////////////////////
//////////////////// Funciones ////////////////////
///////////////////////////////////////////////////

// movimiento de brazos (funciones básicas que ya tenías)
void moverServoConVelocidad(int inicio, int fin, int delayTime, Servo &servo) {
  if (inicio < fin) {
    for (int angulo = inicio; angulo <= fin; angulo++) {
      servo.write(angulo);
      delay(delayTime);
    }
  } else {
    for (int angulo = inicio; angulo >= fin; angulo--) {
      servo.write(angulo);
      delay(delayTime);
    }
  }
}

void moverServo(int anguloInicial, int anguloFinal, Servo &servo, int velocidad) {
  moverServoConVelocidad(anguloInicial, anguloFinal, velocidad, servo);
}

///////////////////////////////////////////////////
/////////////// Fin de funciones //////////////////
///////////////////////////////////////////////////


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