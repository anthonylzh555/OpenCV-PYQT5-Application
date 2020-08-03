# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multitask_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_main_ui(object):
    def setupUi(self, main_ui):
        
        main_ui.setObjectName("main_ui")
        main_ui.setWindowModality(QtCore.Qt.NonModal)
        main_ui.resize(800, 600)
        main_ui.setSizeGripEnabled(True)
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(main_ui)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 530, 761, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.btn_cameraon = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_cameraon.setObjectName("btn_cameraon")
        self.horizontalLayout.addWidget(self.btn_cameraon)
        self.btn_save = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_save.setObjectName("btn_save")
        self.horizontalLayout.addWidget(self.btn_save)
        self.btn_rect = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_rect.setObjectName("btn_rect")
        self.horizontalLayout.addWidget(self.btn_rect)
        self.btn_corp = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_corp.setObjectName("btn_corp")
        self.horizontalLayout.addWidget(self.btn_corp)
        self.btn_process = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_process.setObjectName("btn_process")
        self.horizontalLayout.addWidget(self.btn_process)
        self.btn_quit = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayout.addWidget(self.btn_quit)
        
        self.gridLayoutWidget = QtWidgets.QWidget(main_ui)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 761, 431))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label_thresholdimg = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_thresholdimg.setObjectName("label_thresholdimg")
        self.gridLayout.addWidget(self.label_thresholdimg, 1, 1, 1, 1)
        
        self.label_corpimg = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_corpimg.setObjectName("label_corpimg")
        self.gridLayout.addWidget(self.label_corpimg, 1, 0, 1, 1)
        
        self.label_processedimg = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_processedimg.setObjectName("label_processedimg")
        self.gridLayout.addWidget(self.label_processedimg, 0, 1, 1, 1)
        
        self.label_regularimg = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_regularimg.setObjectName("label_regularimg")
        self.gridLayout.addWidget(self.label_regularimg, 0, 0, 1, 1)
        
        self.Slider_threshold = QtWidgets.QSlider(main_ui)
        self.Slider_threshold.setGeometry(QtCore.QRect(500, 480, 141, 30))
        self.Slider_threshold.setMaximum(255)
        self.Slider_threshold.setOrientation(QtCore.Qt.Horizontal)
        self.Slider_threshold.setObjectName("Slider_threshold")
        
        self.verticalLayoutWidget = QtWidgets.QWidget(main_ui)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(660, 460, 121, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_rate = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_rate.setObjectName("label_rate")
        self.verticalLayout_2.addWidget(self.label_rate)
        self.label_threshold = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_threshold.setObjectName("label_threshold")
        self.verticalLayout_2.addWidget(self.label_threshold)

        self.retranslateUi(main_ui)
        
        self.Slider_threshold.valueChanged['int'].connect(self.label_threshold.setNum)
        self.btn_cameraon.clicked.connect(main_ui.btnCamOn_clicked)
        QtCore.QMetaObject.connectSlotsByName(main_ui)

    def retranslateUi(self, main_ui):
        
        _translate = QtCore.QCoreApplication.translate
        main_ui.setWindowTitle(_translate("main_ui", "Threshold Rate app"))
        self.btn_cameraon.setText(_translate("main_ui", " Cam On"))
        self.btn_save.setText(_translate("main_ui", "Save"))
        self.btn_rect.setText(_translate("main_ui", "Rect"))
        self.btn_corp.setText(_translate("main_ui", "Corp"))
        self.btn_process.setText(_translate("main_ui", "Process"))
        self.btn_quit.setText(_translate("main_ui", "Quit"))
        self.label_thresholdimg.setText(_translate("main_ui", "Threshold Image"))
        self.label_corpimg.setText(_translate("main_ui", "Corp Image"))
        self.label_processedimg.setText(_translate("main_ui", "Processed Image"))
        self.label_regularimg.setText(_translate("main_ui", "Regular Image"))
        self.label_rate.setText(_translate("main_ui", "Rate : 0"))
        self.label_threshold.setText(_translate("main_ui", "TextLabel : 0"))

        
