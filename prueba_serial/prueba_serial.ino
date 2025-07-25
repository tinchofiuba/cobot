
#include <Servo.h>
#include <ArduinoJson.h>

int bauds = 9600;
int ledPin = 13;
int blinkDelay = 333;  // 1 segundo por defecto
bool isConectado = false;
byte p = 0, s = 0;
// CONFIGURACION DE LOS STRUCTS DE LOS SERVOS Y MOTORES

#define MAX_SERVOS 6
#define MAX_PAP 6

struct servoConfig {
  String nombre;
  byte pin;
  byte largo;
  float angulo_paso;
  Servo objeto;
  
};

byte numServos = 0;
servoConfig servos[MAX_SERVOS];


struct papconfig {
  String nombre;
  byte enable;
  byte pasos;
  byte direccion;
  byte largo;
  float angulo_paso;
};

byte numMotores = 0;
papconfig motores[MAX_PAP];

bool configuracion_terminada = false;

// FIN DE CONFIGURACION DE LOS STRUCTS DE LOS SERVOS Y MOTORES

void parsear_girar_base(String mensaje){

  byte index_pasos = mensaje.indexOf('_');
  String mensaje_pasos = mensaje.substring(0, index_pasos);
  int num_pasos = mensaje_pasos.toInt();
  mensaje = mensaje.substring(index_pasos+1);

  byte index_delay_bobina = mensaje.indexOf('_');
  String mensaje_delay_bobina = mensaje.substring(0, index_delay_bobina);
  int delay_bobina = mensaje_delay_bobina.toInt();
  mensaje = mensaje.substring(index_delay_bobina+1);

  byte index_direccion = mensaje.indexOf('_');
  String mensaje_direccion = mensaje.substring(0, index_direccion);
  int direccion = mensaje_direccion.toInt();
  mensaje = mensaje.substring(index_direccion+1);

  int delay_entre_rutinas = mensaje.toInt();

  digitalWrite(11,direccion);

  for (int i = 0; i < num_pasos ; i++){  

    digitalWrite(13, HIGH);
    delayMicroseconds(delay_bobina); 
    digitalWrite(13, LOW); 
    delayMicroseconds(delay_bobina); 
    }

  if (delay_entre_rutinas != 0)
  {
    delay(delay_entre_rutinas);
  }


  
}

