// movimientos_locales.h - Para incluir con #include "movimientos_locales.h"

#ifndef MOVIMIENTOS_LOCALES_H
#define MOVIMIENTOS_LOCALES_H

#include <Servo.h>

// Función para secuencia de pick and place
void secuenciaPickAndPlace(Servo &hombro, Servo &antebrazo, Servo &brazo, Servo &muneca) {
  Serial.println("=== SECUENCIA PICK AND PLACE ===");
  
  // 1. Ir a posición de aproximación
  Serial.println("1. Posición de aproximación");
  moverServo(0, 45, hombro, 25);
  moverServo(0, 60, antebrazo, 20);
  delay(1000);
  
  // 2. Descender para tomar objeto
  Serial.println("2. Descender para tomar");
  moverServo(60, 90, antebrazo, 15);
  delay(500);
  
  // 3. Cerrar pinza (simular)
  Serial.println("3. Cerrar pinza");
  moverServo(0, 90, muneca, 10);
  delay(500);
  
  // 4. Levantar objeto
  Serial.println("4. Levantar objeto");
  moverServo(90, 45, antebrazo, 15);
  delay(500);
  
  // 5. Mover a posición de entrega
  Serial.println("5. Mover a entrega");
  moverServo(45, 135, hombro, 20);
  delay(1000);
  
  // 6. Descender para entregar
  Serial.println("6. Descender para entregar");
  moverServo(45, 75, antebrazo, 15);
  delay(500);
  
  // 7. Abrir pinza
  Serial.println("7. Abrir pinza");
  moverServo(90, 0, muneca, 10);
  delay(500);
  
  // 8. Volver a home
  Serial.println("8. Volver a HOME");
  moverServo(75, 0, antebrazo, 20);
  moverServo(135, 0, hombro, 25);
  
  Serial.println("=== SECUENCIA COMPLETADA ===\n");
}

// Función para calibración de servos
void calibrarServos(Servo &hombro, Servo &antebrazo, Servo &brazo, Servo &muneca) {
  Serial.println("=== CALIBRACIÓN DE SERVOS ===");
  
  Servo* servos[] = {&hombro, &antebrazo, &brazo, &muneca};
  String nombres[] = {"Hombro", "Antebrazo", "Brazo", "Muñeca"};
  
  for (int i = 0; i < 4; i++) {
    Serial.println("Calibrando " + nombres[i] + ":");
    
    // Ir a 0°
    Serial.println("  -> 0°");
    servos[i]->write(0);
    delay(1000);
    
    // Ir a 90°
    Serial.println("  -> 90°");
    servos[i]->write(90);
    delay(1000);
    
    // Ir a 180°
    Serial.println("  -> 180°");
    servos[i]->write(180);
    delay(1000);
    
    // Volver a 90°
    Serial.println("  -> 90° (centro)");
    servos[i]->write(90);
    delay(1000);
  }
  
  Serial.println("=== CALIBRACIÓN COMPLETADA ===\n");
}

#endif
