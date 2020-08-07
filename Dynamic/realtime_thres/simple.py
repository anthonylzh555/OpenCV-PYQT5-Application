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
        self.CAM_NUM = 0  
        
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
        

    def initUI(self):
        """ deifine the component of the user interface """
        # Define Size
        self.setGeometry(50,50,600,500)
        self.setWindowTitle('Load Image')


        # Define Label
        self.label_regulerImg_sign = QLabel("Reguler Image : ")
        self.label_overlapImg_sign = QLabel("Overlap : ")
        
        
        self.label_regularImg = CutImage(self)
        self.label_overlapImg = drawRect("Overlapping img")
        self.label_thresholdrate = QLabel("佔比率 : 0 ",self)
        

        # Layout
        layout = QGridLayout(self)
        layout.addWidget(self.label_regulerImg_sign, 1, 1, 1, 1)
        layout.addWidget(self.label_regularImg, 2, 1, 1, 1)    # (y,x,yspan,xspan)
        layout.addWidget(self.label_overlapImg_sign, 1, 3, 1, 1)
        layout.addWidget(self.label_overlapImg, 2, 3, 1, 1)
        
        layout.addWidget(self.label_thresholdrate, 4, 4, 1, 1) 
        
        
    def queryFrame(self):
        """When Qtimer time out, refresh regular_img """
        ret, frame= self.camera.read()
        scale_percent = 80       # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        show = cv2.resize(frame,dim)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        self.img_regular = show
        
        QImg = QImage(self.img_regular.data,  self.img_regular.shape[1], self.img_regular.shape[0],QImage.Format_RGB888)
        self.label_regularImg.setPixmap(QPixmap.fromImage(QImg))
#         self.label_overlapImg.setPixmap(QPixmap.fromImage(QImg))
        
    def cropImg(self):
        """ Corp the Image"""
        self.img_corp = qtpixmap_to_cvimg(processed_img)
        self.img_processed = cv2.cvtColor(self.img_corp, cv2.COLOR_BGR2GRAY)
        
        
    def thresImg(self):
        """Threshold"""
        ret , self.img_threshold = cv2.threshold(self.img_processed,threshold_rate,255,cv2.THRESH_BINARY)  
        height, width = self.img_threshold.shape
        bytesPerline = 1 * width
        
        # Calculate the threshold value
        rate = PixelRate(self.img_threshold)
        self.label_thresholdrate.setText("佔比率 :"+str(rate.thresholdRate()))     
        

    def overlapImg(self):
        """Overlap Img2"""
        mask = self.img_threshold
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB) 
        
        height, width, depth = mask_rgb.shape
        for i in range(height):
            for j in range(width):
                if mask[i, j] == 255:
                    mask_rgb[i, j] = (255,0,0)

        img = self.img_regular
        
        blank_image = np.zeros((img.shape[0],img.shape[1],3), np.uint8)
        blank_image[y0+1:y0+h-1, x0+1:x0+w-1] = mask_rgb

        self.img_overlap = cv2.addWeighted(img, 0.8, blank_image, 0.2, 0)      
        
        height, width, bp = self.img_overlap.shape
        bytesPerline = 3 * width

        # Qimage to QLabel
        self.qImg_overlap = QImage(self.img_overlap.data, self.img_overlap.shape[1], self.img_overlap.shape[0],bytesPerline, QImage.Format_RGB888)
        self.label_overlapImg.setPixmap(QPixmap.fromImage(self.qImg_overlap))
        
        
class PixelRate():
    """Count the threshold rate"""
    
    def __init__(self, img):
        self.thresh_img = img
    
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
        Rate = np.round(Rate,1)
        return Rate
        
        
class CutImage(QLabel):
    """ define a class of Label to draw rectangle """
            
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(x0, y0, w, h)
        
        pqscreen  = QGuiApplication.primaryScreen()
        pixmap2 = pqscreen.grabWindow(self.winId(), x0+1, y0+1, w-2, h-2)
        
        global processed_img
        processed_img = pixmap2
        
class drawRect(QLabel):
    """ define a class of Label to draw rectangle """
            
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(x0, y0, w, h)
        
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawRect(rect)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    mainwindow.show()
    sys.exit(app.exec_())