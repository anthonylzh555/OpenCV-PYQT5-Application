from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from webcam_ui_test import Ui_CameraPage
import numpy as np
import cv2

class CameraPageWindow(QWidget,Ui_CameraPage):
    
    returnSignal = pyqtSignal()
    
    def __init__(self,parent=None):
        
        super(CameraPageWindow, self).__init__(parent)
        self.timer_camera = QTimer() #初始化定时器
        self.cap = cv2.VideoCapture() #初始化摄像头
        self.CAM_NUM = 0
        self.setupUi(self)
        self.initUI()
        self.slot_init()

    def initUI(self):
        
        self.setLayout(self.gridLayout)

    def slot_init(self):
        
        self.timer_camera.timeout.connect(self.show_camera)
        #信号和槽连接
        self.cameraButton.clicked.connect(self.slotCameraButton)

    def show_camera(self):
        
        flag,self.image = self.cap.read()
        show = cv2.resize(self.image,(480,360))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        self.cameraLabel.setPixmap(QPixmap.fromImage(showImage))
    
    #打开关闭摄像头控制
    def slotCameraButton(self):
        
        if self.timer_camera.isActive() == False:
            #打开摄像头并显示图像信息
            self.openCamera()
        else:
            #关闭摄像头并清空显示信息
            self.closeCamera()

    #打开摄像头
    def openCamera(self):
        
        flag = self.cap.open(self.CAM_NUM)
        
        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'請檢察相機是連接',
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok)
            
        else:
            self.timer_camera.start(30)
            self.cameraButton.setText('關閉攝影機')

    #关闭摄像头
    def closeCamera(self):
        
        self.timer_camera.stop()
        self.cap.release()
        self.cameraLabel.clear()
        self.cameraButton.setText('打開攝影機')

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = CameraPageWindow()
    
    window.show()
    sys.exit(app.exec_())