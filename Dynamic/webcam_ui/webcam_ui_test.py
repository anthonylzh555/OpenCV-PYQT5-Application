# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_CameraPage(object):
    
    def setupUi(self, CameraPage):
        
        CameraPage.setObjectName("CameraPage")
        CameraPage.resize(800, 600)
        
        self.layoutWidget = QtWidgets.QWidget(CameraPage)
        self.layoutWidget.setGeometry(100,100,800,600)
        self.layoutWidget.setObjectName("layoutWidget")
        
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setObjectName("gridLayout")
        
        self.cameraButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cameraButton.setFont(font)
        self.cameraButton.setObjectName("cameraButton")
        self.gridLayout.addWidget(self.cameraButton, 0, 1, 1, 1)
        
        self.cameraLabel = QtWidgets.QLabel(self.layoutWidget)
        self.cameraLabel.setMinimumSize(QtCore.QSize(480, 320))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cameraLabel.setFont(font)
        self.cameraLabel.setObjectName("cameraLabel")
        self.gridLayout.addWidget(self.cameraLabel, 0, 3, 1, 1)

        self.retranslateUi(CameraPage)
        QtCore.QMetaObject.connectSlotsByName(CameraPage)

    def retranslateUi(self, CameraPage):
        _translate = QtCore.QCoreApplication.translate
        CameraPage.setWindowTitle(_translate("CameraPage", "Camera Interface"))
        self.cameraButton.setText(_translate("CameraPage", "Camera On"))
        self.cameraLabel.setText(_translate("CameraPage", "Camera "))
        
        
