
from PyQt5.QtCore import QObject, pyqtSignal

import json
import os
import serial
import time
#importo 

path_json = "python/model/json/json_cobot.json"
path_cobots_guardados = "python/model/json/json_cobots_guardados.json"

ultimo_cobot = {}

if os.path.exists(path_json):
    with open(path_json, "r") as file:
        try:
            ultimo_cobot = json.load(file)  
            print("se ha cargado el json asociado al ultimo cobot utilizado")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
else:
    print(f"El archivo {path_json} no existe.")
    
   
if os.path.exists(path_cobots_guardados):
    with open(path_cobots_guardados, "r") as file:
        try:
            cobots_guardados = json.load(file)  
            print("se ha cargado el json de los cobots guardados")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
else:
    print(f"El archivo {path_cobots_guardados} no existe.")

class ModelCobot(QObject):
    '''
    Model de la GUI para mandar ordenes al cobot, y también recibir información del cobot.
    '''
    json_ultimo_cobot = ultimo_cobot # json del ultimo cobot importado en instancia de clase
    json_cobots_guardados = cobots_guardados # json de los cobots guardados, se carga al iniciar la clase
    cobot_guardado_signal = pyqtSignal(bool)  # Emite True si se guardó el cobot correctamente, False si hubo un error al guardar.
    poblar_lw_cobots_signal = pyqtSignal(list, list)
    cobot_borrado_signal = pyqtSignal(bool)  # Emite True si se borró el cobot correctamente, False si hubo un error al borrar.

    ## signals
    conexion_signal = pyqtSignal(bool)  
    eslavon_guardado_signal = pyqtSignal(bool)  
    actualizar_le_direccion_y_enable_signal = pyqtSignal(str, str)  # Emite los valores de direccion y enable del motor del eslavon
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.conectado = False
        
    def from_json_to_arduino(self, json_cobot):
        json_plano =""
        lista_setup =[]
        for key, value in json_cobot.items():
            if value['motor']['tipo'] == "Paso a paso":
                json_plano += f"p_{value['nombre']},{value['motor']['enable']},{value['motor']['pin']},{value['motor']['direccion']},{value['largo']},{value['motor']['angulo_minimo']};"
            else:
                json_plano += f"s_{value['nombre']},{value['motor']['pin']},{value['largo']},{value['motor']['angulo_minimo']};"
        print("")
        print(f"json_plano: {json_plano}")
        print("")
        return json_plano
        
           
    def setear_cobot_en_arduino(self):
        
        if not self.conectado:
            print("No hay conexión con el Arduino. Conectarse primero!.")
            return
        try:
            path_json = "python/model/json/json_cobot.json" 
            if os.path.exists(path_json):
                with open(path_json, "r") as file:
                    json_cobot = json.load(file)
                    json_plano = self.from_json_to_arduino(json_cobot["DOF"]) 
                    json_plano_spliteado = [item for item in json_plano.split(";") if item != ""] 
                    for eslavon in json_plano_spliteado:
                        print(f"----->   Enviando al Arduino: {eslavon}")
                        self.ser.write((eslavon + "\n").encode())
                        time.sleep(0.5)  

                        while True:
                            respuesta = self.ser.readline().decode().strip()
                            print(f"Respuesta del Arduino: {respuesta}  <-----")
                            if respuesta == eslavon:
                                print("")
                                print(f"Arduino ha recibido correctamente: {eslavon}")
                                self.ser.write(b"OK\n") 
                                print("")
                                break
                            else:
                                print("Esperando confirmación correcta del Arduino...")
                    self.ser.write(b"fin_seteo\n")

            else:
                print(f"El archivo {path_json} no existe.")
        except Exception as e:
            print(f"Error al enviar el JSON al Arduino: {e}")
            
    def actualizar_eslavon_cambio_motor(self, numero_de_eslavon):
        print(f"Actualizando eslavón {numero_de_eslavon} para mostrar los pines de dirección y enable del motor.")
        if numero_de_eslavon in self.json_ultimo_cobot.get("DOF", {}):
            datos_eslavon = self.json_ultimo_cobot["DOF"][numero_de_eslavon].get("motor", {})
            valor_pin_direccion = datos_eslavon.get("direccion", "N/A")
            print(f"Valor de pin dirección: {valor_pin_direccion}")
            valor_pin_enable = datos_eslavon.get("enable", "N/A")
            print(f"Valor de pin enable: {valor_pin_enable}")
            self.actualizar_le_direccion_y_enable_signal.emit(str(valor_pin_direccion), str(valor_pin_enable))
        else:
            print(f"El eslavón {numero_de_eslavon} no existe en el JSON.")
    
    def guardado_sin_nombre(self, nombre_cobot : str):
        json_sin_nombre = self.json_ultimo_cobot.copy()  
        json_sin_nombre.pop("nombre", None)  
        self.json_cobots_guardados[nombre_cobot] = json_sin_nombre
        print(json_sin_nombre)
        print(f"guardando el cobot {nombre_cobot} en el json de_ cobots guardados")
        
        with open(path_cobots_guardados, "w") as file:
            json.dump(self.json_cobots_guardados, file, indent=4)
            
    def borrar_cobot(self, nombre_cobot: str):
        if nombre_cobot in self.json_cobots_guardados:
            del self.json_cobots_guardados[nombre_cobot]
            with open(path_cobots_guardados, "w") as file:
                json.dump(self.json_cobots_guardados, file, indent=4)
            print(f"Cobot {nombre_cobot} eliminado de los cobots guardados.")
            self.cobot_borrado_signal.emit(True)
        else:
            self.cobot_borrado_signal.emit(False)
            print(f"El cobot {nombre_cobot} no existe en los cobots guardados.")
            
    def cargar_datos_cobots(self):
        try:
            with open(path_cobots_guardados, "r") as file:
                self.json_cobots_guardados = json.load(file)
                print("Se ha cargado el JSON de los cobots guardados.")
                
            lista_cobots_guardados = list(self.json_cobots_guardados.keys())

            ''''
            descripción del cobot guardado.
            
            Nº de DOF  = valor
            Nº servos = valor
            Nª motores paso a paso = valor
            '''
            
            lista_descripciones = []
            for nombre_cobot, datos_cobot in self.json_cobots_guardados.items():
                descripcion = datos_cobot.get("descripcion", "")
                num_dof = len(datos_cobot.get("DOF", {}))
                num_servos = sum(1 for eslavon in datos_cobot.get("DOF", {}).values() if eslavon.get("motor", {}).get("tipo") == "Servo motor")
                num_paso_a_paso = sum(1 for eslavon in datos_cobot.get("DOF", {}).values() if eslavon.get("motor", {}).get("tipo") == "Paso a paso")
                
                descripcion = (
                    "Descripción:\n"
                    f"{descripcion}\n"
                    "\n"
                    "Detalles:\n"
                    f"DOF = {num_dof}\n"
                    f"Nº servos = {num_servos}\n"
                    f"Nº paso a paso = {num_paso_a_paso}")
                lista_descripciones.append(descripcion)
            print(f"descripciones: {lista_descripciones}")
            print(f"cobots guardados: {lista_cobots_guardados}")
            self.poblar_lw_cobots_signal.emit(lista_cobots_guardados, lista_descripciones)
                
        except FileNotFoundError:
            print(f"El archivo {path_cobots_guardados} no existe. No se pueden cargar los cobots guardados.")
      
    def guardar_cobot(self, nombre_cobot: str, forzar_guardado: bool, datos_cobot: dict):
        try:
            # 1. Guardar como "actual" (json_cobot.json)
            with open(path_json, "w") as file:
                json.dump(datos_cobot, file, indent=4)
            self.json_ultimo_cobot = datos_cobot

            # 2. Guardar en el registro de cobots guardados
            self.json_cobots_guardados[nombre_cobot] = datos_cobot.copy()
            with open(path_cobots_guardados, "w") as file:
                json.dump(self.json_cobots_guardados, file, indent=4)

            self.cobot_guardado_signal.emit(True)
        except Exception as e:
            print(f"Error al guardar el cobot {nombre_cobot}: {e}")
            self.cobot_guardado_signal.emit(False)
            
    def guardar_eslavon(self,numero_de_DOF : str, numero_de_eslavon : str,datos_eslavon : dict):
        try:
            
            # si cambio el numero de DOF borro del dict los valores mayores al numero de DOF
            
            if len(self.json_ultimo_cobot["DOF"]) > int(numero_de_DOF):
                #borro cualquier DOF mayor al numero_de_DOF
                for key in list(self.json_ultimo_cobot["DOF"].keys()):
                    if int(key) > int(numero_de_DOF):
                        del self.json_ultimo_cobot["DOF"][key]
            
            if numero_de_eslavon not in self.json_ultimo_cobot.get("DOF", {}):
                self.json_ultimo_cobot["DOF"][numero_de_eslavon] = datos_eslavon

            else:
                self.json_ultimo_cobot["DOF"][numero_de_eslavon].update(datos_eslavon)

            with open("python/model/json/json_cobot.json", "w") as file:
                json.dump(self.json_ultimo_cobot, file, indent=4)
                
            self.eslavon_guardado_signal.emit(True)
        
        except:
            print("Error al obtener el valor del selector DOF.")
            self.eslavon_guardado_signal.emit(False)

        
    def iniciar_rutina(self, mensaje):
        print("iniciando rutina")
        
    def iniciar_detener_conexion(self):
        if self.conectado == False:
            try:
                self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #para linux, 
                #self.ser = serial.Serial("COM10",9600, timeout=1)  #PAR WINDOWS, usb frontal
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
                        print(f"Se ha establecido la conexión con el controlador")
                    else:
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
        
        
        