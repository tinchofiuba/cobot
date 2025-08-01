import json
import os

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
    

class ConfiguracionCobot:
    
    json_ultimo_cobot = ultimo_cobot
    json_cobots_guardados = cobots_guardados

    def __init__(self, model):
        self.model = model
        self.path_json = path_json
        self.path_cobots_guardados = path_cobots_guardados
        self.nombres_motores = [eslabon.get("nombre", f"eslabon {num}") for num, eslabon in self.json_ultimo_cobot.get("DOF", {}).items()]
        
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
    
    def actualizar_eslabon_cambio_motor(self, numero_de_eslabon):
        if numero_de_eslabon in self.json_ultimo_cobot.get("DOF", {}):
            datos_eslabon = self.json_ultimo_cobot["DOF"][numero_de_eslabon].get("motor", {})
            valor_pin_direccion = datos_eslabon.get("direccion", "N/A")
            valor_pin_enable = datos_eslabon.get("enable", "N/A")
            self.model.actualizar_le_direccion_y_enable_signal.emit(str(valor_pin_direccion), str(valor_pin_enable))
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
            
    def borrar_cobot(self, nombre_cobot: str):
        if nombre_cobot in self.json_cobots_guardados:
            del self.json_cobots_guardados[nombre_cobot]
            with open(path_cobots_guardados, "w") as file:
                json.dump(self.json_cobots_guardados, file, indent=4)
            print(f"Cobot {nombre_cobot} eliminado de los cobots guardados.")
            self.model.cobot_borrado_signal.emit(True)
        else:
            self.model.cobot_borrado_signal.emit(False)
            print(f"El cobot {nombre_cobot} no existe en los cobots guardados.")
            
            
    def cargar_datos_cobots(self):
        try:
            with open(path_cobots_guardados, "r") as file:
                self.json_cobots_guardados = json.load(file)
                print("Se ha cargado el JSON de los cobots guardados.")
                
            lista_cobots_guardados = list(self.json_cobots_guardados.keys())
            
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
            self.model.poblar_lw_cobots_signal.emit(lista_cobots_guardados, lista_descripciones)
                
        except FileNotFoundError:
            print(f"El archivo {path_cobots_guardados} no existe. No se pueden cargar los cobots guardados.")
            
    def guardar_cobot_a_json(self):
        self.json_cobots_guardados[self.nombre_cobot] = self.datos_cobot.copy()
        with open(path_cobots_guardados, "w") as file:
            json.dump(self.json_cobots_guardados, file, indent=4)
        self.model.cobot_guardado_signal.emit(True)
      
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
                self.model.cobot_guardado_signal.emit(False)
            
        except Exception as e:
            print(f"Error al guardar el cobot {self.nombre_cobot}: {e}")
            self.model.cobot_guardado_signal.emit(False)
            
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
                
            self.model.eslabon_guardado_signal.emit(True)
        
        except:
            print("Error al obtener el valor del selector DOF.")
            self.model.eslabon_guardado_signal.emit(False)
