import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QPushButton, QSlider
from mainform import Ui_main_ui

class CameraPageWindow(QDialog,Ui_main_ui):
    
    returnSignal = pyqtSignal()
    
    def __init__(self,parent=None):
        
        super(CameraPageWindow, self).__init__(parent)
        self.cap = cv2.VideoCapture() 
        self.CAM_NUM = 0
        self.setupUi(self)
        self.initUI()
        self.slot_init()

    def initUI(self):
        
        self.setLayout(self.gridLayout)

    def slot_init(self):
        
        self.timer_camera.timeout.connect(self.show_camera)
        self.cameraButton.clicked.connect(self.slotCameraButton)

    def show_camera(self):
        
        flag,self.image = self.cap.read()
        show = cv2.resize(self.image,(480,360))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        self.cameraLabel.setPixmap(QPixmap.fromImage(showImage))
    

    def slotCameraButton(self):
        
        if self.timer_camera.isActive() == False:
            self.openCamera()
        else:
            self.closeCamera()

    def openCamera(self):
        
        flag = self.cap.open(self.CAM_NUM)
        
        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'Please Check Your Connection!!',
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok)
            
        else:
            self.timer_camera.start(30)
            self.cameraButton.setText('Cam Off')

    def closeCamera(self):
        
        self.timer_camera.stop()
        self.cap.release()
        self.cameraLabel.clear()
        self.cameraButton.setText('Cam On')

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = CameraPageWindow()
    
    window.show()
    sys.exit(app.exec_())