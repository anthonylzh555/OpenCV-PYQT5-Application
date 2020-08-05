import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QPushButton, QSlider

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
    
    global threshold_rate
    
    def __init__(self):
        """ initialize the parameter and numpy array to save photoes """
        self.img_regular = np.ndarray(())
        self.img_corp = np.ndarray(())
        self.img_processed = np.ndarray(())
        self.img_threshold = np.ndarray(())
        self.img_overlap = np.ndarray(())
        
        
        super().__init__()
        self.initUI()

    def initUI(self):
        """ deifine the component of the user interface """
        # Define Size
        self.resize(400, 300)
        self.setWindowTitle('Load Image')

        # Define Buttum
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnRect = QPushButton('Rect', self)
        self.btnCrop = QPushButton('Crop', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)

        # Define Label
        self.label_regularImg = CutImage(self)
        self.label_processedImg = QLabel("Processed Picture")
        self.label_thresholdImg = QLabel("threshold Picture")
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
        layout.addWidget(self.label_regularImg, 0, 1, 1, 3)    # (y,x,yspan,xspan)
        layout.addWidget(self.label_processedImg, 1, 1, 1, 3)
        layout.addWidget(self.label_thresholdImg, 0, 4, 1, 2)
        layout.addWidget(self.label_overlapImg, 1, 4, 1, 2)
        layout.addWidget(self.label_threshold, 3, 6, 1, 1) 
        layout.addWidget(self.label_thresholdrate, 2, 6, 1, 1) 
        
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnRect, 4, 3, 1, 1)
        layout.addWidget(self.btnCrop, 4, 4, 1, 1)
        layout.addWidget(self.btnProcess, 4, 5, 1, 1)
        layout.addWidget(self.btnQuit, 4, 6, 1, 1)
        
        layout.addWidget(self.threshold_slider, 3, 5,1,1)

        # Define the Buttum Function
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnRect.clicked.connect(self.rectSlot)
        self.btnCrop.clicked.connect(self.cropSlot) 
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)

    def openSlot(self):
        """ Load Image  """
        fileName, tmp = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.png *.jpg *.bmp')

        # Return to the main UI
        if fileName is "":
            return
        
        #Read File by OpenCV and resize
        self.img_regular = cv2.imread(fileName)
        scale_percent = 60       # percent of original size
        width = int(self.img_regular.shape[1] * scale_percent / 100)
        height = int(self.img_regular.shape[0] * scale_percent / 100)
        dim = (width, height)
        self.img_regular = cv2.resize(self.img_regular,dim)

        # Return to the main UI
        if self.img_regular.size == 1:
            return
        
        if len(self.img_regular.shape) ==  2:
            return
        
#         height, width, channel = self.img_regular.shape
        bytesPerline = 3 * width

        # Qimage read image
        self.qImg_regular = QImage(self.img_regular.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        
        # show Qimage
        self.label_regularImg.setPixmap(QPixmap.fromImage(self.qImg_regular))
        
    def saveSlot(self):
        """ Save Photo """
        fileName, tmp = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        if self.img_processed.size == 1:
            return

        # Calling OpenCV function to save photo
        cv2.imwrite(fileName, self.img_processed)
        
    def processSlot(self):
        """ Process Data Here (BGR2GRAY) """
        print("self.img_processed = ",self.img_corp)
        if self.img_corp is '':
            return
        
        print("type(self.img_processed) = ",self.img_corp.size)
        if self.img_corp.size == 1:
            return
        
        #Processing Image
        #self.img = cv2.blur(self.img, (5, 5))
        self.img_processed = cv2.cvtColor(self.img_corp, cv2.COLOR_BGR2GRAY)
        

        height, width = self.img_processed.shape
        bytesPerline = 1 * width
            
        # Qimage read image
        self.qImg_processed = QImage(self.img_processed.data, width, height, bytesPerline, QImage.Format_Grayscale8)
        
        # show Qimage
        self.label_processedImg.setPixmap(QPixmap.fromImage(self.qImg_processed))
        
    def rectSlot(self):
        """ Draw Rectangle on image """
        self.label_regularImg.setCursor(Qt.CrossCursor)


    def cropSlot(self):
        """ Corp the Image"""
        if processed_img is '':
            return
        self.label_regularImg.setCursor(Qt.ArrowCursor)
        self.label_processedImg.setPixmap(processed_img)
        self.img_corp = qtpixmap_to_cvimg(processed_img)
        
    def changevalue(self,threshold_value):
        """ let the label change with the scroll bar """
        sender = self.sender()
        if sender == self.threshold_slider:
            self.threshold_slider.setValue(threshold_value)
        self.label_threshold.setText('threshold:'+str(threshold_value))
        
        # Threshold
        ret , self.img_threshold = cv2.threshold(self.img_processed,threshold_value,255,cv2.THRESH_BINARY)  

        height, width = self.img_threshold.shape
        bytesPerline = 1 * width
            
        # Qimage read image
        self.qImg_threshold = QImage(self.img_threshold.data, width, height, bytesPerline, QImage.Format_Grayscale8)
        
        # show Qimage
        self.label_thresholdImg.setPixmap(QPixmap.fromImage(self.qImg_threshold))
        
        # Calculate the threshold value
        rate = PixelRate(self.img_threshold,threshold_value)
        self.label_thresholdrate.setText("佔比率 :"+str(rate.thresholdRate()))
        
         
        """Overlap Img"""
        ret , mask = cv2.threshold(self.img_processed,threshold_value,255,cv2.THRESH_BINARY)
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
#     global processed_img
    
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
        pixmap2 = pqscreen.grabWindow(self.winId(), min(self.x0, self.x1), min(self.y0, self.y1), abs(self.x1-self.x0), abs(self.y1-self.y0))
        
        global processed_img
        processed_img = pixmap2
    
#         print("processed_img = ",type(processed_img))
#         pixmap2.save('cut.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    mainwindow.show()
    sys.exit(app.exec_())