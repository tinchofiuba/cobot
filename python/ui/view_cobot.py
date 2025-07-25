
from .default_cobot import Ui_Dialog
from ..model.model_cobot import ModelCobot
from .agregar_movimientos import Ui_Dialog as Ui_Dialog_Movimiento
from .gestionar_cobots import Ui_Dialog as Ui_Dialog_GestionarCobots

from PyQt5.QtWidgets import QDialog, QMessageBox, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QTimer


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
        self.pb_borrar_cobot.clicked.connect(lambda : self.model.borrar_cobot(self.lw_cobots_guardados.currentItem().text()))
        self.pb_cargar_cobot.clicked.connect(lambda : self.model.cargar_cobot(self.lw_cobots_guardados.currentItem().text()))

    def mostrar_descripcion_cobot(self, row):
        if 0 <= row < len(self.lista_descripciones):
            self.te_descripcion_cobot.setPlainText(self.lista_descripciones[row])
        else:
            self.te_descripcion_cobot.clear()
        
    def funcionalidad_lw(self):
        self.lw_cobots_guardados.currentRowChanged.connect(self.mostrar_descripcion_cobot)
        
    def config_iniciales(self):
        self.model.cargar_datos_cobots()
        self.te_descripcion_cobot.setStyleSheet("font-size: 12px;")
        
    def cobot_borrado(self, condicion : bool):
        if condicion:
            QMessageBox.information(self, "Éxito", "Cobot borrado correctamente.")
            self.model.cargar_datos_cobots()

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
    lista_movimientos_posibles = ["Mover a", "A origen", "Begin loop", "End loop"]
    
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
                self.l_x.setText("Pasos")  # Cambia el texto del label de manera dinámica
                self.l_y.setText("d_useg")  # Cambia el texto del label de manera dinámica
                self.l_z.setText("dir") # Cambia el texto del label de manera dinámica
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
        if self.pb_seleccion_movimiento.text() == "Girar base":
            vector = f"({self.le_x.text()},{self.le_y.text()},{self.le_z.text()})"
        elif self.pb_seleccion_movimiento.text() == "Loop" or self.pb_seleccion_movimiento.text() == "Endloop":
            vector = ""
        else:
            vector = f"({self.le_x.text()},{self.le_y.text()},{self.le_z.text()})"
        if self.le_delay.text() != "":
            delay = f"d{self.le_delay.text()}"
            self.movimiento = f"{self.pb_seleccion_movimiento.text()}-{vector}-{delay}"
        else:
            self.movimiento = f"{self.pb_seleccion_movimiento.text()}-{vector}-d0"
            
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
        
