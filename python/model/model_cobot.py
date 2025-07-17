
from PyQt5.QtCore import QObject, pyqtSignal

import json
import os

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
    
    def __init__(self, parent = None):
        super().__init__(parent)
        print(self.json_ultimo_cobot)
        
    def actualizar_datos_json(self, datos_json):
        try:
            self.datos = json.loads(datos_json)
            self.datos_actualizados.emit(self.datos)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")