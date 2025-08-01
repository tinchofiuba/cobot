
from .default_cobot import Ui_Dialog
from ..model.model_cobot import ModelCobot

from .ventanas_emergentes import DialogMovimiento, DialogGestionarCobots

from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QTimer
        
class view(Ui_Dialog, QDialog):
    
    def __init__(self, parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        self.lista_line_edits = [self.le_nombre_cobot, self.le_nombre_eslabon, self.le_largo_eslabon, self.le_pin_pasos_eslabon, self.le_pin_direccion_eslabon, self.le_pin_enable_eslabon]
        self.model = ModelCobot()
        self.config_iniciales()
        self.poblar_widgets("init")
        self.funcionalidad_hs()
        self.funcionalidad_pb()
        self.funcionalidad_lw()
        self.funcionalidad_le()
        self.funcionalidad_signals()

    def funcionalidad_lw(self):
        self.lw_lista_movimientos.currentItemChanged.connect(self.verificacion_cantidad_movimientos)

    def config_iniciales(self):
        self.condicion_loop = False
        self.error_numerico_le = False
        self.pb_conectar_controlador.setStyleSheet("background-color: #99FF99;")
        self.l_estado_de_conexion.setStyleSheet("color: #c0392b;")
        self.pb_setear_cobot.setEnabled(False)
        self.pb_enviar_ordenes.setEnabled(False)
        self.le_RPM_cobot.setEnabled(False)

    def estado_conexion(self, conectado):
        if conectado:
            self.l_estado_de_conexion.setText("Controlador conectado")
            self.l_estado_de_conexion.setStyleSheet("color: #27ae60;")
            self.pb_conectar_controlador.setText("Desconectar")
            self.pb_conectar_controlador.setStyleSheet("background-color: #FF9999;")
            self.pb_setear_cobot.setEnabled(True)
        else:
            self.l_estado_de_conexion.setText("Desconectado")
            self.l_estado_de_conexion.setStyleSheet("color: #c0392b;")
            self.pb_conectar_controlador.setText("Conectar")
            self.pb_conectar_controlador.setStyleSheet("background-color: #99FF99;")
            self.pb_setear_cobot.setEnabled(False)
            
    def estado_seteado_cobot(self, seteado):
        if seteado:
            self.l_seteo_cobot.setText("Cobot seteado !")
            self.l_seteo_cobot.setStyleSheet("color: #27ae60;")
            self.pb_enviar_ordenes.setEnabled(True)
            self.pb_enviar_ordenes.setStyleSheet("background-color: #99FF99;")
            self.le_RPM_cobot.setEnabled(True)

        else:
            self.l_seteo_cobot.setText("Error al setear el Cobot.")
            self.l_seteo_cobot.setStyleSheet("color: #c0392b;") 
            self.pb_enviar_ordenes.setEnabled(False)
            self.pb_enviar_ordenes.setStyleSheet("background-color: #c0392b;")
            self.le_RPM_cobot.setEnabled(False)
    
    def actualizar_pin_enable_y_direccion(self, direccion, enable):
        print(f"Actualizar dirección: {direccion}, Enable: {enable}")
        self.le_pin_direccion_eslabon.setText(str(direccion))
        self.le_pin_enable_eslabon.setText(str(enable))

    
    def mostrar_confirmacion_guardado_cobot(self, exito):
        if exito:
            QMessageBox.information(self, "Éxito", "Cobot guardado correctamente.")
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Warning..")
            msg.setText("No se pudo guardar el Cobot, el nombre está duplicado.")
            btn_forzar = msg.addButton("Forzar guardado", QMessageBox.AcceptRole)
            btn_cancelar = msg.addButton(QMessageBox.Cancel)
            msg.exec_()

            if msg.clickedButton() == btn_forzar:
                self.model.cb.guardar_cobot(self.le_nombre_cobot.text(), True)
           
    def mostrar_actualizacion_eslabon(self, exito):
        if exito:
            QMessageBox.information(self, "Éxito", "Eslavón actualizado correctamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el eslavón. Verifique los datos ingresados.")    
            
    def estado_iniciar_movimiento(self, exito):
        if exito:
            self.pb_iniciar_movimiento.setEnabled(True)
            self.pb_iniciar_movimiento.setStyleSheet("background-color: #99FF99;")
        else:
            QMessageBox.warning(self, "Error",)
            self.pb_iniciar_movimiento.setEnabled(False)
            self.pb_iniciar_movimiento.setStyleSheet("background-color: #c0392b;")
               
    
    def funcionalidad_signals(self):
        self.model.conexion_signal.connect(self.estado_conexion)
        self.model.eslabon_guardado_signal.connect(self.mostrar_actualizacion_eslabon)
        self.model.actualizar_le_direccion_y_enable_signal.connect(self.actualizar_pin_enable_y_direccion)
        self.model.cobot_guardado_signal.connect(self.mostrar_confirmacion_guardado_cobot)
        self.model.cobot_cargado_signal.connect(self.estado_cargado_cobot)
        self.model.cobot_seteado_signal.connect(self.estado_seteado_cobot)
        self.model.estado_iniciar_movimiento_signal.connect(self.estado_iniciar_movimiento)
        self.model.estado_seteo_velocidad_signal.connect(self.estado_seteo_velocidad)
        
    def estado_seteo_velocidad(self, exito):
        if exito:
            QMessageBox.information(self, "Éxito", "Velocidad seteada correctamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo setear la velocidad. Error de input o de conexión.")

    def estado_cargado_cobot(self, exito : bool):
        if exito:
            self.poblar_widgets("init")
            QMessageBox.information(self, "Éxito", "Cobot cargado correctamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo cargar el Cobot. Verifique que el archivo exista y sea válido.")
        
    def validar_line_edits(self):
        todos_llenos = all(le.text().strip() != "" for le in self.lista_line_edits)
        try:
            float(self.le_largo_eslabon.text())
            float(self.le_RPM_cobot.text())
            numericos_validos = True
        except ValueError:
            numericos_validos = False
            QMessageBox.warning(self, "Error", "Los campos numéricos deben ser válidos.")

        self.pb_guardar_eslabon.setEnabled(todos_llenos and numericos_validos)
    
    def funcionalidad_le(self):
        for le in self.lista_line_edits:
            le.textChanged.connect(self.validar_line_edits)
        self.le_RPM_cobot.textChanged.connect(lambda: self.model.set_vel(self.le_RPM_cobot.text()))
        
    def habilitar_deshabilitar_guardado(self):
        if all(le.text() for le in self.lista_line_edits):
            self.pb_guardar_eslabon.setEnabled(True)
        else:
            self.pb_guardar_eslabon.setEnabled(False)

    def actualizar_motor(self):
        if self.pb_seleccion_motor.text() == "Paso a paso":
            self.pb_seleccion_motor.setText("Servo motor")
            self.le_pin_direccion_eslabon.setEnabled(False)
            self.le_pin_enable_eslabon.setEnabled(False)
            self.le_pin_direccion_eslabon.setText("N/A")
            self.le_pin_enable_eslabon.setText("N/A")
        else:
            self.pb_seleccion_motor.setText("Paso a paso")
            self.le_pin_direccion_eslabon.setEnabled(True)
            self.le_pin_enable_eslabon.setEnabled(True)
            self.model.cb.actualizar_eslabon_cambio_motor(str(self.hs_selector_DOF.value())) 
            
    def verificacion_cantidad_movimientos(self):
        if self.lw_lista_movimientos.count() == 0:
            self.pb_remover_movimiento.setEnabled(False)
            self.pb_borrar_todo_movimiento.setEnabled(False)
            self.pb_enviar_ordenes.setEnabled(False)
            self.lw_lista_movimientos.addItem("Sin movimientos asignados.")
        else:
            self.pb_remover_movimiento.setEnabled(True)
            self.pb_borrar_todo_movimiento.setEnabled(True)
            self.pb_enviar_ordenes.setEnabled(True)
            
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
        self.lista_movimientos = [self.lw_lista_movimientos.item(i).text() for i in range(self.lw_lista_movimientos.count())]
        self.verificacion_cantidad_movimientos() 

    def agregar_movimiento_a_lista(self, movimiento):
        if movimiento:
            if self.lw_lista_movimientos.count() == 1 and self.lw_lista_movimientos.item(0).text() == "Sin movimientos asignados.":
                self.lw_lista_movimientos.clear()
            self.lw_lista_movimientos.addItem(movimiento)
            self.lista_movimientos = [self.lw_lista_movimientos.item(i).text() for i in range(self.lw_lista_movimientos.count())]
            self.verificacion_cantidad_movimientos()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el movimiento. Verifique los datos ingresados.")
        
    def abrir_dialogo_movimiento(self):
        self.model.cb.nombres_motores = [eslabon.get("nombre", f"eslabon {num}") for num, eslabon in self.json_ultimo_cobot.get("DOF", {}).items()]
        print(f"Nombres de motores: {self.model.cb.nombres_motores}")
        dialog = DialogMovimiento(self.model.cb.nombres_motores, self)
        dialog.movimiento_nuevo_signal.connect(self.agregar_movimiento_a_lista)
        dialog.exec_()
            
    def enviar_ordenes(self):
        if self.lista_movimientos:
            self.model.enviar_ordenes(self.lista_movimientos, self.condicion_loop,self.le_RPM_cobot.text())
        else:
            QMessageBox.warning(self, "Error", "No hay movimientos para iniciar la rutina.")
            
    def guardar_eslabon(self):
        self.datos_eslabon = {
            "nombre": self.le_nombre_eslabon.text(),
            "largo": float(self.le_largo_eslabon.text()),
            "posicion": [float(v) for v in self.le_posicion_absoluta_eslabon.text().split(",")],
            "motor": {
                "tipo": self.pb_seleccion_motor.text(),
                "pin": int(self.le_pin_pasos_eslabon.text()),
                "direccion": int(self.le_pin_direccion_eslabon.text()),
                "enable": int(self.le_pin_enable_eslabon.text())
            }
        } if self.pb_seleccion_motor.text() == "Paso a paso" else {
            "nombre": self.le_nombre_eslabon.text(),
            "largo": float(self.le_largo_eslabon.text()),
            "posicion": [float(v) for v in self.le_posicion_absoluta_eslabon.text().split(",")],
            "motor": {
                "tipo": self.pb_seleccion_motor.text(),
                "pin": int(self.le_pin_pasos_eslabon.text())
            }
        }
        self.model.cb.guardar_eslabon(str(self.hs_numero_DOF.value()),str(self.hs_selector_DOF.value()), self.datos_eslabon)
  

    def armar_diccionario_cobot_desde_gui_y_json(self):
        return {
            "nombre": self.le_nombre_cobot.text(),
            "descripcion": self.te_descripcion_cobot.toPlainText(),
            "RPM":float(self.le_RPM_cobot.text()),
            "DOF": self.json_ultimo_cobot.get("DOF", {}),
            "movimientos" : self.lista_movimientos
        }

    def guardar_cobot(self):
        datos_cobot = self.armar_diccionario_cobot_desde_gui_y_json()
        self.model.guardar_cobot(datos_cobot["nombre"], False, datos_cobot = datos_cobot)

    def gestionar_cobot(self):
        dialog = DialogGestionarCobots(self.model, self)
        dialog.exec_()
        
    def actualizar_valor_eje(self):
        if self.pb_seleccion_eje.text() == "Eje X":
            self.pb_seleccion_eje.setText("Eje Y")
        elif self.pb_seleccion_eje.text() == "Eje Y":
            self.pb_seleccion_eje.setText("Eje Z")
        else:
            self.pb_seleccion_eje.setText("Eje X")

    def funcionalidad_pb(self):
        self.pb_seleccion_motor.clicked.connect(self.actualizar_motor)
        self.pb_borrar_todo_movimiento.clicked.connect(lambda : self.borrar_movimiento("todo"))
        self.pb_remover_movimiento.clicked.connect(lambda : self.borrar_movimiento("uno"))
        self.pb_agregar_movimiento.clicked.connect(self.abrir_dialogo_movimiento)
        self.pb_enviar_ordenes.clicked.connect(self.enviar_ordenes)
        self.pb_conectar_controlador.clicked.connect(self.model.iniciar_detener_conexion)
        self.pb_setear_cobot.clicked.connect(self.model.setear_eslabones_en_arduino)
        self.pb_guardar_eslabon.clicked.connect(self.guardar_eslabon)
        self.pb_guardar_cobot.clicked.connect(self.guardar_cobot)
        self.pb_gestionar_cobot.clicked.connect(self.gestionar_cobot)
        self.pb_seleccion_eje.clicked.connect(self.actualizar_valor_eje)
        self.pb_iniciar_movimiento.clicked.connect(self.model.iniciar_movimiento)
        
    def funcionalidad_hs(self):
        self.hs_numero_DOF.valueChanged.connect(lambda : self.actualizar_hs(self.hs_numero_DOF, self.l_valor_numero_DOF))
        self.hs_selector_DOF.valueChanged.connect(lambda : self.actualizar_hs(self.hs_selector_DOF, self.l_valor_seleccion_DOF))
        self.habilitar_deshabilitar_guardado()
        
    def actualizar_widgets_seleccion_DOF(self, valor):
        try:
            if str(valor) in self.json_ultimo_cobot.get("DOF", {}):
                eslabon = self.json_ultimo_cobot.get("DOF", {}).get(str(valor), {})
                self.le_largo_eslabon.setText(str(eslabon.get("largo", 0)))
                self.le_nombre_eslabon.setText(eslabon.get("nombre", "Cintura"))
                self.le_RPM_cobot.setText(str(self.json_ultimo_cobot.get("RPM", 3.0)))
                self.pb_seleccion_motor.setText(eslabon.get("motor", {}).get("tipo", "Paso a paso"))
                self.le_pin_pasos_eslabon.setText(str(eslabon.get("motor", {}).get("pin", 0)))
                self.le_posicion_absoluta_eslabon.setText(str(eslabon.get("posicion", "0.0,0.0,0.0")).replace("[", "").replace("]", ""))
                if self.pb_seleccion_motor.text() == "Paso a paso":
                    self.le_pin_direccion_eslabon.setText(str(eslabon.get("motor", {}).get("direccion", 0)))
                    self.le_pin_enable_eslabon.setText(str(eslabon.get("motor", {}).get("enable", 0)))
                else:
                    self.le_pin_direccion_eslabon.setText("N/A")
                    self.le_pin_enable_eslabon.setText("N/A")
                    self.le_pin_direccion_eslabon.setEnabled(False)
                    self.le_pin_enable_eslabon.setEnabled(False)
            else:
                self.le_largo_eslabon.setText("0")
                self.le_nombre_eslabon.setText("setear!")
                self.pb_seleccion_motor.setText("Paso a paso")
                self.le_pin_pasos_eslabon.setText("0")
                self.le_pin_direccion_eslabon.setText("0")
                self.le_pin_enable_eslabon.setText("0")
                self.le_pin_direccion_eslabon.setEnabled(True)
                self.le_pin_enable_eslabon.setEnabled(True)

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
        self.json_ultimo_cobot = self.model.cb.json_ultimo_cobot  
        if self.json_ultimo_cobot:
            if condicion == "init":
                self.le_nombre_cobot.setText(self.json_ultimo_cobot.get("nombre", ""))
                self.te_descripcion_cobot.setText(self.json_ultimo_cobot.get("descripcion", ""))
                self.le_RPM_cobot.setText(str(self.json_ultimo_cobot.get("RPM", 3)))
                self.hs_numero_DOF.setValue(len(self.json_ultimo_cobot.get("DOF", [])))
                self.l_valor_numero_DOF.setText(str(self.hs_numero_DOF.value()))
                self.hs_selector_DOF.setMaximum(len(self.json_ultimo_cobot.get("DOF", [])))
                self.hs_selector_DOF.setMinimum(1)

                self.valor_selector_DOF = str(self.hs_selector_DOF.value())
                self.l_valor_seleccion_DOF.setText(self.valor_selector_DOF)

                self.le_largo_eslabon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("largo", 1111)))
                self.pb_seleccion_motor.setText(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("tipo", "Paso a paso"))
                self.le_nombre_eslabon.setText(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("nombre", "Cintura"))
                self.le_posicion_absoluta_eslabon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("posicion", "0.0,0.0,0.0")).replace("[", "").replace("]", ""))
                if self.pb_seleccion_motor.text() == "Paso a paso":
                    self.le_pin_direccion_eslabon.setEnabled(True)
                    self.le_pin_enable_eslabon.setEnabled(True)
                    self.le_pin_direccion_eslabon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("direccion", 0)))
                    self.le_pin_enable_eslabon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("enable", 0)))
                else:
                    self.le_pin_direccion_eslabon.setEnabled(False)
                    self.le_pin_enable_eslabon.setEnabled(False)
                    self.le_pin_direccion_eslabon.setText("N/A")
                    self.le_pin_enable_eslabon.setText("N/A")
                self.le_pin_pasos_eslabon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("pin", 0)))
                if self.json_ultimo_cobot.get("movimientos", []) != []:
                    self.lista_movimientos = [movimiento for movimiento in self.json_ultimo_cobot.get("movimientos")]
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