
from .default_cobot import Ui_Dialog
from ..model.model_cobot import ModelCobot

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QTimer

class view(Ui_Dialog, QDialog):
    
    def __init__(self, parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        self.lista_line_edits = [self.le_nombre_cobot, self.le_largo_eslavon, self.le_nombre_eslavon, self.le_angulo_minimo_eslavon]
        self.model = ModelCobot()
        self.json_ultimo_cobot = self.model.json_ultimo_cobot  
        self.error_numerico_le = False
        self.poblar_widgets("init")
        self.funcionalidad_hs()
        self.funcionalidad_pb()
        self.funcionalidad_le()
        
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
        
    def funcionalidad_pb(self):
        self.pb_seleccion_motor.clicked.connect(self.actualizar_motor)
        self.pb_borrar_todo_movimiento.clicked.connect(lambda: self.borrar_movimiento("todo"))
        self.pb_remover_movimiento.clicked.connect(lambda: self.borrar_movimiento("uno"))
        
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