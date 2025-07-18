# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'default_cobot.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 575)
        self.groupBox_movimientos = QtWidgets.QGroupBox(Dialog)
        self.groupBox_movimientos.setGeometry(QtCore.QRect(250, 10, 211, 451))
        self.groupBox_movimientos.setObjectName("groupBox_movimientos")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_movimientos)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 196, 411))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lw_lista_movimientos = QtWidgets.QListWidget(self.layoutWidget)
        self.lw_lista_movimientos.setMinimumSize(QtCore.QSize(190, 250))
        self.lw_lista_movimientos.setMaximumSize(QtCore.QSize(190, 250))
        self.lw_lista_movimientos.setObjectName("lw_lista_movimientos")
        self.verticalLayout.addWidget(self.lw_lista_movimientos)
        self.pb_agregar_movimiento = QtWidgets.QPushButton(self.layoutWidget)
        self.pb_agregar_movimiento.setMinimumSize(QtCore.QSize(150, 30))
        self.pb_agregar_movimiento.setMaximumSize(QtCore.QSize(190, 30))
        self.pb_agregar_movimiento.setObjectName("pb_agregar_movimiento")
        self.verticalLayout.addWidget(self.pb_agregar_movimiento)
        self.pb_remover_movimiento = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.pb_remover_movimiento.sizePolicy().hasHeightForWidth())
        self.pb_remover_movimiento.setSizePolicy(sizePolicy)
        self.pb_remover_movimiento.setMinimumSize(QtCore.QSize(150, 30))
        self.pb_remover_movimiento.setMaximumSize(QtCore.QSize(190, 30))
        self.pb_remover_movimiento.setObjectName("pb_remover_movimiento")
        self.verticalLayout.addWidget(self.pb_remover_movimiento)
        self.pb_borrar_todo_movimiento = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(150)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.pb_borrar_todo_movimiento.sizePolicy().hasHeightForWidth())
        self.pb_borrar_todo_movimiento.setSizePolicy(sizePolicy)
        self.pb_borrar_todo_movimiento.setMinimumSize(QtCore.QSize(150, 30))
        self.pb_borrar_todo_movimiento.setMaximumSize(QtCore.QSize(190, 30))
        self.pb_borrar_todo_movimiento.setObjectName("pb_borrar_todo_movimiento")
        self.verticalLayout.addWidget(self.pb_borrar_todo_movimiento)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(38, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.pb_iniciar_rutina = QtWidgets.QPushButton(self.layoutWidget)
        self.pb_iniciar_rutina.setObjectName("pb_iniciar_rutina")
        self.horizontalLayout_3.addWidget(self.pb_iniciar_rutina)
        spacerItem1 = QtWidgets.QSpacerItem(38, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.groupBox_config_cobot = QtWidgets.QGroupBox(Dialog)
        self.groupBox_config_cobot.setGeometry(QtCore.QRect(10, 10, 231, 451))
        self.groupBox_config_cobot.setObjectName("groupBox_config_cobot")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_config_cobot)
        self.groupBox.setGeometry(QtCore.QRect(10, 30, 211, 180))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 180))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 11, 194, 167))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 19))
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_6.addWidget(self.label_11)
        self.le_nombre_cobot = QtWidgets.QLineEdit(self.layoutWidget1)
        self.le_nombre_cobot.setMaximumSize(QtCore.QSize(130, 27))
        self.le_nombre_cobot.setObjectName("le_nombre_cobot")
        self.horizontalLayout_6.addWidget(self.le_nombre_cobot)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_12.setMaximumSize(QtCore.QSize(16777215, 19))
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.te_descripcion_cobot = QtWidgets.QTextEdit(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.te_descripcion_cobot.sizePolicy().hasHeightForWidth())
        self.te_descripcion_cobot.setSizePolicy(sizePolicy)
        self.te_descripcion_cobot.setMinimumSize(QtCore.QSize(190, 50))
        self.te_descripcion_cobot.setMaximumSize(QtCore.QSize(190, 88))
        self.te_descripcion_cobot.setObjectName("te_descripcion_cobot")
        self.verticalLayout_3.addWidget(self.te_descripcion_cobot)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_17.setMaximumSize(QtCore.QSize(16777215, 19))
        self.label_17.setObjectName("label_17")
        self.verticalLayout_4.addWidget(self.label_17)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.hs_numero_DOF = QtWidgets.QSlider(self.layoutWidget1)
        self.hs_numero_DOF.setMaximumSize(QtCore.QSize(143, 16777215))
        self.hs_numero_DOF.setMinimum(1)
        self.hs_numero_DOF.setMaximum(6)
        self.hs_numero_DOF.setOrientation(QtCore.Qt.Horizontal)
        self.hs_numero_DOF.setObjectName("hs_numero_DOF")
        self.horizontalLayout_8.addWidget(self.hs_numero_DOF)
        self.l_valor_numero_DOF = QtWidgets.QLabel(self.layoutWidget1)
        self.l_valor_numero_DOF.setMinimumSize(QtCore.QSize(30, 20))
        self.l_valor_numero_DOF.setMaximumSize(QtCore.QSize(50, 20))
        self.l_valor_numero_DOF.setAlignment(QtCore.Qt.AlignCenter)
        self.l_valor_numero_DOF.setObjectName("l_valor_numero_DOF")
        self.horizontalLayout_8.addWidget(self.l_valor_numero_DOF)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_config_cobot)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 210, 211, 181))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 231))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget2.setGeometry(QtCore.QRect(11, 60, 189, 114))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_2.setMinimumSize(QtCore.QSize(80, 20))
        self.label_2.setMaximumSize(QtCore.QSize(80, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_3.setMinimumSize(QtCore.QSize(80, 20))
        self.label_3.setMaximumSize(QtCore.QSize(80, 20))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.le_largo_eslavon = QtWidgets.QLineEdit(self.layoutWidget2)
        self.le_largo_eslavon.setObjectName("le_largo_eslavon")
        self.gridLayout.addWidget(self.le_largo_eslavon, 1, 0, 1, 1)
        self.pb_seleccion_motor = QtWidgets.QPushButton(self.layoutWidget2)
        self.pb_seleccion_motor.setObjectName("pb_seleccion_motor")
        self.gridLayout.addWidget(self.pb_seleccion_motor, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_4.setMinimumSize(QtCore.QSize(60, 20))
        self.label_4.setMaximumSize(QtCore.QSize(80, 20))
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_5.setMinimumSize(QtCore.QSize(60, 20))
        self.label_5.setMaximumSize(QtCore.QSize(80, 20))
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 1, 1, 1)
        self.le_angulo_minimo_eslavon = QtWidgets.QLineEdit(self.layoutWidget2)
        self.le_angulo_minimo_eslavon.setText("")
        self.le_angulo_minimo_eslavon.setObjectName("le_angulo_minimo_eslavon")
        self.gridLayout.addWidget(self.le_angulo_minimo_eslavon, 3, 0, 1, 1)
        self.le_nombre_eslavon = QtWidgets.QLineEdit(self.layoutWidget2)
        self.le_nombre_eslavon.setText("")
        self.le_nombre_eslavon.setObjectName("le_nombre_eslavon")
        self.gridLayout.addWidget(self.le_nombre_eslavon, 3, 1, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget3.setGeometry(QtCore.QRect(12, 31, 181, 22))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hs_selector_DOF = QtWidgets.QSlider(self.layoutWidget3)
        self.hs_selector_DOF.setMaximumSize(QtCore.QSize(143, 16777215))
        self.hs_selector_DOF.setMinimum(1)
        self.hs_selector_DOF.setMaximum(6)
        self.hs_selector_DOF.setOrientation(QtCore.Qt.Horizontal)
        self.hs_selector_DOF.setObjectName("hs_selector_DOF")
        self.horizontalLayout.addWidget(self.hs_selector_DOF)
        self.l_valor_seleccion_DOF = QtWidgets.QLabel(self.layoutWidget3)
        self.l_valor_seleccion_DOF.setMinimumSize(QtCore.QSize(30, 20))
        self.l_valor_seleccion_DOF.setMaximumSize(QtCore.QSize(50, 20))
        self.l_valor_seleccion_DOF.setAlignment(QtCore.Qt.AlignCenter)
        self.l_valor_seleccion_DOF.setObjectName("l_valor_seleccion_DOF")
        self.horizontalLayout.addWidget(self.l_valor_seleccion_DOF)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_config_cobot)
        self.groupBox_3.setGeometry(QtCore.QRect(11, 390, 207, 51))
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 51))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 10, 191, 29))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.cargar_cobot = QtWidgets.QPushButton(self.layoutWidget4)
        self.cargar_cobot.setObjectName("cargar_cobot")
        self.horizontalLayout_7.addWidget(self.cargar_cobot)
        self.pb_guardar_eslavon = QtWidgets.QPushButton(self.layoutWidget4)
        self.pb_guardar_eslavon.setObjectName("pb_guardar_eslavon")
        self.horizontalLayout_7.addWidget(self.pb_guardar_eslavon)
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 460, 451, 111))
        self.groupBox_4.setObjectName("groupBox_4")
        self.pb_tipo_controlador = QtWidgets.QPushButton(self.groupBox_4)
        self.pb_tipo_controlador.setGeometry(QtCore.QRect(10, 30, 101, 27))
        self.pb_tipo_controlador.setObjectName("pb_tipo_controlador")
        self.pb_conectar_controlador = QtWidgets.QPushButton(self.groupBox_4)
        self.pb_conectar_controlador.setGeometry(QtCore.QRect(10, 70, 101, 27))
        self.pb_conectar_controlador.setObjectName("pb_conectar_controlador")
        self.l_estado_de_conexion = QtWidgets.QLabel(self.groupBox_4)
        self.l_estado_de_conexion.setGeometry(QtCore.QRect(130, 75, 161, 19))
        self.l_estado_de_conexion.setObjectName("l_estado_de_conexion")
        self.pb_setear_cobot = QtWidgets.QPushButton(self.groupBox_4)
        self.pb_setear_cobot.setGeometry(QtCore.QRect(120, 30, 160, 27))
        self.pb_setear_cobot.setMaximumSize(QtCore.QSize(160, 27))
        self.pb_setear_cobot.setObjectName("pb_setear_cobot")
        self.l_seteo_cobot = QtWidgets.QLabel(self.groupBox_4)
        self.l_seteo_cobot.setGeometry(QtCore.QRect(290, 33, 161, 19))
        self.l_seteo_cobot.setObjectName("l_seteo_cobot")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Cobot"))
        self.groupBox_movimientos.setTitle(_translate("Dialog", "Movimientos programados"))
        self.pb_agregar_movimiento.setText(_translate("Dialog", "Agregar movimiento"))
        self.pb_remover_movimiento.setText(_translate("Dialog", "Remover movimiento"))
        self.pb_borrar_todo_movimiento.setText(_translate("Dialog", "Borrar todo"))
        self.pb_iniciar_rutina.setText(_translate("Dialog", "Inciar rutina"))
        self.groupBox_config_cobot.setTitle(_translate("Dialog", "Configurar Cobot"))
        self.label_11.setText(_translate("Dialog", "Nombre: "))
        self.label_12.setText(_translate("Dialog", "Descripción"))
        self.label_17.setText(_translate("Dialog", "Número de eslavones"))
        self.l_valor_numero_DOF.setText(_translate("Dialog", "3"))
        self.groupBox_2.setTitle(_translate("Dialog", "Configuraciones eslavones"))
        self.label_2.setText(_translate("Dialog", "Largo [mm]"))
        self.label_3.setText(_translate("Dialog", "Tipo motor"))
        self.le_largo_eslavon.setText(_translate("Dialog", "150.12"))
        self.pb_seleccion_motor.setText(_translate("Dialog", "Paso a paso"))
        self.label_4.setText(_translate("Dialog", "º mínimo"))
        self.label_5.setText(_translate("Dialog", "Nombre"))
        self.l_valor_seleccion_DOF.setText(_translate("Dialog", "3"))
        self.cargar_cobot.setText(_translate("Dialog", "Cargar"))
        self.pb_guardar_eslavon.setText(_translate("Dialog", "Guardar"))
        self.groupBox_4.setTitle(_translate("Dialog", "Conexion serial"))
        self.pb_tipo_controlador.setText(_translate("Dialog", "Arduino"))
        self.pb_conectar_controlador.setText(_translate("Dialog", "Conectar"))
        self.l_estado_de_conexion.setText(_translate("Dialog", "Desconectado"))
        self.pb_setear_cobot.setText(_translate("Dialog", "Setear"))
        self.l_seteo_cobot.setText(_translate("Dialog", "cobot aún no seateado"))
