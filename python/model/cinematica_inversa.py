import ikpy
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np
import json

class CinematicaInversa:
    
    def __init__(self):
        '''
        hoja_de_ruta es un dict con movimientos a realizar. Cada movimiento tiene
        el array de ángulos, su velocidad y delay, si corresponde.
        '''
        self.eslabones = []

    def inicializar_cobot(self):
        '''
        Inicializa el robot con los eslabones y la cadena cinemática.
        '''
        path_json = "python/model/json/json_cobot.json"
        with open(path_json, 'r') as file:
            data = json.load(file)
        self.dict_eslabones = data.get("DOF", {})
        for i, eslabon in self.dict_eslabones.items():
            self.eslabones.append(
                URDFLink(
                    name=eslabon.get("nombre"),
                    translation_vector=eslabon.get("posicion", [0, 0, 0]),
                    rotation=[0,0,1],
                    parent_index=eslabon.get("parent_index", -1)
                    )
                )

        
        eslabones = [
            URDFLink(
                name="cintura",
                translation_vector=[0, 0, 0.05],
                rotation=[0, 0, 1],
                parent_index=-1
            ),
            
            URDFLink(
                name="hombro",
                translation_vector=[0, 0, 0.2],
                rotation=[0, 1, 0]
            ),
            
            URDFLink(
                name="codo",
                translation_vector=[0, 0, 0.2],
                rotation=[0, 1, 0]
            )
        ]
        
        self.chain = Chain(name='cobot', links=eslabones)
        
    def angulos_a_pasos(self, angulos, pasos_por_vuelta):
        """
        Convierte una lista de ángulos (radianes) a pasos para cada motor.
        angulos: lista de ángulos en radianes (ikpy)
        pasos_por_vuelta: lista con los pasos por vuelta de cada motor
        """
        pasos = []
        for i, ang in enumerate(angulos):
            grados = np.degrees(ang)
            pasos_motor = int((grados / 360.0) * pasos_por_vuelta[i])
            pasos.append(pasos_motor)
        return pasos

    def calcular_pasos_desde_orden(self, orden, pasos_por_vuelta):
        """
        Recibe un string tipo "Mover_a:(A,B,C):d0" y devuelve "p1_p2_p3_0;"
        """
        try:
            partes = orden.split(":")
            if len(partes) < 3:
                raise ValueError("Formato de orden incorrecto")
            vector = partes[1].replace("(", "").replace(")", "").split(",")
            vector = [float(x) for x in vector]
            delay = partes[2].replace("d", "").strip()
            # Calcula los ángulos con ikpy
            angulos = self.chain.inverse_kinematics(vector)
            # Omitimos el primer ángulo (OriginLink) si corresponde
            pasos = self.angulos_a_pasos(angulos[1:], pasos_por_vuelta)
            # Arma el string de salida
            pasos_str = "_".join(str(p) for p in pasos) + f"_{delay};"
            return pasos_str
        except Exception as e:
            print(f"Error al calcular pasos desde orden: {e}")
            return ""
