#include <Servo.h>
#include <ArduinoJson.h>

int bauds = 9600;
int ledPin = 13;
int blinkDelay = 333; // 1 segundo por defecto
bool isConectado = false;

// CONFIGURACION DE LOS STRUCTS DE LOS SERVOS Y MOTORES

                    #define MAX_SERVOS 6
                    #define MAX_PAP 6

                    struct ServoConfig {
                      String nombre;  
                      byte pin;       
                      byte largo;     
                      byte angulo_paso; 
                      Servo servo;    

                      void configurar(String n, byte p, byte l, byte a) {
                        nombre = n;
                        pin = p;
                        largo = l;
                        angulo_paso = a;
                        servo.attach(pin); 
                      }
                    };

                    Servo servos[MAX_SERVOS];

                    byte numServos = 0;

                    struct MotorPasoAPaso {
                    byte enable;
                    byte pasos;
                    byte direccion;
                    byte largo;
                    byte angulo_paso;

                    };

                    MotorPasoAPaso motores[MAX_PAP]; 
                    byte numMotores = 0;

// FIN DE CONFIGURACION DE LOS STRUCTS DE LOS SERVOS Y MOTORES


void setear_cobot(String jsonConfig) {

  StaticJsonDocument<512> doc;

  DeserializationError error = deserializeJson(doc, jsonConfig);
  if (error) {
    Serial.println("Error al analizar JSON");
    return;
  }

  // Si llegó hasta acá es que el JSON es válido !!

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

}




void esperando_coordenadas()
{
  while (isConectado) { 
    
    digitalWrite(ledPin, HIGH);
    delay(blinkDelay / 2);
    digitalWrite(ledPin, LOW);
    delay(blinkDelay / 2);
    
    if (Serial.available() > 0) {
      
        String mensaje = Serial.readStringUntil('\n');
        mensaje.trim();
        if (mensaje == "finalizar") {
          
          Serial.println("finalizado");
          isConectado = false;   
          break;               
        
        }

        else if (mensaje.startsWith("{"))  {
          
        setear_cobot(mensaje);
          
        }
        

    }
    
  }
}
    
void esperando_inicializacion()
{
  
    if (Serial.available() > 0) {
      String mensaje = Serial.readStringUntil('\n');
      mensaje.trim(); // Elimina espacios en blanco o caracteres extra

      if (mensaje == "iniciar") {
        if (!isConectado) {
          Serial.println("iniciado");
          blinkDelay = 1000; 
          isConectado = true;
          esperando_coordenadas();
        }
      } 
      else if (mensaje == "finalizar") {
          Serial.println("finalizado"); 
          }
    }

    //else {
      //Serial.println("sin ordenes");
    //}
    
}

////////////////////////////
// FIN DEL BARDO
////////////////////////////




void setup() 
{
  
  Serial.begin(bauds);
  pinMode(ledPin, OUTPUT);
  
}

void loop() 

{
  
  esperando_inicializacion();

}
