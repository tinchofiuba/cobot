//este srcipt va a esperar hasta la conexión serial enlazada desde python.
// mientras no esté conectado va a hacer un blink del led 13 3 veces por segundo
//si se conecta lo hace 1 vez por segundo
//el arduino utilizado será un Arduino Nano por usb

int bauds = 115200;
int ledPin = 13;
int blinkDelay = 333; // 1 segundo por defecto
bool isConnected = false;

void setup() {
  Serial.begin(bauds);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Verifica si hay datos disponibles en el puerto serial
  if (Serial.available() > 0) {
    if (!isConnected) {
      isConnected = true;
      blinkDelay = 1000; // Cambia el delay a 1 segundo al conectarse
      Serial.println("Conexión establecida.");
    }
  } else {
    if (isConnected) {
      isConnected = false;
      blinkDelay = 333; // Cambia el delay a 333 ms al desconectarse
      Serial.println("Conexión perdida.");
    }
  }

  // Parpadeo del LED
  digitalWrite(ledPin, HIGH);
  delay(blinkDelay / 2);
  digitalWrite(ledPin, LOW);
  delay(blinkDelay / 2);
}
