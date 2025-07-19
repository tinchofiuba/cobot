
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
  Servo servo;
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


void setear_cobot(String datos) {

  datos.trim();  

  while (datos.length() > 0) {
    if (datos.startsWith("p")) {
      datos = datos.substring(2); 

      byte fin = datos.indexOf(';'); 
      if (fin == -1) break; //si llego al final del string corta

      String bloque = datos.substring(0, fin);  
      datos = datos.substring(fin + 1);         

      byte idx = 0;
      String campos[6];
      for (byte i = 0; i < 6; i++) {

        byte coma = bloque.indexOf(',');
        if (coma == -1 && i < 5) {
          Serial.println("Error: faltan campos en el comando del pap");
          return;

        }

        if (coma == -1) {

          campos[i] = bloque; // Último campo
        } else {

          campos[i] = bloque.substring(0, coma);
          bloque = bloque.substring(coma + 1);

        }
      }

      String nombre = campos[0];
      byte enable = campos[1].toInt();
      byte pasos = campos[2].toInt();
      byte direccion = campos[3].toInt();
      byte largo = campos[4].toInt();
      float angulo_paso = campos[5].toFloat();

      Serial.println("Nombre del pap: " + nombre);
      Serial.println("Enable: " + String(enable));
      Serial.println("Pasos: " + String(pasos));
      Serial.println("Direccion: " + String(direccion));
      Serial.println("Largo: " + String(largo));
      Serial.println("Angulo paso: " + String(angulo_paso));

      motores[p].nombre = nombre;
      motores[p].enable = enable;
      motores[p].pasos = pasos;
      motores[p].direccion = direccion;
      motores[p].largo = largo;
      motores[p].angulo_paso = angulo_paso;

      pinMode(enable, OUTPUT);
      pinMode(pasos, OUTPUT);
      pinMode(direccion, OUTPUT);

      p++;  
    } 

    else if (datos.startsWith("s")) {

      datos = datos.substring(2); 

      byte fin = datos.indexOf(';'); 
      if (fin == -1) break; 

      String bloque = datos.substring(0, fin);  
      datos = datos.substring(fin + 1);         

      byte idx = 0;
      String campos[4];
      for (byte i = 0; i < 4; i++) {

        Serial.println("aaaaaaaaaa");
        byte coma = bloque.indexOf(',');
        if (coma == -1 && i < 3) {

          Serial.println("Error: faltan campos en el comando del servo");
          return;

        }

        if (coma == -1) {

          campos[i] = bloque; // Último campo
          Serial.println("AAAAAA");

        } else {

          campos[i] = bloque.substring(0, coma);
          bloque = bloque.substring(coma + 1);
          Serial.println("BBBB");

        }
      }

      String nombre = campos[0];
      byte pin = campos[1].toInt();
      byte largo = campos[2].toInt();
      float angulo_paso = campos[3].toFloat();

      Serial.println("Nombre del servo: " + nombre);
      Serial.println("pin: " + String(pin));
      Serial.println("Largo: " + String(largo));
      Serial.println("Angulo paso: " + String(angulo_paso));

      servos[s].nombre = nombre;
      servos[s].pin = pin;
      servos[s].largo = largo;
      servos[s].angulo_paso = angulo_paso;

      pinMode(servos[s].pin, OUTPUT);
      servos[s].servo.attach(servos[s].pin);

      s++;  

    }
    else {

      Serial.println("Error: prefijo desconocido");
      break;

    }
  }

  Serial.println("Resto del string para otros parseos: " + datos);
}


void esperando_seteo() {

  while (isConectado) {

    digitalWrite(ledPin, HIGH);
    delay(blinkDelay / 2);
    digitalWrite(ledPin, LOW);
    delay(blinkDelay / 2);

    if (Serial.available() > 0) {

      String mensaje = Serial.readStringUntil('\n');
      //mensaje.trim();
      if (mensaje == "finalizar") {

        Serial.println("finalizado");
        isConectado = false;
        break;

      }

      else if (mensaje.startsWith("p_") || mensaje.startsWith("s_")) {
        Serial.println("Seteando cobot");
        setear_cobot(mensaje);
        String chequeo_mensaje = "";
        Serial.println("seteo:");

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
      }
    } else if (mensaje == "finalizar") {
      Serial.println("finalizado");
    }
  }
}
