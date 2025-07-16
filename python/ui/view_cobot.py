
from .default_cobot import Ui_Dialog
from ..model.model_cobot import ModelCobot

from PyQt5.QtWidgets import QDialog




class view(Ui_Dialog, QDialog):
    def __init__(self, parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        self.model = ModelCobot()
        self.json_ultimo_cobot = self.model.json_ultimo_cobot  
        self.poblar_widgets("init")
    
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