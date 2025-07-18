
#include <Servo.h>
#include <ArduinoJson.h>

int bauds = 9600;
int ledPin = 13;
int blinkDelay = 333; // 1 segundo por defecto
bool isConectado = false;

// CONFIGURACION DE LOS STRUCTS DE LOS SERVOS Y MOTORES

                    #define MAX_SERVOS 6
                    #define MAX_PAP 6

                    struct servoConfig {
                      String nombre;  
                      byte pin;       
                      byte largo;     
                      float angulo_paso; 
                      Servo servo;   

                      void configurar(String n, byte p, byte l, float a) {
                        nombre = n;
                        pin = p;
                        largo = l;
                        angulo_paso = a;
                        servo.attach(pin); 
                      }
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


void setear_cobot( ) {
  while (true)  {
    if (Serial.available() >0) {
      String mensaje = Serial.readStringUntil('\n');
      mensaje.trim(); // Elimina espacios en blanco o caracteres extra
      if (mensaje.startsWith("p")) 
        {

        String datos = mensaje.substring(2); 

        String nombre = "";
        byte enable = 0;
        byte pasos = 0;
        byte direccion = 0;
        byte largo = 0;
        float angulo_paso = 0.0;
        byte largo_datos = datos.length();

        for (byte i=0; i< largo_datos; i++)
        {
          if (datos[i] == ',') {
            if (nombre == "") {
              nombre = datos.substring(0, i);
              Serial.println("Nombre del pap: " + nombre);
            } else if (enable == 0) {
              enable = datos.substring(0, i).toInt();
              Serial.println("Enable del pap: " + String(enable));
            } else if (pasos == 0) {
              pasos = datos.substring(0, i).toInt();
              Serial.println("Pasos del pap: " + String(pasos));
            } else if (direccion == 0) {
              direccion = datos.substring(0, i).toInt();
              Serial.println("Direccion del pap: " + String(direccion));
            } else if (largo == 0) {
              largo = datos.substring(0, i).toInt();
              Serial.println("Largo del pap: " + String(largo));
            } else {
              angulo_paso = datos.substring(0, i).toFloat();
              Serial.println("Angulo del pap: " + String(angulo_paso));
            }
            datos = datos.substring(i + 1); // Elimina la parte procesada
            i = -1; // Reinicia el índice para procesar el nuevo string
          }

        }
      }

      else if (mensaje.startsWith("s"))
      {

        String datos = mensaje.substring(2); 

        String nombre = "";
        byte pin = 0;
        byte largo = 0;
        float angulo_paso = 0.0;
        byte largo_datos = datos.length();

        for (byte i=0; i< largo_datos; i++)
        {
          if (datos[i] == ',') {
            if (nombre == "") {
              nombre = datos.substring(0, i);
              Serial.println("Nombre del servo: " + nombre);
            } else if (pin == 0) {
              pin = datos.substring(0, i).toInt();
              Serial.println("Pin del servo: " + String(pin));
            }  else if (largo == 0) {
              largo = datos.substring(0, i).toInt();
              Serial.println("Largo del servo: " + String(largo));
            } else {
              angulo_paso = datos.substring(0, i).toFloat();
              Serial.println("Angulo del servo: " + String(angulo_paso));
            }
            datos = datos.substring(i + 1); // Elimina la parte procesada
            i = -1; // Reinicia el índice para procesar el nuevo string
          }
        }
        Serial.prinln("siguiente");
      }

      else if (mensaje.startsWith("f"))
      {
      Serial.println("fin!!");
      break;  
      }

    }
  }
  }



void esperando_seteo()
{
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
        else if (mensaje == "set")  {
        Serial.println("esperando_set");
        setear_cobot();
          
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
          esperando_seteo();
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
  Serial.println("holaaa");
  
}

void loop() 

{
  
  esperando_inicializacion();

}
