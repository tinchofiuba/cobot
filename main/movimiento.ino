// movimiento.ino - Funciones de movimiento para el cobot
// Este archivo se incluye automáticamente por Arduino IDE

// Función para mover múltiples servos simultáneamente
void moverMultiplesServos(int angulos[], Servo servos[], int cantidad, int velocidad) {
  // Encontrar el rango máximo de movimiento
  int maxMovimiento = 0;
  int posicionesIniciales[cantidad];
  
  // Obtener posiciones iniciales (estimadas)
  for (int i = 0; i < cantidad; i++) {
    posicionesIniciales[i] = 90; // Asumimos posición central inicial
    int movimiento = abs(angulos[i] - posicionesIniciales[i]);
    if (movimiento > maxMovimiento) {
      maxMovimiento = movimiento;
    }
  }
  
  // Mover todos los servos paso a paso
  for (int paso = 0; paso <= maxMovimiento; paso++) {
    for (int i = 0; i < cantidad; i++) {
      int inicio = posicionesIniciales[i];
      int fin = angulos[i];
      
      // Calcular posición actual del servo
      int posicionActual;
      if (inicio < fin) {
        posicionActual = inicio + (paso * (fin - inicio)) / maxMovimiento;
      } else {
        posicionActual = inicio - (paso * (inicio - fin)) / maxMovimiento;
      }
      
      servos[i].write(posicionActual);
    }
    delay(velocidad);
  }
}

// Función para secuencia de saludo
void secuenciaSaludo() {
  Serial.println("Ejecutando secuencia de saludo...");
  
  // Levantar brazo
  moverServo(0, 90, hombro, 20);
  delay(500);
  
  // Mover antebrazo
  moverServo(0, 45, antebrazo, 15);
  delay(500);
  
  // Agitar muñeca
  for (int i = 0; i < 3; i++) {
    moverServo(0, 45, muneca, 10);
    moverServo(45, 0, muneca, 10);
  }
  
  // Volver a posición inicial
  moverServo(45, 0, antebrazo, 15);
  moverServo(90, 0, hombro, 20);
  
  Serial.println("Secuencia completada!");
}

// Función para ir a posición de home
void irAPosicionHome() {
  Serial.println("Moviendo a posición HOME...");
  
  int angulosHome[] = {0, 0, 90, 0}; // hombro, antebrazo, brazo, muneca
  Servo servosArray[] = {hombro, antebrazo, brazo, muneca};
  
  moverMultiplesServos(angulosHome, servosArray, 4, 25);
  
  Serial.println("Posición HOME alcanzada");
}

// Función para posición de reposo
void irAPosicionReposo() {
  Serial.println("Moviendo a posición de REPOSO...");
  
  int angulosReposo[] = {45, 90, 135, 90}; // Posición neutral
  Servo servosArray[] = {hombro, antebrazo, brazo, muneca};
  
  moverMultiplesServos(angulosReposo, servosArray, 4, 30);
  
  Serial.println("Posición REPOSO alcanzada");
}
