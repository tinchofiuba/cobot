
from .default_cobot import Ui_Dialog
from ..model.model_cobot import ModelCobot
from .agregar_movimientos import Ui_Dialog as Ui_Dialog_Movimiento

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QTimer


class DialogMovimiento(Ui_Dialog_Movimiento, QDialog):
    
    movimiento_nievo_signal = pyqtSignal(str)  
    lista_movimientos_posibles = ["Mover a", "A origen", "Loop", "Endloop"]
    
    def __init__(self, parent=None):
        super(DialogMovimiento, self).__init__(parent)
        self.setupUi(self)
        self.config_iniciales()  
        self.funcionalidad_le("change")
        self.funcionalidad_pb()
        
    def limpiar_y_deshabilitar_line_edits(self):
        for le in [self.le_x, self.le_y, self.le_z, self.le_delay]:
            le.clear()
            le.setEnabled(False)
        
    def seleccionar_movimiento(self):
        if self.pb_seleccion_movimiento.text() in self.lista_movimientos_posibles:
            self.funcionalidad_le("check")
            index = self.lista_movimientos_posibles.index(self.pb_seleccion_movimiento.text())
            next_index = (index + 1) % len(self.lista_movimientos_posibles)
            self.pb_seleccion_movimiento.setText(self.lista_movimientos_posibles[next_index])
        else:
            self.pb_seleccion_movimiento.setText(self.lista_movimientos_posibles[0])
            
        if self.pb_seleccion_movimiento.text() == "Loop" or self.pb_seleccion_movimiento.text() == "Endloop":
            self.limpiar_y_deshabilitar_line_edits()
            self.pb_agregar_movimiento.setEnabled(True)
        else:
            self.le_x.setEnabled(True)
            self.le_y.setEnabled(True)
            self.le_z.setEnabled(True)
            self.le_delay.setEnabled(True)
            #self.pb_agregar_movimiento.setEnabled(False)            
        
    def funcionalidad_pb(self):
        self.pb_seleccion_movimiento.clicked.connect(self.seleccionar_movimiento)
        self.pb_agregar_movimiento.clicked.connect(self.agregar_movimiento)
        
    def config_iniciales(self):
        self.pb_agregar_movimiento.setEnabled(False)
        
    def agregar_movimiento(self):
        delay = ""
        vector = f"({self.le_x.text()},{self.le_y.text()},{self.le_z.text()})"
        if self.le_delay.text() != "":
            delay = f"d{self.le_delay.text()}"
            self.movimiento = f"{self.pb_seleccion_movimiento.text()} {vector} {delay}"
        else:
            self.movimiento = f"{self.pb_seleccion_movimiento.text()} {vector}"
            
        self.movimiento_nievo_signal.emit(self.movimiento)
        
        print(f"Movimiento agregado: {self.movimiento}")
        self.close()
        
    def funcionalidad_le(self,condicion: str):
        if condicion == "change":
            for le in [self.le_x, self.le_y, self.le_z]:
                le.textChanged.connect(lambda: self.validar_line_edits(le))
        elif condicion == "check":
            #me fijo si todos los los le que estan en la lista estan llenos, si es así habilito el pb_agregar_movimiento con la función all()
            if all(le.text() for le in [self.le_x, self.le_y, self.le_z]):
                print(all(le.text() for le in [self.le_x, self.le_y, self.le_z]))
                self.pb_agregar_movimiento.setEnabled(True)
            else:
                self.pb_agregar_movimiento.setEnabled(False)
                
        
    def validar_line_edits(self, le):
        print("cambio")
        if le.text()== "":
            self.pb_agregar_movimiento.setEnabled(False)
            print("boton deshabilitado")
        else:
            print("boton habilitado")
            self.pb_agregar_movimiento.setEnabled(True)
        
