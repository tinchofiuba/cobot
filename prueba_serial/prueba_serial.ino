
#include <Servo.h>
#include <ArduinoJson.h>
#define max_movimientos 10

int bauds = 9600;
int ledPin = 13;
int blinkDelay = 333;  // 1 segundo por defecto
long delay_bobina = 2000;
bool isConectado = false;
byte delay_led = 200;
byte p = 0, s = 0;
String mensaje_movimientos = "";

// CONFIGURACION DE LOS STRUCTS DE LOS SERVOS Y MOTORES
#define MAX_SERVOS 6
#define MAX_PAP 6

struct Eslabon {
  int pasos;      
  byte direccion; 
};

struct Movimiento {
  Eslabon eslabones[MAX_PAP];
  //int delay_bobina;//esto va a estar hardcodeado, hay que cambiarlo y no tengo ganas
  int delay_total;
};

Movimiento movimientos[max_movimientos]; 

int cantidad_movimientos = 0;

struct servoConfig {
  String nombre;
  byte pin;
  Servo objeto;
  
};

byte numServos = 0;
servoConfig servos[MAX_SERVOS];

struct papconfig {
  String nombre;
  byte enable;
  byte pasos;
  byte direccion;
};

byte numMotores = 0;
papconfig motores[MAX_PAP];

bool configuracion_terminada = false;

// FIN DE CONFIGURACION DE LOS STRUCTS DE LOS SERVOS Y MOTORES

void asignar_movimiento(String mensaje, byte m) {
    for (byte loc_p = 0; loc_p < p; loc_p++){
      byte index = mensaje.indexOf('_');
      int pasos_motor = mensaje.substring(0, index).toInt();
      
      movimientos[m].eslabones[loc_p].pasos = abs(pasos_motor);
      movimientos[m].eslabones[loc_p].direccion = (pasos_motor > 0) ? 1 : 0;
      //movimientos[m].delay_bobina = 1000; //super hardcodeado
      mensaje = mensaje.substring(index+1);
    }
    movimientos[m].delay_total = mensaje.toInt();
}

void espera_correcta_recepcion() {
  while (Serial.available() == 0){
    digitalWrite(13,HIGH);
    delay(60);
    digitalWrite(13,LOW);
    delay(60);
    if (Serial.available() > 0){
      if (Serial.readStringUntil('\n') == "OK"){
        break;
      }
    }     
  } 
}

void setear_movimientos_cobot(String mensaje, bool condicion_loop){ 

  if (condicion_loop == false){

    for (byte m = 0; m < cantidad_movimientos; m++){
      byte index_movimiento = mensaje.indexOf(';'); 
      asignar_movimiento(mensaje.substring(0, index_movimiento), m);
      if (m < cantidad_movimientos - 1){
      mensaje = mensaje.substring(index_movimiento+1);
      }

      /*
      Serial.print(movimientos[m].eslabones[0].pasos);
      Serial.print(" ");
      Serial.print(movimientos[m].eslabones[1].pasos);
      Serial.print(" ");
      Serial.print(movimientos[m].eslabones[2].pasos);
      Serial.print(" ");
      Serial.print(movimientos[m].eslabones[0].direccion);
      Serial.print(" ");
      Serial.print(movimientos[m].eslabones[1].direccion);
      Serial.print(" ");
      Serial.println(movimientos[m].eslabones[2].direccion);*/

    }
  }
}

String decodificar_servo(String string_python){ //decodificación y reconstrucción del mensaje para setear un servo

  byte fin, largo_campos = 2;
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
    }
    
  }
  s++;
  return reconstruccion;
}

String decodificar_pap(String string_python){ //decodificación y reconstrucción del mensaje para setear un paso a paso

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
        espera_correcta_recepcion(); //espero hasta recibir OK

      }
      else if (mensaje == "fin_seteo"){
        break; //finaliza el seteado del cobot
      }
    }
  }
}

void realizar_movimientos(byte m){
  digitalWrite(motores[0].direccion,movimientos[m].eslabones[0].direccion);
  
  Serial.println(movimientos[m].eslabones[0].direccion);
  Serial.println(motores[0].direccion);

  for (int pasos = 0; pasos < movimientos[m].eslabones[0].pasos; pasos ++){
  digitalWrite(motores[0].pasos,HIGH);
  delayMicroseconds(1000);
  digitalWrite(motores[0].pasos,LOW);
  delayMicroseconds(1000);
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

    else if (mensaje.startsWith("Set_mov")) {
        mensaje_movimientos = "";
        /*
        El mensaje viene del tipo: Set_mov_XXX_YYY
        donde XXX es el valor de delay_bobina y YYY es el número de movimientos a realizar.
        */
        cantidad_movimientos = mensaje.substring(7).toInt();
        Serial.println("Set_mov"+String(cantidad_movimientos));
        espera_correcta_recepcion(); // Espero hasta OK

        while (true) {
          digitalWrite(13,HIGH);
            if (Serial.available() > 0) {
              digitalWrite(13,LOW);
                String mensaje_parcial = Serial.readStringUntil('\n');
                mensaje_parcial.trim();
                Serial.println(mensaje_parcial);

                if (mensaje_parcial.startsWith("fin")) {
                  break; // Salir del bucle si se recibe "fin_mov"
                } else if (mensaje_parcial.length() > 0) {
                    mensaje_movimientos += mensaje_parcial;
                }
            }
        }
        setear_movimientos_cobot(mensaje_movimientos, false);
    }

    else if (mensaje.startsWith("Set_vel")) {
        /*
        El mensaje viene del tipo: Set_velXXX
        donde XXX es el valor de delay_bobina 
        */
        delay_bobina = mensaje.substring(7).toInt();
        Serial.println("Set_vel"+String(delay_bobina));
        espera_correcta_recepcion(); // Espero hasta OK
    }

    else if (mensaje.startsWith("Realizar movimientos")){
      /*
      Serial.println(cantidad_movimientos);
      Serial.println(movimientos[0].eslabones[0].direccion);
      Serial.println(movimientos[0].eslabones[0].pasos);
      Serial.println(movimientos[0].eslabones[1].direccion);
      Serial.println(movimientos[0].eslabones[1].pasos);
      Serial.println(movimientos[1].eslabones[0].direccion);
      Serial.println(movimientos[1].eslabones[0].pasos);
      Serial.println(movimientos[1].eslabones[1].direccion);
      Serial.println(movimientos[1].eslabones[1].pasos);
      Serial.println(motores[0].direccion);*/

      for (int n_mov = 0; n_mov < cantidad_movimientos; n_mov++){
          //realizar_movimientos(n_mov);

          digitalWrite(motores[0].direccion,movimientos[n_mov].eslabones[0].direccion);
          for (int pasos = 0; pasos < movimientos[n_mov].eslabones[0].pasos; pasos++){
            digitalWrite(motores[0].pasos,HIGH);
            delayMicroseconds(delay_bobina);
            digitalWrite(motores[0].pasos,LOW);
            delayMicroseconds(delay_bobina);
          }
          if (movimientos[n_mov].delay_total > 0){
            delay(movimientos[n_mov].delay_total);
          }

      }
      Serial.println("Movimientos finalizados");
    }
    
    else if (mensaje == "finalizar") {

      Serial.println("finalizado");

    }
  }

  digitalWrite(ledPin,HIGH);
  delay(delay_led);
  digitalWrite(ledPin,LOW);
  delay(delay_led);
        

}