void parsear_movimientos(String mensaje){
  if (mensaje.startswith("gb_"){
    mensaje = mensaje.substring(3);

  }

}


void mover_cobot(String mensaje, bool loop){

  if (loop){ 

    mensaje = mensaje.substring(3) //borro 'bl_'

    while (Serial.available() == 0){
      
      parsear_movimientos(mensaje);
      
      if (Serial.available() > 0){
        if (Serial.readStringUntil('\n') == "break_loop"){
          break;

        }
      }     
    } 

  }

}

String decodificar_servo(String string_python){ //decodificación y reconstrucción del mensaje para setear un servo

  byte fin, largo_campos = 4;
  String parseo;
  String reconstruccion = string_python.substring(0,2); // borro el "p_" y lo guardo para reconstruir
  string_python = string_python.substring(2);
  
  String campos[largo_campos];

  for (byte i = 0; i < largo_campos; i++) {

    fin = string_python.indexOf(',');
    if ( fin != -1 && fin != 255){

      String campo = string_python.substring(0, fin); // corto el texto hasta la ","
      campos[i] = campo;
      string_python = string_python.substring(fin+1);  
      reconstruccion += campo + ","; // lo agrego a la reconstrucción

    }

    else{

      campos[i] = string_python; 
      reconstruccion += string_python;

    }
    }

  for (byte i = 0; i < largo_campos; i++){

    switch (i) {
      case 0:
        servos[p].nombre = campos[i]; 
        break;
      case 1:
        servos[p].pin = campos[i].toInt();
        pinMode(servos[p].pin, OUTPUT);
        servos[p].objeto.attach(servos[p].pin);
        break;
      case 2:
        servos[p].largo = campos[i].toInt(); 
        break;
      case 3:
        servos[p].angulo_paso = campos[i].toInt(); 
        break;
    }
    
  }
  s++;
  return reconstruccion;
}

String decodificar_pap(String string_python){ //decodificación y reconstrucción del mensaje para setear un paso a paso

  byte fin, largo_campos = 6;
  String parseo;
  String reconstruccion = string_python.substring(0,2); // borro el "p_" y lo guardo para reconstruir
  string_python = string_python.substring(2);  
  String campos[largo_campos];

  for (byte i = 0; i < largo_campos; i++) {

    fin = string_python.indexOf(',');

    if ( fin != -1 && fin != 255){

      String campo = string_python.substring(0, fin); // corto el texto hasta la ","
      campos[i] = campo;
      string_python = string_python.substring(fin+1);  
      reconstruccion += campo + ","; // lo agrego a la reconstrucción
    }

    else{

      campos[i] = string_python; 
      reconstruccion += string_python;

    }

    }
  
  for (byte i = 0; i < largo_campos; i++){

    switch (i) {
      case 0:
        motores[p].nombre = campos[i]; 
        break;
      case 1:
        motores[p].enable = campos[i].toInt();
        pinMode(motores[p].enable, OUTPUT);
        digitalWrite(motores[p].enable, LOW);
        break;
      case 2:
        motores[p].pasos = campos[i].toInt(); 
        pinMode(motores[p].pasos, OUTPUT);
        break;
      case 3:
        motores[p].direccion = campos[i].toInt();
        pinMode(motores[p].direccion, OUTPUT); 
        digitalWrite(motores[p].direccion, LOW);
        break;
      case 4:
        motores[p].largo = campos[i].toInt(); 
        break;
      case 5:
        motores[p].angulo_paso = campos[i].toFloat(); 
        break;
    }
    
  }

  p++;
  return reconstruccion;
  }

String setear_cobot(String datos) {

  datos.trim();  

  if (datos.startsWith("p")) {

    return decodificar_pap(datos);
    
  } 

    else if (datos.startsWith("s")) {

      return decodificar_servo(datos);

    }
    else {

      Serial.println("Error: prefijo desconocido");

    }
  }


void esperando_seteo() {

  while (isConectado) {

    digitalWrite(ledPin, HIGH);
    delay(blinkDelay / 2);
    digitalWrite(ledPin, LOW);
    delay(blinkDelay / 2);

    if (Serial.available() > 0) {

      String mensaje = Serial.readStringUntil('\n');

      if (mensaje == "finalizar") {

        Serial.println("finalizado");
        isConectado = false;
        break;

      }

      else if (mensaje.startsWith("p_") || mensaje.startsWith("s_")) {

        Serial.println(setear_cobot(mensaje)); //reenvío a python el mje para ver si está bien

        while (Serial.available() == 0){
          digitalWrite(ledPin, HIGH);  
          if (Serial.available() > 0){

            if (Serial.readStringUntil('\n') == "OK"){
              break;

            }
          }     
        } 
      }
      else if (mensaje == "fin_seteo"){
        break; //finaliza el seteado del cobot
      }
    }
  }
}

////////////////////////////
// FIN DEL BARDO
////////////////////////////

void setup() {

  Serial.begin(bauds);
  pinMode(ledPin, OUTPUT);

}

void loop()

{

  if (Serial.available() > 0) {

    digitalWrite(ledPin,HIGH);
    delay(200);
    digitalWrite(ledPin,LOW);
    delay(200);

    String mensaje = Serial.readStringUntil('\n');
    mensaje.trim();  // Elimina espacios en blanco o caracteres extra

    if (mensaje == "iniciar") {
      if (!isConectado) {
        Serial.println("iniciado");
        blinkDelay = 1000;
        isConectado = true;
        esperando_seteo();
      }
    } 

    else if (mensaje.startsWith("gb_")){
      mensaje = mensaje.substring(3);
      mover_cobot(mensaje);
      Serial.println("finalizado");
    }
    
    else if (mensaje == "finalizar") {
      Serial.println("finalizado");
    }
  }

  //digitalWrite(ledPin,HIGH);
  //delay(20);
  //digitalWrite(ledPin,LOW);
  //delay(20);

}
