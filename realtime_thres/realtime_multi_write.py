import sys
import cv2
import numpy as np
import os
from configparser import ConfigParser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5.QtCore import QRect, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QPushButton, QSlider, QMessageBox

def qtpixmap_to_cvimg(qtpixmap):
    """ transform qtImage into numpy array ( regular image) """
    qimg = qtpixmap.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]
    return result


class mainUI(QDialog):
    """ deployment of the user interface """
    
    def __init__(self):
        """ initialize the parameter and numpy array to save photoes """
        super().__init__()
        self.initUI()
        
        self.img_regular = np.ndarray(())
        self.img_corp = np.ndarray(())
        self.img_processed = np.ndarray(())
        self.img_threshold = np.ndarray(())
        
        self.threshold_value = 0

        self.camera = cv2.VideoCapture()
        self.CAM_NUM = 0  # Set Camera num
        
        self.camera_timer = QtCore.QTimer()
        self.camera_timer.timeout.connect(self.queryFrame)
        self.corp_timer = QtCore.QTimer()
        self.corp_timer.timeout.connect(self.cropImg)
        self.corp_timer.timeout.connect(self.thres_img)
        

    def initUI(self):
        """ deifine the component of the user interface """
        # Define Size
        self.setGeometry(50,50,600,500)
        self.setWindowTitle('Load Image')

        # Define Buttum
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnRect = QPushButton('Rect', self)
        self.btnCrop = QPushButton('Corp', self)
        self.btnSaveParam = QPushButton('Save Param', self)
        self.btnLoadParam = QPushButton('Load Param', self)
        self.btnQuit = QPushButton('Quit', self)

        # Define Label
        self.label_regulerImg_sign = QLabel("Reguler Image : ")
        self.label_roiImg_sign = QLabel("ROI Image : ")
        self.label_thresImg_sign = QLabel("Threshold Image : ")
        self.label_overlapImg_sign = QLabel("Overlap : ")
        
        
        self.label_regularImg = CutImage(self)
        self.label_processedImg = QLabel("Processed img")
        self.label_thresholdImg = QLabel("Threshold img")
        self.label_overlapImg = QLabel("Overlapping img")
        self.label_threshold = QLabel("threshold: 0 ",self)
        self.label_thresholdrate = QLabel("佔比率 : 0 ",self)
        
        # Define Slider
        self.threshold_slider = QSlider(Qt.Horizontal,self)  
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.valueChanged[int].connect(self.changevalue)

        # Layout
        layout = QGridLayout(self)
        layout.addWidget(self.label_regulerImg_sign, 1, 1, 1, 1)
        layout.addWidget(self.label_regularImg, 2, 1, 2, 3)    # (y,x,yspan,xspan)
        layout.addWidget(self.label_roiImg_sign, 4, 1, 1, 1)
        layout.addWidget(self.label_processedImg, 5, 1, 2, 3)
        layout.addWidget(self.label_thresImg_sign, 1, 4, 1, 1)
        layout.addWidget(self.label_thresholdImg, 2, 4, 2, 3)
        layout.addWidget(self.label_overlapImg_sign, 4, 4, 1, 1)
        layout.addWidget(self.label_overlapImg, 5, 4, 2, 3)
        
        layout.addWidget(self.label_threshold, 8, 7, 1, 1) 
        layout.addWidget(self.label_thresholdrate, 7, 7, 1, 1) 
        
        layout.addWidget(self.btnOpen, 9, 1, 1, 1)
        layout.addWidget(self.btnSave, 9, 2, 1, 1)
        layout.addWidget(self.btnRect, 9, 3, 1, 1)
        layout.addWidget(self.btnCrop, 9, 4, 1, 1)
        layout.addWidget(self.btnSaveParam, 9, 5, 1, 1)
        layout.addWidget(self.btnLoadParam, 9, 6, 1, 1)
        layout.addWidget(self.btnQuit, 9, 7, 1, 1)
        
        layout.addWidget(self.threshold_slider, 8, 5,1,2)

        # Define the Buttum Function
        self.btnOpen.clicked.connect(self.cameraSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnRect.clicked.connect(self.rectSlot)
        self.btnCrop.clicked.connect(self.cropSlot) 
        self.btnSaveParam.clicked.connect(self.saveParamSlot)
        self.btnLoadParam.clicked.connect(self.loadParamSlot) 
        self.btnQuit.clicked.connect(self.close)

        
    def cameraSlot(self):
        
        if self.camera_timer.isActive() == False:
            self.openCamera()
        else:
            self.closeCamera()
        
    def openCamera(self):
        
        flag = self.camera.open(self.CAM_NUM)
        
        if flag == False:
            msg = QMessageBox.warning(self, u'Warning', u'Please Check Your Camera Connection',
                                        buttons = QMessageBox.Ok,
                                        defaultButton = QMessageBox.Ok)
        else:
            self.camera_timer.start(100)
            self.btnOpen.setText('Cam Off')
        
    def closeCamera(self):
        
        self.camera_timer.stop()
        self.corp_timer.stop()
        self.camera.release()
        self.label_regularImg.clear()
        self.label_processedImg.clear()
        self.label_thresholdImg.clear()
        self.btnOpen.setText('Cam On')
        
    def queryFrame(self):
        """When Qtimer time out, refresh regular_img """
        ret, self.frame = self.camera.read()
        show = cv2.resize(self.frame,(480,360))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        QImg = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        self.label_regularImg.setPixmap(QPixmap.fromImage(QImg))
        

    def saveSlot(self):
        """ Save Photo """
        fileName, tmp = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        if self.img_processed.size == 1:
            return

        # Calling OpenCV function to save photo
        cv2.imwrite(fileName, self.img_processed)
        
    def rectSlot(self):
        """ Draw Rectangle on image """
        
        self.label_regularImg.setCursor(Qt.CrossCursor)
        self.corp_timer.stop()
        

    def cropSlot(self):
        
        self.corp_timer.start(30)
        self.label_regularImg.setCursor(Qt.ArrowCursor)
        self.label_processedImg.clear()

        
    def cropImg(self):
        """ Corp the Image"""
        
#         self.label_regularImg.setCursor(Qt.ArrowCursor)
        self.img_corp = qtpixmap_to_cvimg(processed_img)
        self.img_processed = cv2.cvtColor(self.img_corp, cv2.COLOR_BGR2GRAY)
        self.label_processedImg.setPixmap(processed_img)
        
        
    def changevalue(self,threshold):
        """ let the label change with the scroll bar """
        sender = self.sender()
        if sender == self.threshold_slider:
            self.threshold_slider.setValue(threshold)
        self.label_threshold.setText('threshold:'+str(threshold))
        self.threshold_value = threshold
        print (self.threshold_value)
        
        
    def thres_img(self):
        """Threshold"""
        ret , self.img_threshold = cv2.threshold(self.img_processed,self.threshold_value,255,cv2.THRESH_BINARY)  

        height, width = self.img_threshold.shape
        bytesPerline = 1 * width
            
        # Qimage read image
        self.qImg_threshold = QImage(self.img_threshold.data, width, height, bytesPerline, QImage.Format_Grayscale8)
        
        # show Qimage
        self.label_thresholdImg.setPixmap(QPixmap.fromImage(self.qImg_threshold))
        
        # Calculate the threshold value
        rate = PixelRate(self.img_threshold,self.threshold_value)
        self.label_thresholdrate.setText("佔比率 :"+str(rate.thresholdRate()))
        
    def saveParamSlot(self):
        config = ConfigParser()

        config['locate'] = {'x0': xywh[0],
                           'y0': xywh[1],
                           'w': xywh[2],
                           'h': xywh[3]}

        config['threshold'] = {'rate': self.threshold_value }

        with open('thres_param.ini', 'w') as configfile:
            config.write(configfile)
            
        msg = QMessageBox.warning(self, u'Warning', u'File save success!',
                                        buttons = QMessageBox.Ok)
            
    def loadParamSlot(self):
        filepath = "thres_param.ini"

        if os.path.isfile(filepath):
            msg = QMessageBox.warning(self, u'Warning', u'File exists',
                                        buttons = QMessageBox.Ok)
            
        else:
            msg = QMessageBox.warning(self, u'Warning', u'File does not exist',
                                        buttons = QMessageBox.Ok)
            
#     def loadAndRect(self):
        
        

        
class PixelRate():
    """Count the threshold rate"""
    
    def __init__(self, img_path, threshhold):
        self.img_path = img_path
        self.threshhold = threshhold
        
#         regular_img = cv2.imread(self.img_path,0)
        regular_img = self.img_path
        ret , self.thresh_img = cv2.threshold(regular_img,self.threshhold,255,cv2.THRESH_BINARY)
    
    def thresholdPixel(self):
        """Count the pixel which is above the threshold"""
        area = 0
        height, width = self.thresh_img.shape
        for i in range(height):
            for j in range(width):
                if self.thresh_img[i, j] > 180:
                    area += 1
        return area

    def totalPixel(self):
        """Count the total pixel"""
        height, width = self.thresh_img.shape
        return height*width


    def thresholdRate(self):
        """Calculate the Rate of the threshold"""
        Rate = (self.thresholdPixel()/self.totalPixel())*100
        Rate = np.round(Rate,2)
        return Rate
        
        
class CutImage(QLabel):
    """ define a class of Label to draw rectangle """
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self,event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        self.x1 = 0 ##
        self.y1 = 0 ##
        print("Start : ",self.x0,self.y0) ##
        
    def mouseReleaseEvent(self,event):
        self.flag = False
        print("End : ",self.x1,self.y1) ##
        
    def mouseMoveEvent(self,event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
            
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.x0, self.y0, self.x1-self.x0, self.y1-self.y0)
        
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)
        
        pqscreen  = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), min(self.x0, self.x1)+1, min(self.y0, self.y1)+1, abs(self.x1-self.x0)-2, abs(self.y1-self.y0)-2)
        
        global processed_img, xywh
        processed_img = pixmap2
        global xywh
        xywh = [min(self.x0, self.x1), min(self.y0, self.y1), abs(self.x1-self.x0), abs(self.y1-self.y0)]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    mainwindow.show()
    sys.exit(app.exec_())