class view(Ui_Dialog, QDialog):
    
    def __init__(self, parent=None):
        super(view, self).__init__(parent)
        self.setupUi(self)
        self.lista_line_edits = [self.le_nombre_cobot, self.le_nombre_eslavon, self.le_largo_eslavon, self.le_angulo_minimo_eslavon, self.le_pin_pasos_eslavon, self.le_pin_direccion_eslavon, self.le_pin_enable_eslavon]
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
    
    def actualizar_pin_enable_y_direccion(self, direccion, enable):
        print(f"Actualizar dirección: {direccion}, Enable: {enable}")
        self.le_pin_direccion_eslavon.setText(str(direccion))
        self.le_pin_enable_eslavon.setText(str(enable))

    
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
                self.model.guardar_cobot(self.le_nombre_cobot.text(), True)
           
    def mostrar_actualizacion_eslavon(self, exito):
        if exito:
            QMessageBox.information(self, "Éxito", "Eslavón actualizado correctamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el eslavón. Verifique los datos ingresados.")       
    
    def funcionalidad_signals(self):
        self.model.conexion_signal.connect(self.estado_conexion)
        self.model.eslavon_guardado_signal.connect(self.mostrar_actualizacion_eslavon)
        self.model.actualizar_le_direccion_y_enable_signal.connect(self.actualizar_pin_enable_y_direccion)
        self.model.cobot_guardado_signal.connect(self.mostrar_confirmacion_guardado_cobot)
        self.model.cobot_cargado_signal.connect(self.confirmacion_cargado_cobot)
        
    def confirmacion_cargado_cobot(self, exito : bool):
        if exito:
            self.poblar_widgets("init")
            QMessageBox.information(self, "Éxito", "Cobot cargado correctamente.")
        else:
            QMessageBox.warning(self, "Error", "No se pudo cargar el Cobot. Verifique que el archivo exista y sea válido.")
        
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
            self.le_pin_direccion_eslavon.setEnabled(False)
            self.le_pin_enable_eslavon.setEnabled(False)
            self.le_pin_direccion_eslavon.setText("N/A")
            self.le_pin_enable_eslavon.setText("N/A")
        else:
            self.pb_seleccion_motor.setText("Paso a paso")
            self.le_pin_direccion_eslavon.setEnabled(True)
            self.le_pin_enable_eslavon.setEnabled(True)
            self.model.actualizar_eslavon_cambio_motor(str(self.hs_selector_DOF.value())) 
            
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
        self.model.nombres_motores = [eslavon.get("nombre", f"Eslavon {num}") for num, eslavon in self.json_ultimo_cobot.get("DOF", {}).items()]
        print(f"Nombres de motores: {self.model.nombres_motores}")
        dialog = DialogMovimiento(self.model.nombres_motores, self)
        dialog.movimiento_nuevo_signal.connect(self.agregar_movimiento_a_lista)
        dialog.exec_()
            
    def enviar_ordenes(self):
        if self.lista_movimientos:
            self.model.enviar_ordenes(self.lista_movimientos, self.condicion_loop)
        else:
            QMessageBox.warning(self, "Error", "No hay movimientos para iniciar la rutina.")
            
    def guardar_eslavon(self):
        self.datos_eslavon = {
            "nombre": self.le_nombre_eslavon.text(),
            "largo": float(self.le_largo_eslavon.text()),
            "motor": {
                "tipo": self.pb_seleccion_motor.text(),
                "pin": int(self.le_pin_pasos_eslavon.text()),
                "direccion": int(self.le_pin_direccion_eslavon.text()),
                "enable": int(self.le_pin_enable_eslavon.text()),
                "angulo_minimo": float(self.le_angulo_minimo_eslavon.text())
            }
        } if self.pb_seleccion_motor.text() == "Paso a paso" else {
            "nombre": self.le_nombre_eslavon.text(),
            "largo": float(self.le_largo_eslavon.text()),
            "motor": {
                "tipo": self.pb_seleccion_motor.text(),
                "pin": int(self.le_pin_pasos_eslavon.text()),
                "angulo_minimo": float(self.le_angulo_minimo_eslavon.text())
            }
        }
        self.model.guardar_eslavon(str(self.hs_numero_DOF.value()),str(self.hs_selector_DOF.value()), self.datos_eslavon)
  

    def armar_diccionario_cobot_desde_gui_y_json(self):
        return {
            "nombre": self.le_nombre_cobot.text(),
            "descripcion": self.te_descripcion_cobot.toPlainText(),
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
        self.pb_setear_cobot.clicked.connect(lambda : self.model.setear_cobot_en_arduino())
        self.pb_guardar_eslavon.clicked.connect(self.guardar_eslavon)
        self.pb_guardar_cobot.clicked.connect(self.guardar_cobot)
        self.pb_gestionar_cobot.clicked.connect(self.gestionar_cobot)
        self.pb_seleccion_eje.clicked.connect(self.actualizar_valor_eje)
        
    def funcionalidad_hs(self):
        self.hs_numero_DOF.valueChanged.connect(lambda : self.actualizar_hs(self.hs_numero_DOF, self.l_valor_numero_DOF))
        self.hs_selector_DOF.valueChanged.connect(lambda : self.actualizar_hs(self.hs_selector_DOF, self.l_valor_seleccion_DOF))
        self.habilitar_deshabilitar_guardado()
        
    def actualizar_widgets_seleccion_DOF(self, valor):
        try:
            if str(valor) in self.json_ultimo_cobot.get("DOF", {}):
                eslavon = self.json_ultimo_cobot.get("DOF", {}).get(str(valor), {})
                self.le_largo_eslavon.setText(str(eslavon.get("largo", 0)))
                self.le_nombre_eslavon.setText(eslavon.get("nombre", "Cintura"))
                self.le_angulo_minimo_eslavon.setText(str(eslavon.get("angulo_minimo", 1.8)))
                self.pb_seleccion_motor.setText(eslavon.get("motor", {}).get("tipo", "Paso a paso"))
                self.le_pin_pasos_eslavon.setText(str(eslavon.get("motor", {}).get("pin", 0)))
                if self.pb_seleccion_motor.text() == "Paso a paso":
                    self.le_pin_direccion_eslavon.setText(str(eslavon.get("motor", {}).get("direccion", 0)))
                    self.le_pin_enable_eslavon.setText(str(eslavon.get("motor", {}).get("enable", 0)))
                else:
                    self.le_pin_direccion_eslavon.setText("N/A")
                    self.le_pin_enable_eslavon.setText("N/A")
                    self.le_pin_direccion_eslavon.setEnabled(False)
                    self.le_pin_enable_eslavon.setEnabled(False)
            else:
                self.le_largo_eslavon.setText("0")
                self.le_nombre_eslavon.setText("setear!")
                self.le_angulo_minimo_eslavon.setText("1.8")
                self.pb_seleccion_motor.setText("Paso a paso")
                self.le_pin_pasos_eslavon.setText("0")
                self.le_pin_direccion_eslavon.setText("0")
                self.le_pin_enable_eslavon.setText("0")
                self.le_pin_direccion_eslavon.setEnabled(True)
                self.le_pin_enable_eslavon.setEnabled(True)

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
        self.json_ultimo_cobot = self.model.json_ultimo_cobot  
        if self.json_ultimo_cobot:
            if condicion == "init":
                self.le_nombre_cobot.setText(self.json_ultimo_cobot.get("nombre", ""))
                self.te_descripcion_cobot.setText(self.json_ultimo_cobot.get("descripcion", ""))
                self.hs_numero_DOF.setValue(len(self.json_ultimo_cobot.get("DOF", [])))
                self.l_valor_numero_DOF.setText(str(self.hs_numero_DOF.value()))
                self.hs_selector_DOF.setMaximum(len(self.json_ultimo_cobot.get("DOF", [])))
                self.hs_selector_DOF.setMinimum(1)

                self.valor_selector_DOF = str(self.hs_selector_DOF.value())
                self.l_valor_seleccion_DOF.setText(self.valor_selector_DOF)

                self.le_largo_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("largo", 1111)))
                self.pb_seleccion_motor.setText(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("tipo", "Paso a paso"))
                self.le_angulo_minimo_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("angulo_minimo", 1)))
                self.le_nombre_eslavon.setText(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("nombre", "Cintura"))
                if self.pb_seleccion_motor.text() == "Paso a paso":
                    self.le_pin_direccion_eslavon.setEnabled(True)
                    self.le_pin_enable_eslavon.setEnabled(True)
                    self.le_pin_direccion_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("direccion", 0)))
                    self.le_pin_enable_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("enable", 0)))
                else:
                    self.le_pin_direccion_eslavon.setEnabled(False)
                    self.le_pin_enable_eslavon.setEnabled(False)
                    self.le_pin_direccion_eslavon.setText("N/A")
                    self.le_pin_enable_eslavon.setText("N/A")
                self.le_pin_pasos_eslavon.setText(str(self.json_ultimo_cobot.get("DOF", {}).get(self.valor_selector_DOF, {}).get("motor", {}).get("pin", 0)))
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