import ikpy
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np

class CinematicaInversa:
    
    def __init__(self, hoja_de_ruta : dict):
        '''
        hoja_de_ruta es un dict con movimientos a realizar. Cada movimiento tiene
        el array de ángulos, su velocidad y delay, si corresponde.
        '''
        self.hoja_de_ruta = hoja_de_ruta
        self.inicializar_cobot()
        
    def inicializar_cobot(self):
        '''
        Inicializa el robot con los eslabones y la cadena cinemática.
        '''
        eslabones = [
            URDFLink(
                name="cintura",
                translation_vector=[0, 0, 0.1],
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
