
from PyQt5.QtCore import QObject, pyqtSignal

#from python.model.cinematica_inversa import CinematicaInversa  

import json
import os
import serial
import time

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

    json_ultimo_cobot = ultimo_cobot 
    json_cobots_guardados = cobots_guardados
    cobot_seteado_signal = pyqtSignal(bool)
    cobot_guardado_signal = pyqtSignal(bool)  
    poblar_lw_cobots_signal = pyqtSignal(list, list)
    cobot_borrado_signal = pyqtSignal(bool)  
    cobot_cargado_signal = pyqtSignal(bool)
    conexion_signal = pyqtSignal(bool)  
    eslabon_guardado_signal = pyqtSignal(bool)  
    actualizar_le_direccion_y_enable_signal = pyqtSignal(str, str)  
    estado_iniciar_movimiento_signal = pyqtSignal(bool)
    nombres_motores = [eslabon.get("nombre", f"eslabon {num}") for num, eslabon in json_ultimo_cobot.get("DOF", {}).items()]
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.conectado = False
        #self.CI = CinematicaInversa()
        
    def from_json_to_arduino(self, json_cobot):
        json_plano =""
        lista_setup =[]
        for key, value in json_cobot.items():
            if value['motor']['tipo'] == "Paso a paso":
                json_plano += f"p_{value['nombre']},{value['motor']['enable']},{value['motor']['pin']},{value['motor']['direccion']};"
            else:
                json_plano += f"s_{value['nombre']},{value['motor']['pin']};"
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
                    for eslabon in json_plano_spliteado:
                        print(f"----->   Enviando al Arduino: {eslabon}")
                        self.ser.write((eslabon + "\n").encode())
                        time.sleep(0.2)  

                        while True:
                            respuesta = self.ser.readline().decode().strip()
                            print(f"Respuesta del Arduino: {respuesta}  <-----")
                            if respuesta == eslabon:
                                print("")
                                print(f"Arduino ha recibido correctamente: {eslabon}")
                                self.ser.write(b"OK\n") 
                                print("")
                                break
                            else:
                                print("Esperando confirmación correcta del Arduino...")
                    print("Enviando el mensaje de finalización de seteo al Arduino ")
                    self.ser.write(b"fin_seteo\n")
                    self.cobot_seteado_signal.emit(True)
                    print("listo, ya debería estar seteado")
            else:
                print(f"El archivo {path_json} no existe.")
        except Exception as e:
            print(f"Error al enviar el JSON al Arduino: {e}")
            
    def actualizar_eslabon_cambio_motor(self, numero_de_eslabon):
        print(f"Actualizando eslavón {numero_de_eslabon} para mostrar los pines de dirección y enable del motor.")
        if numero_de_eslabon in self.json_ultimo_cobot.get("DOF", {}):
            datos_eslabon = self.json_ultimo_cobot["DOF"][numero_de_eslabon].get("motor", {})
            valor_pin_direccion = datos_eslabon.get("direccion", "N/A")
            print(f"Valor de pin dirección: {valor_pin_direccion}")
            valor_pin_enable = datos_eslabon.get("enable", "N/A")
            print(f"Valor de pin enable: {valor_pin_enable}")
            self.actualizar_le_direccion_y_enable_signal.emit(str(valor_pin_direccion), str(valor_pin_enable))
        else:
            print(f"El eslavón {numero_de_eslabon} no existe en el JSON.")
    
    def cargar_cobot(self, nombre_cobot: str):
        if nombre_cobot in self.json_cobots_guardados:
            self.nombre_cobot = nombre_cobot
            self.nombres_motores = [eslabon.get("nombre", f"eslabon {num}") for num, eslabon in self.json_ultimo_cobot.get("DOF", {}).items()]
            self.json_ultimo_cobot = self.json_cobots_guardados[nombre_cobot]
            with open(path_json, "w") as file:
                json.dump(self.json_ultimo_cobot, file, indent=4)
            print(f"Cargado el cobot {nombre_cobot} desde los cobots guardados.")
            self.cobot_cargado_signal.emit(True)
        else:
            print(f"El cobot {nombre_cobot} no existe en los cobots guardados.")
            self.cobot_cargado_signal.emit(False)
    
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
                num_servos = sum(1 for eslabon in datos_cobot.get("DOF", {}).values() if eslabon.get("motor", {}).get("tipo") == "Servo motor")
                num_paso_a_paso = sum(1 for eslabon in datos_cobot.get("DOF", {}).values() if eslabon.get("motor", {}).get("tipo") == "Paso a paso")
                
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
      
    def guardar_cobot_a_json(self):
        self.json_cobots_guardados[self.nombre_cobot] = self.datos_cobot.copy()
        with open(path_cobots_guardados, "w") as file:
            json.dump(self.json_cobots_guardados, file, indent=4)
        self.cobot_guardado_signal.emit(True)
      
    def guardar_cobot(self, nombre_cobot: str, forzar_guardado: bool, **kwargs):
        
        self.nombre_cobot = nombre_cobot
        
        if "datos_cobot" in kwargs:
            self.datos_cobot = kwargs["datos_cobot"]
            
        try:
            with open(path_json, "w") as file:
                json.dump(self.datos_cobot, file, indent=4)
            self.json_ultimo_cobot = self.datos_cobot

            if self.nombre_cobot not in self.json_cobots_guardados:
                self.guardar_cobot_a_json()
            elif forzar_guardado:
                self.guardar_cobot_a_json()
            else:
                self.cobot_guardado_signal.emit(False)
            
        except Exception as e:
            print(f"Error al guardar el cobot {self.nombre_cobot}: {e}")
            self.cobot_guardado_signal.emit(False)
            
    def guardar_eslabon(self,numero_de_DOF : str, numero_de_eslabon : str,datos_eslabon : dict):
        try:
            
            if len(self.json_ultimo_cobot["DOF"]) > int(numero_de_DOF):
                #borro cualquier DOF mayor al numero_de_DOF
                for key in list(self.json_ultimo_cobot["DOF"].keys()):
                    if int(key) > int(numero_de_DOF):
                        del self.json_ultimo_cobot["DOF"][key]
            
            if numero_de_eslabon not in self.json_ultimo_cobot.get("DOF", {}):
                self.json_ultimo_cobot["DOF"][numero_de_eslabon] = datos_eslabon

            else:
                self.json_ultimo_cobot["DOF"][numero_de_eslabon].update(datos_eslabon)
                
            self.nombres_motores = [eslabon.get("nombre", f"eslabon {num}") for num, eslabon in self.json_ultimo_cobot.get("DOF", {}).items()]

            with open("python/model/json/json_cobot.json", "w") as file:
                json.dump(self.json_ultimo_cobot, file, indent=4)
                
            self.eslabon_guardado_signal.emit(True)
        
        except:
            print("Error al obtener el valor del selector DOF.")
            self.eslabon_guardado_signal.emit(False)
    
    def espera_correcta_recepcion(self, mensaje: str, OK = bool):
        '''
        Solo tiene sentido bool cuando el mje debe ser parseado por el arduino, sino False
        '''
        if OK:
            while True:
                mensaje_recibido = self.ser.readline().decode().strip()
                print(f"Mensaje recibido del Arduino: {mensaje_recibido}")
                if mensaje_recibido == mensaje:
                    print("Mensaje de movimiento recibido correctamente del Arduino.")
                    self.ser.write("OK\n".encode())  
                    time.sleep(0.2)  # espero por las dudas
                    break
        else:
            while True:
                mensaje_recibido = self.ser.readline().decode().strip()
                print(f"Mensaje recibido del Arduino: {mensaje_recibido}")
                if mensaje_recibido == mensaje:
                    print("Mensaje de movimiento recibido correctamente del Arduino.")
                    break
            
    def codificar_orden_de_movimiento(self, lista_mov: list):
        movimiento_codificado = ""
        self.lista_mov_volatil = lista_mov.copy()  
        for movimiento in lista_mov:

            if movimiento[0][0] == "M": #solamente si la orden es del timpo Mover_a (por ahora)
                movimiento_spliteado = movimiento.split(":")
                vector_parseado = movimiento_spliteado[1].replace("(", "").replace(")", "").split(",")  
                delay = movimiento_spliteado[2].replace("d", "")
                movimiento_parseado = f"{vector_parseado[0]}_{vector_parseado[1]}_{vector_parseado[2]}_{delay};"
                if len(movimiento_codificado + movimiento_parseado) > 55:
                    return movimiento_codificado, self.lista_mov_volatil
                else:
                    movimiento_codificado += movimiento_parseado
                    self.lista_mov_volatil.remove(movimiento)
                    
        if movimiento_codificado:
            return movimiento_codificado, self.lista_mov_volatil

    def enviar_ordenes(self,mensaje: list, condicion_loop: bool, RPM: str):
        try:
            if condicion_loop == False:
                delay_microseconds = round((60 * 10**6 / (float(RPM)) * 200),0)
                set_cantindad_mov = f"Set_mov_{delay_microseconds}_{len(mensaje)}" 
                print(set_cantindad_mov)
                self.ser.write(set_cantindad_mov.encode())
                time.sleep(0.5)  # espero por las dudas
                self.espera_correcta_recepcion(set_cantindad_mov, True)

                while (len(mensaje) > 0):
                    #codifico el mensaje siempre que el largo sea menor a 55 bytes --> para un arduino Nano
                    mensaje_movimiento, mensaje = self.codificar_orden_de_movimiento(mensaje)
                    
                    mensaje_movimiento += "\n"
                    print(f"Enviando mensaje de movimiento: {mensaje_movimiento}")
                    self.ser.write(mensaje_movimiento.encode())
                    time.sleep(0.2)  # espero por las dudas
                    
                self.ser.write("fin\n".encode())
                
            self.estado_iniciar_movimiento_signal.emit(True)
                
        except serial.SerialException as e:
            print(f"Error al enviar órdenes al Arduino: {e}")
            return
        
    def iniciar_movimiento(self):
        self.ser.write("Realizar movimientos\n".encode())
        time.sleep(0.2)  # espero por las dudas
        print("Enviando mensaje de inicio de movimientos al Arduino.")
        print("Realizar movimientos\n")
        
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
                time.sleep(1) # espero por las dudas

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
            time.sleep(0.2) # espero por las dudas
            
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
        
        