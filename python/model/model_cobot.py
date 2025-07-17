
from PyQt5.QtCore import QObject, pyqtSignal

import json
import os
import serial
import time
#importo 

path_json = "python/model/json/json_cobot.json"

ultimo_cobot = {}

if os.path.exists(path_json):
    with open(path_json, "r") as file:
        try:
            ultimo_cobot = json.load(file)  
            print("Datos cargados:", ultimo_cobot)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
else:
    print(f"El archivo {path_json} no existe.")

class ModelCobot(QObject):
    '''
    Model de la GUI para mandar ordenes al cobot, y también recibir información del cobot.
    '''
    json_ultimo_cobot = ultimo_cobot # json del ultimo cobot importado en instancia de clase
    
    ## signals
    conexion_signal = pyqtSignal(bool)  
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.conectado = False
        print(self.json_ultimo_cobot)
        
    def setear_cobot_en_arduino(self):
        if not self.conectado:
            print("No hay conexión con el Arduino. Conectarse primero!.")
            return

        try:
            path_json = "python/model/json/ultimo_cobot_guardaro.json" #cambiar esto!!

            if os.path.exists(path_json):
                with open(path_json, "r") as file:
                    json_cobot = json.load(file)
                    json_string = json.dumps(json_cobot) 
                    print(f"Enviando JSON al Arduino: {json_string}")

                    self.ser.write((json_string + "\n").encode())
                    time.sleep(0.5)  # Esperar por si hay respuesta

                    if self.ser.in_waiting > 0:
                        respuesta = self.ser.readline().decode().strip()
                        print(f"Respuesta del Arduino: {respuesta}")
                    else:
                        print("No se recibió respuesta del Arduino.")
            else:
                print(f"El archivo {path_json} no existe.")
        except Exception as e:
            print(f"Error al enviar el JSON al Arduino: {e}")
        
        
    def actualizar_datos_json(self, datos_json):
        try:
            self.datos = json.loads(datos_json)
            self.datos_actualizados.emit(self.datos)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")

    def iniciar_rutina(self, mensaje):
        print("iniciando rutina")
        
    def iniciar_detener_conexion(self):
        if self.conectado == False:
            try:
                self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
                time.sleep(2)  # espero por las dudas, así se establece la conexión
                self.conectado = True
                mensaje = "iniciar" + "\n"  
                self.ser.write(mensaje.encode())
                print(f"Mensaje enviado: {mensaje}")
                time.sleep(0.5) # espero por las dudas

                if self.ser.in_waiting > 0:
                    respuesta = self.ser.readline().decode().strip()
                    if respuesta == "iniciado":
                        self.conexion_signal.emit(self.conectado)    
                        print(f"Se ha establecido la conexxión con el controlador")
                    print(f"Respuesta del Arduino: {respuesta}, no es la esperada ...")
                else:
                    print("No hay respuesta del Arduino.")

            except serial.SerialException as e:
                print(f"Error al conectar con el controlador: {e}")
        else:
            mensaje = "finalizar" + "\n"  
            self.ser.write(mensaje.encode())
            print(f"Mensaje enviado: {mensaje}")
            time.sleep(0.5) # espero por las dudas
            
            if self.ser.in_waiting > 0:
                respuesta = self.ser.readline().decode().strip()
                if respuesta == "finalizado":
                    self.conectado = False
                    self.conexion_signal.emit(self.conectado)    
                    print(f"Se han desconectado las funciones del controlador")
                else:
                    print(f"Respuesta del Arduino: {respuesta}, no es la esperada ...")
            else:
                print("No hay respuesta del Arduino.")
            
            #self.ser.close()
        
        
        