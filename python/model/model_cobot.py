
from PyQt5.QtCore import QObject, pyqtSignal

#from python.model.cinematica_inversa import CinematicaInversa  
from python.model.configuracion_cobot import ConfiguracionCobot as cb

import json
import os
import serial
import time


class ModelCobot(QObject):

    cobot_seteado_signal = pyqtSignal(bool)
    cobot_guardado_signal = pyqtSignal(bool)  
    poblar_lw_cobots_signal = pyqtSignal(list, list)
    cobot_borrado_signal = pyqtSignal(bool)  
    cobot_cargado_signal = pyqtSignal(bool)
    conexion_signal = pyqtSignal(bool)  
    eslabon_guardado_signal = pyqtSignal(bool)  
    actualizar_le_direccion_y_enable_signal = pyqtSignal(str, str)  
    estado_iniciar_movimiento_signal = pyqtSignal(bool)
    estado_seteo_velocidad_signal = pyqtSignal(bool)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.conectado = False
        #self.CI = CinematicaInversa()
        self.cb = cb(self)
    
           
    def setear_eslabones_en_arduino(self):
        if not self.conectado:
            print("No hay conexión con el Arduino. Conectarse primero!.")
            return
        try:
            path_json = "python/model/json/json_cobot.json" 
            if os.path.exists(path_json):
                with open(path_json, "r") as file:
                    json_cobot = json.load(file)
                    json_plano = self.cb.from_json_to_arduino(json_cobot["DOF"]) 
                    json_plano_spliteado = [item for item in json_plano.split(";") if item != ""] 
                    for eslabon in json_plano_spliteado:
                        print(f"----->   Enviando al Arduino: {eslabon}")
                        self.ser.write((eslabon + "\n").encode())
                        #time.sleep(0.01)  

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
                    print("listo, cobot seteado")
            else:
                print(f"El archivo {path_json} no existe.")
        except Exception as e:
            print(f"Error al enviar el JSON al Arduino: {e}")
    
    def espera_correcta_recepcion(self, mensaje: str, **kwargs):
        """
        Espera la recepción correcta de un mensaje desde el Arduino.
        :param mensaje: Mensaje esperado desde el Arduino.
        :param kwargs: Argumentos opcionales:
            - timeout: Tiempo máximo de espera en segundos (opcional).
            - signal: Objeto signal para emitir si se recibe el mensaje esperado (opcional).
            - conf_recepcion: Mensaje de confirmación a enviar al Arduino (opcional).
        """
        t_inicial = time.time() if "timeout" in kwargs else None  # Solo inicializa si hay timeout

        while True:
            
            if t_inicial and time.time() - t_inicial > kwargs["timeout"]:
                print(f"Timeout alcanzado esperando el mensaje '{mensaje}'.")
                if "signal"  in kwargs:
                    kwargs["signal"].emit(False)  # Emitir señal indicando fallo
                break

            if self.ser.in_waiting > 0:  
                mensaje_recibido = self.ser.readline().decode().strip()
                print(f"Mensaje recibido del Arduino: {mensaje_recibido}")
                if mensaje_recibido == mensaje:
                    print(f"Mensaje '{mensaje}' recibido correctamente del Arduino.")
                    if "conf_recepcion" in kwargs:
                        self.ser.write(f"OK\n".encode())  # Enviar confirmación al Arduino
                    if "signal" in kwargs:
                        kwargs["signal"].emit(False)  # Emitir señal con el valor especificado
                    break
            else:
                time.sleep(0.01)
                
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

    def set_vel(self, RPM: str):
            try:
                if RPM != "":
                    print(f"Seteando velocidad del cobot a {RPM} RPM")
                    delay_microseconds = round(60 * 10**6 / (float(RPM) * 200))
                    print(delay_microseconds)
                    if delay_microseconds > 1500 and delay_microseconds < 200000:
                        mensaje = f"Set_vel{delay_microseconds}"
                        self.ser.write(mensaje.encode())
                        #time.sleep(0.01)  # espero por las dudas
                        print(f"Enviando mensaje de velocidad al Arduino: {mensaje}")
                        self.espera_correcta_recepcion(mensaje, config_recepcion = True)
                        self.estado_seteo_velocidad_signal.emit(True)
                    else:
                        print(f"El valor de RPM no está dentro de los parámetros{RPM} es demasiado alto, da un delay de {delay_microseconds} usegs, debe estar entre 1500 y 200000 microsegundos.")
                         
            except serial.SerialException as e:
                print(f"Error al enviar la velocidad al Arduino: {e}")
                self.estado_seteo_velocidad_signal.emit(False)

    def enviar_ordenes(self,mensaje: list, condicion_loop: bool, RPM: str):
        try:
            if condicion_loop == False:
                set_cantindad_mov = f"Set_mov{len(mensaje)}" 
                self.ser.write((set_cantindad_mov + "\n").encode())
                #time.sleep(0.01)  # espero por las dudas
                self.espera_correcta_recepcion(set_cantindad_mov, config_recepcion = True)

                while (len(mensaje) > 0):
                    #codifico el mensaje siempre que el largo sea menor a 55 bytes --> para un arduino Nano
                    mensaje_movimiento, mensaje = self.codificar_orden_de_movimiento(mensaje)
                    
                    mensaje_movimiento += "\n"
                    print(f"Enviando mensaje de movimiento: {mensaje_movimiento}")
                    self.ser.write(mensaje_movimiento.encode())
                    time.sleep(0.01)  # espero por las dudas
                    
                self.ser.write("fin".encode())
                
            self.estado_iniciar_movimiento_signal.emit(True)
                
        except serial.SerialException as e:
            print(f"Error al enviar órdenes al Arduino: {e}")
            return
        
    def iniciar_movimiento(self):
        self.ser.write("Realizar movimientos\n".encode())
        #time.sleep(0.01)  # espero por las dudas
        print("Enviando mensaje de inicio de movimientos al Arduino.")
        print("Realizar movimientos\n")
        
    def iniciar_detener_conexion(self):
        if self.conectado == False:
            try:
                self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) #para linux, 
                #self.ser = serial.Serial("COM10",9600, timeout=1)  #PAR WINDOWS, usb frontal
                time.sleep(2)  # espero por las dudas, así se establece la conexión
                mensaje = "iniciar"
                self.ser.write((mensaje+"\n").encode())
                print(f"Mensaje enviado: {mensaje}")
                time.sleep(1)  # espero por las dudas
                
                if self.ser.in_waiting > 0:
                    respuesta = self.ser.readline().decode().strip()
                    if respuesta == "iniciado":
                        self.conectado = True
                        self.conexion_signal.emit(self.conectado)    
                        print(f"Se ha establecido la conexión con el controlador")
                    else:
                        print(f"Respuesta del Arduino: {respuesta}, no es la esperada ...")
                else:
                    print("No hay respuesta del Arduino.")

            except serial.SerialException as e:
                print(f"Error al conectar con el controlador: {e}")
        else:
            mensaje = "finalizar"
            self.ser.write((mensaje+"\n").encode())
            print(f"Mensaje enviado: {mensaje}")
            time.sleep(0.01) # espero por las dudas
            
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
    