from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

from .agregar_movimientos import Ui_Dialog as Ui_Dialog_Movimiento
from .gestionar_cobots import Ui_Dialog as Ui_Dialog_GestionarCobots

class DialogGestionarCobots(Ui_Dialog_GestionarCobots, QDialog):
    
    def __init__(self, model, parent = None):
        super(DialogGestionarCobots, self).__init__(parent)
        self.setupUi(self)
        self.model = model
        self.funcionalidad_signals()
        self.config_iniciales()
        self.funcionalidad_pb_gestionar_cobot()
        self.funcionalidad_lw() 

    def funcionalidad_pb_gestionar_cobot(self):
        self.pb_borrar_cobot.clicked.connect(lambda : self.model.cb.borrar_cobot(self.lw_cobots_guardados.currentItem().text()))
        self.pb_cargar_cobot.clicked.connect(lambda : self.model.cb.cargar_cobot(self.lw_cobots_guardados.currentItem().text()))

    def mostrar_descripcion_cobot(self, row):
        if 0 <= row < len(self.lista_descripciones):
            self.te_descripcion_cobot.setPlainText(self.lista_descripciones[row])
        else:
            self.te_descripcion_cobot.clear()
        
    def funcionalidad_lw(self):
        self.lw_cobots_guardados.currentRowChanged.connect(self.mostrar_descripcion_cobot)
        
    def config_iniciales(self):
        self.model.cb.cargar_datos_cobots()
        self.te_descripcion_cobot.setStyleSheet("font-size: 12px;")
        
    def cobot_borrado(self, condicion : bool):
        if condicion:
            QMessageBox.information(self, "Éxito", "Cobot borrado correctamente.")
            self.model.cb.cargar_datos_cobots()

        else:
            QMessageBox.warning(self, "Error", "No se pudo borrar el Cobot.")
        
    def funcionalidad_signals(self):
        self.model.cobot_borrado_signal.connect(self.cobot_borrado) 
        self.model.poblar_lw_cobots_signal.connect(self.poblar_lw_cobots)
        
    def poblar_lw_cobots(self,lista_cobots_guardados, lista_descripciones):
        self.lista_descripciones = lista_descripciones
        self.lista_cobots_guardados = lista_cobots_guardados
        
        self.lw_cobots_guardados.clear()
        if not lista_cobots_guardados:
            self.lw_cobots_guardados.addItem("No hay cobots guardados.")
        else:
            self.lw_cobots_guardados.addItems(lista_cobots_guardados)
            self.te_descripcion_cobot.setPlainText(lista_descripciones[0]) 

        self.te_descripcion_cobot.clear()

class DialogMovimiento(Ui_Dialog_Movimiento, QDialog):
    
    movimiento_nuevo_signal = pyqtSignal(str)  
    lista_movimientos_posibles = ["Mover_a", "A_origen", "Begin loop", "End loop"]
    
    def __init__(self, nombres_motores, parent=None):
        super(DialogMovimiento, self).__init__(parent)
        self.nombres_motores = nombres_motores
        self.armar_lista_movimientos()
        self.setupUi(self)
        self.config_iniciales()  
        self.funcionalidad_le("change")
        self.funcionalidad_pb_movimientos()
        
    def armar_lista_movimientos(self):
        if self.nombres_motores != []:
            for nombre in self.nombres_motores:
                self.lista_movimientos_posibles.append(f"Girar {nombre}")

    def limpiar_y_deshabilitar_line_edits(self):
        for le in [self.le_x, self.le_y, self.le_z, self.le_delay]:
            le.clear()
            le.setEnabled(False)
        
    def seleccionar_movimientos(self):
        if self.pb_seleccion_movimiento.text() in self.lista_movimientos_posibles:
            
            index = self.lista_movimientos_posibles.index(self.pb_seleccion_movimiento.text())
            next_index = (index + 1) % len(self.lista_movimientos_posibles)
            self.pb_seleccion_movimiento.setText(self.lista_movimientos_posibles[next_index])
            self.funcionalidad_le("check")
            
            if "Girar" in self.pb_seleccion_movimiento.text():
                self.l_x.setText("Angulo")  
                self.l_y.setText("RPM")  
                self.l_z.setText("dir") 
            else:
                self.l_x.setText("X")
                self.l_y.setText("Y")
                self.l_z.setText("Z")

        else:
            self.pb_seleccion_movimiento.setText(self.lista_movimientos_posibles[0])
            
        if self.pb_seleccion_movimiento.text() == "Begin loop" or self.pb_seleccion_movimiento.text() == "End loop":
            self.limpiar_y_deshabilitar_line_edits()
            self.pb_agregar_movimiento.setEnabled(True)
        else:
            self.le_x.setEnabled(True)
            self.le_y.setEnabled(True)
            self.le_z.setEnabled(True)
            self.le_delay.setEnabled(True) 
        
    def funcionalidad_pb_movimientos(self):
        self.pb_seleccion_movimiento.clicked.connect(self.seleccionar_movimientos)
        self.pb_agregar_movimiento.clicked.connect(self.agregar_movimiento)
        
    def config_iniciales(self):
        self.pb_agregar_movimiento.setEnabled(False)
        
    def agregar_movimiento(self):
        delay = ""
        if self.pb_seleccion_movimiento.text() == "Loop" or self.pb_seleccion_movimiento.text() == "Endloop":
            vector = ""
        else:
            vector = f"({self.le_x.text()},{self.le_y.text()},{self.le_z.text()})"
        if self.le_delay.text() != "":
            delay = f"d{self.le_delay.text()}"
            self.movimiento = f"{self.pb_seleccion_movimiento.text()}:{vector}:{delay}"
        else:
            self.movimiento = f"{self.pb_seleccion_movimiento.text()}:{vector}:d0"
            
        self.movimiento_nuevo_signal.emit(self.movimiento)
        
        print(f"Movimiento agregado: {self.movimiento}")
        self.close()
        
    def funcionalidad_le(self,condicion: str):
        if condicion == "change":
            if self.pb_seleccion_movimiento.text() == "Girar base":
                for le in [self.le_x, self.le_y]:
                    le.textChanged.connect(lambda : self.validar_line_edits(le))
            else:
                for le in [self.le_x, self.le_y, self.le_z, self.le_delay]:
                    le.textChanged.connect(lambda : self.validar_line_edits(le))
        elif condicion == "check":
            if all(le.text() for le in [self.le_x, self.le_y, self.le_z]):
                self.pb_agregar_movimiento.setEnabled(True)
            else:
                self.pb_agregar_movimiento.setEnabled(False)
        elif condicion == "check girar base":
            if all(le.text() for le in [self.le_x, self.le_y]):
                self.pb_agregar_movimiento.setEnabled(True)
            else:
                self.pb_agregar_movimiento.setEnabled(False)
            
                
        
    def validar_line_edits(self, le):
        if le.text()== "":
            self.pb_agregar_movimiento.setEnabled(False)
            print("boton deshabilitado")
        else:
            print("boton habilitado")
            self.pb_agregar_movimiento.setEnabled(True)