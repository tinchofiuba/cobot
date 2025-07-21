
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
  byte pin;
  byte largo;
  float angulo_paso;
  Servo nombre;
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


  String decodificar_servo(String string_python){

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

    s++;
    return reconstruccion;
  }

  String decodificar_pap(String string_python){

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
        } //       p_base,2,3,4,0,1.8
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
    String mensaje = Serial.readStringUntil('\n');
    mensaje.trim();  // Elimina espacios en blanco o caracteres extra

    if (mensaje == "iniciar") {
      if (!isConectado) {

        Serial.println("iniciado");
        blinkDelay = 1000;
        isConectado = true;
        esperando_seteo();
        Serial.println("fin del seteo!!!!!");
        
      }
    } else if (mensaje == "finalizar") {
      Serial.println("finalizado");
    }
  }
}
