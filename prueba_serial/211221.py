/*
  JsonArray motoresArray = doc["pap"];
  JsonArray servosArray = doc["servos"];
  numMotores = motoresArray.size();
  numServos = servosArray.size();
  if (numMotores > MAX_PAP) {
    Serial.println("Error: Número de motores paso a paso excede el máximo soportado.");
    return;
  }

  if (numServos > MAX_SERVOS) {
    Serial.println("Error: Número de servomotores excede el máximo soportado.");
    return;
  }

  // inicio el ciclo for para setear el struct de los motores paso a paso

  for (byte i = 0; i < numMotores; i++) {
    motores[i].enable = motoresArray[i]["en"];
    motores[i].pasos = motoresArray[i]["p"];
    motores[i].direccion = motoresArray[i]["dir"];
    motores[i].largo = motoresArray[i]["l"];
    motores[i].angulo_paso = motoresArray[i]["a"];

    pinMode(motores[i].enable, OUTPUT);
    pinMode(motores[i].pasos, OUTPUT);
    pinMode(motores[i].direccion, OUTPUT);

    // Inicializo el motor por pasos -> deshabilitado inicialmente
    digitalWrite(motores[i].enable, HIGH); // HIGH deshabilitará el motor
    digitalWrite(motores[i].pasos, LOW);
    digitalWrite(motores[i].direccion, LOW);

  }

  for (byte j = 0; j < numServos; j++) {
  
    servos[j].configurar(
      servosArray[j]["n"], 
      servosArray[j]["p"], 
      servosArray[j]["l"], 
      servosArray[j]["a"]
    );
  
    digitalWrite(ledPin, HIGH);
    delay(5000);
    //Serial.println("Cobot seteado!");
    //hago un print de la cantidad de motores paso a paso y la cantidad de servos
    String mje = String(numMotores)+ " " +String(numServos);
    Serial.println(mje);
  
  } */