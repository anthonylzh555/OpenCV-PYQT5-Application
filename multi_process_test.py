import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QGridLayout, QLabel, QPushButton



class mainUI(QDialog):
    
    def __init__(self):
        """
        imitialize a numpy array to save  a photo
        """
        self.img_regular = np.ndarray(())
        self.img_processed = np.ndarray(())
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        deifine the user interface
        """
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
        

        # Layout
        layout = QGridLayout(self)
        layout.addWidget(self.label_regularImg, 0, 1, 1, 3)    # (y,x,yspan,xspan)
        layout.addWidget(self.label_processedImg, 0, 4, 1, 3)    # (y,x,yspan,xspan)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnRect, 4, 3, 1, 1)
        layout.addWidget(self.btnCrop, 4, 4, 1, 1)
        layout.addWidget(self.btnProcess, 4, 5, 1, 1)
        layout.addWidget(self.btnQuit, 4, 6, 1, 1)

        # Define the Buttum Function
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
        self.btnRect.clicked.connect(self.rectSlot)
        self.btnCrop.clicked.connect(self.cropSlot) 
        self.btnProcess.clicked.connect(self.processSlot)
        self.btnQuit.clicked.connect(self.close)

    def openSlot(self):
        """
        Load Image
        """
        fileName, tmp = QFileDialog.getOpenFileName(self, 'Open Image', 'Image', '*.png *.jpg *.bmp')

        # Return to the main UI
        if fileName is "":
            return
        
        #Read File by OpenCV
        self.img_regular = cv2.imread(fileName)

        # Return to the main UI
        if self.img_regular.size == 1:
            return
        
        if len(self.img_regular.shape) ==  2:
            return
        
        height, width, channel = self.img_regular.shape
        bytesPerline = 3 * width

        # Qimage read image
        self.qImg_regular = QImage(self.img_regular.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        
        # show Qimage
        self.label_regularImg.setPixmap(QPixmap.fromImage(self.qImg_regular))
        
    def saveSlot(self):
        """
        Save Photo
        """
        fileName, tmp = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        if self.img_processed.size == 1:
            return

        # Calling OpenCV function to save photo
        cv2.imwrite(fileName, self.img_processed)
        
    def processSlot(self):
        """
        Process Data Here
        """
        if self.img_regular.size == 1:
            return
        
        #Processing Image
        #self.img = cv2.blur(self.img, (5, 5))
        self.img_processed = cv2.cvtColor(self.img_processed, cv2.COLOR_BGR2GRAY)

        height, width = self.img_processed.shape
        bytesPerline = 1 * width
            
        # Qimage read image
        self.qImg_processed = QImage(self.img_processed.data, width, height, bytesPerline, QImage.Format_Grayscale8)
        
        # show Qimage
        self.label_processedImg.setPixmap(QPixmap.fromImage(self.qImg_processed))
        
    def rectSlot(self):
        """
        Draw Rectangle on image
        """
        self.label_regularImg.setCursor(Qt.CrossCursor)


    def cropSlot(self):
        
        if processed_img is '':
            return

        self.label_processedImg.setPixmap(processed_img)
        ##########################
        self.img_processed = processed_img
        ##########################

        
class CutImage(QLabel):
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
#         processed_img= np.ndarray((pixmap2))
        processed_img = pixmap2
        
#         pixmap2.save('cut.png')

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    
    mainwindow.show()
    sys.exit(app.exec_())