class view(Ui_Dialog, QDialog):
    
    def __init__(self, parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        self.lista_line_edits = [self.le_nombre_cobot, self.le_largo_eslavon, self.le_nombre_eslavon, self.le_angulo_minimo_eslavon]
        self.model = ModelCobot()
        self.config_iniciales()
        self.poblar_widgets("init")
        self.funcionalidad_hs()
        self.funcionalidad_pb()
        self.funcionalidad_le()
        self.funcionalidad_signals()
        
    def config_iniciales(self):
        self.json_ultimo_cobot = self.model.json_ultimo_cobot  
        self.error_numerico_le = False
        self.pb_conectar_controlador.setStyleSheet("background-color: #99FF99;")
        
    def estado_conexion(self, conectado):
        if conectado:
            self.l_estado_de_conexion.setText("Controlador conectado")
            self.pb_conectar_controlador.setText("Desconectar")
            self.pb_conectar_controlador.setStyleSheet("background-color: #FF9999;")
        else:
            self.l_estado_de_conexion.setText("Desconectado")
            self.pb_conectar_controlador.setText("Conectar")
            self.pb_conectar_controlador.setStyleSheet("background-color: #99FF99;")
    
    def funcionalidad_signals(self):
        self.model.conexion_signal.connect(self.estado_conexion)
        
    def validar_line_edits(self):
        todos_llenos = all(le.text().strip() != "" for le in self.lista_line_edits)
        try:
            float(self.le_largo_eslavon.text())
            float(self.le_angulo_minimo_eslavon.text())
            numericos_validos = True
        except ValueError:
            numericos_validos = False
            QMessageBox.warning(self, "Error", "Los campos numéricos deben ser válidos.")

        self.pb_guardar_eslavon.setEnabled(todos_llenos and numericos_validos)

        
    def funcionalidad_le(self):
        for le in self.lista_line_edits:
            le.textChanged.connect(self.validar_line_edits)
        
    def habilitar_deshabilitar_guardado(self):
        if all(le.text() for le in self.lista_line_edits):
            self.pb_guardar_eslavon.setEnabled(True)
        else:
            self.pb_guardar_eslavon.setEnabled(False)

    def actualizar_motor(self):
        if self.pb_seleccion_motor.text() == "Paso a paso":
            self.pb_seleccion_motor.setText("Servo motor")
        else:
            self.pb_seleccion_motor.setText("Paso a paso")
            
    def verificacion_cantidad_movimientos(self):
        if self.lw_lista_movimientos.count() == 0:
            self.pb_remover_movimiento.setEnabled(False)
            self.pb_borrar_todo_movimiento.setEnabled(False)
            self.pb_iniciar_rutina.setEnabled(False)
            self.lw_lista_movimientos.addItem("Sin movimientos asignados.")
        else:
            self.pb_remover_movimiento.setEnabled(True)
            self.pb_borrar_todo_movimiento.setEnabled(True)
            self.pb_iniciar_rutina.setEnabled(True)
        
            
    def borrar_movimiento(self, cantidad):
        if cantidad == "uno":
            try:
                item = self.lw_lista_movimientos.currentItem()
                if item:
                    self.lw_lista_movimientos.takeItem(self.lw_lista_movimientos.row(item))
            except Exception as e:
                print(f"Error al borrar movimiento: {e}")
        elif cantidad == "todo":
            self.lw_lista_movimientos.clear()
                
        self.verificacion_cantidad_movimientos() 

    def agregar_movimiento_a_lista(self, movimiento):
        if movimiento:
            #me fijo 
            self.lw_lista_movimientos.addItem(movimiento)
            self.verificacion_cantidad_movimientos()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el movimiento. Verifique los datos ingresados.")
        
    def abrir_dialogo_movimiento(self):
        dialog = DialogMovimiento(self)
        dialog.movimiento_nievo_signal.connect(self.agregar_movimiento_a_lista) 
        dialog.exec_()
            
    def iniciar_rutina(self):
        movimientos_enviados = [self.lw_lista_movimientos.item(i).text() for i in range(self.lw_lista_movimientos.count())]
        if movimientos_enviados:
            #self.model.inicar_rutina(movimientos_enviados)
            self.model.iniciar_rutina("iniciar")
        else:
            QMessageBox.warning(self, "Error", "No hay movimientos para iniciar la rutina.")
                
    def funcionalidad_pb(self):
        self.pb_seleccion_motor.clicked.connect(self.actualizar_motor)
        self.pb_borrar_todo_movimiento.clicked.connect(lambda: self.borrar_movimiento("todo"))
        self.pb_remover_movimiento.clicked.connect(lambda: self.borrar_movimiento("uno"))
        self.pb_agregar_movimiento.clicked.connect(self.abrir_dialogo_movimiento)
        self.pb_iniciar_rutina.clicked.connect(self.iniciar_rutina)
        self.pb_conectar_controlador.clicked.connect(self.model.iniciar_detener_conexion)
        self.pb_setear_cobot.clicked.connect(lambda: self.model.setear_cobot_en_arduino(self.json_ultimo_cobot))
        
        
    def funcionalidad_hs(self):
        self.hs_numero_DOF.valueChanged.connect(lambda: self.actualizar_hs(self.hs_numero_DOF, self.l_valor_numero_DOF))
        self.hs_selector_DOF.valueChanged.connect(lambda: self.actualizar_hs(self.hs_selector_DOF, self.l_valor_seleccion_DOF))
        self.habilitar_deshabilitar_guardado()
        
    def actualizar_widgets_seleccion_DOF(self, valor):
        try:
            self.le_largo_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(str(valor)).get("largo", 0)))
            self.le_nombre_eslavon.setText(self.json_ultimo_cobot.get("DOF", {}).get(str(valor)).get("nombre", "Cintura"))
            self.le_angulo_minimo_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(str(valor)).get("angulo_minimo", 1.8)))
            self.pb_seleccion_motor.setText(self.json_ultimo_cobot.get("DOF", {}).get(str(valor)).get("tipo_motor", "Paso a paso"))
            
        except Exception as e:
            print(f"Error al actualizar widgets de selección DOF: {e}")

    def actualizar_hs(self, hs, l_valor_hs):
        if hs == self.hs_numero_DOF:
            self.hs_selector_DOF.setMaximum(hs.value())
            if hs.value() < self.hs_selector_DOF.value():
                self.hs_selector_DOF.setValue(hs.value())
                self.l_valor_seleccion_DOF.setText(str(hs.value()))
        if hs == self.hs_selector_DOF:
            self.actualizar_widgets_seleccion_DOF(self.hs_selector_DOF.value())
            
        l_valor_hs.setText(str(hs.value()))
    
    def poblar_widgets(self,condicion: str):
        if self.json_ultimo_cobot:
            if condicion == "init":
                self.le_nombre_cobot.setText(self.json_ultimo_cobot.get("nombre", ""))
                self.te_descripcion_cobot.setText(self.json_ultimo_cobot.get("descripcion", ""))
                self.hs_numero_DOF.setValue(len(self.json_ultimo_cobot.get("DOF", [])))
                self.l_valor_numero_DOF.setText(str(self.hs_numero_DOF.value()))
                self.hs_selector_DOF.setMaximum(len(self.json_ultimo_cobot.get("DOF", [])))
                self.hs_selector_DOF.setMinimum(1)
                self.hs_selector_DOF.setValue(1)
                self.l_valor_seleccion_DOF.setText("1")
                self.le_largo_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get("largo", 0)))
                self.pb_seleccion_motor.setText(self.json_ultimo_cobot.get("DOF", {}).get("tipo_motor", "Paso a paso"))
                self.le_angulo_minimo_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get("angulo_minimo", 1.8)))
                self.le_nombre_eslavon.setText(self.json_ultimo_cobot.get("DOF", {}).get("nombre", "Cintura"))
                if self.json_ultimo_cobot.get("movimientos", []) != []:
                    self.lw_lista_movimientos.clear()
                    for movimiento in self.json_ultimo_cobot.get("movimientos"):
                        self.lw_lista_movimientos.addItem(movimiento)
                else:
                    self.lw_lista_movimientos.clear()

        
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = view()
    dialog.show()
    sys.exit(app.exec_())