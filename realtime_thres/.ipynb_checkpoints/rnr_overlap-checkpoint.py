import sys
import cv2
import numpy as np
import os 
from configparser import ConfigParser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5.QtCore import QRect, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QMessageBox

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
    """ define the user interface """
    
    filepath = "thres_param.ini"

    if os.path.isfile(filepath):
        config = ConfigParser()
        config.read('thres_param.ini')

        global x0, y0, w, h, threshold_rate

        x0 = int(config['locate']['x0'])
        y0 = int(config['locate']['y0'])
        w = int(config['locate']['w'])
        h = int(config['locate']['h'])
        threshold_rate = int(config['threshold']['rate']) 

    else:
        msg = QMessageBox.warning(self, u'Warning', u'File does not exist',
                                buttons = QMessageBox.Ok)
    
    def __init__(self):

        super().__init__()
        self.initUI()
        
        self.img_regular = np.ndarray(())
        self.img_corp = np.ndarray(())
        self.img_processed = np.ndarray(())
        self.img_threshold = np.ndarray(())
        self.img_overlap = np.ndarray(())

        self.camera = cv2.VideoCapture()
        self.CAM_NUM = 0  # Set Camera num
        
        self.camera_timer = QtCore.QTimer()
        self.camera_timer.timeout.connect(self.queryFrame)
        self.camera_timer.timeout.connect(self.cropImg)
        self.camera_timer.timeout.connect(self.thresImg)
        self.camera_timer.timeout.connect(self.overlapImg)
        
        
        flag = self.camera.open(self.CAM_NUM)
        
        if flag == False:
            msg = QMessageBox.warning(self, u'Warning', u'Please Check Your Camera Connection',
                                        buttons = QMessageBox.Ok,
                                        defaultButton = QMessageBox.Ok)
        else:
            self.camera_timer.start(50)
            self.label_threshold.setText('threshold:'+str(threshold_rate))
        
        

    def initUI(self):
        """ deifine the component of the user interface """
        # Define Size
        self.setGeometry(50,50,600,500)
        self.setWindowTitle('Load Image')


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
        
        layout.addWidget(self.label_threshold, 7, 5, 1, 1) 
        layout.addWidget(self.label_thresholdrate, 7, 6, 1, 1) 
        
        
    def queryFrame(self):
        """When Qtimer time out, refresh regular_img """
        ret, self.frame = self.camera.read()
        show = cv2.resize(self.frame,(480,360))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        QImg = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        self.label_regularImg.setPixmap(QPixmap.fromImage(QImg))
        
    def cropImg(self):
        """ Corp the Image"""
        self.img_corp = qtpixmap_to_cvimg(processed_img)
        self.img_processed = cv2.cvtColor(self.img_corp, cv2.COLOR_BGR2GRAY)
        self.label_processedImg.setPixmap(processed_img)
        
        
    def thresImg(self):
        """Threshold"""
        ret , self.img_threshold = cv2.threshold(self.img_processed,threshold_rate,255,cv2.THRESH_BINARY)  
        height, width = self.img_threshold.shape
        bytesPerline = 1 * width
            
        # Qimage read image
        self.qImg_threshold = QImage(self.img_threshold.data, width, height, bytesPerline, QImage.Format_Grayscale8)
        
        # show Qimage
        self.label_thresholdImg.setPixmap(QPixmap.fromImage(self.qImg_threshold))
        
        # Calculate the threshold value
        rate = PixelRate(self.img_threshold,threshold_rate)
        self.label_thresholdrate.setText("佔比率 :"+str(rate.thresholdRate()))     
        
        
    def overlapImg(self):
        """Overlap Img"""
        ret , mask = cv2.threshold(self.img_processed,threshold_rate,255,cv2.THRESH_BINARY)
        img = cv2.cvtColor(self.img_corp, cv2.COLOR_BGR2RGB)
        
        self.img_overlap = cv2.add(img, np.zeros(np.shape(img), dtype=np.uint8), mask=mask)

        height, width, bp = self.img_overlap.shape
        bytesPerline = 3 * width

        # Qimage read image
        self.qImg_overlap = QImage(self.img_overlap.data, self.img_overlap.shape[1], self.img_overlap.shape[0],bytesPerline, QImage.Format_RGB888)
        
        # show Qimage
        self.label_overlapImg.setPixmap(QPixmap.fromImage(self.qImg_overlap))
        

        
class PixelRate():
    """Count the threshold rate"""
    
    def __init__(self, img_path, threshhold):
        self.img_path = img_path
        self.threshhold = threshhold
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
            
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(x0, y0, w, h)
        
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)
        
        pqscreen  = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), x0+1, y0+1, w-2, h-2)
        
        global processed_img
        processed_img = pixmap2


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    mainwindow.show()
    sys.exit(app.exec_())