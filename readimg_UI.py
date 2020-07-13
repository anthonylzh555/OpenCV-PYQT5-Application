import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
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
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)

        # Define Label
        self.label_regularImg = QLabel("Regular Picture")
        self.label_processedImg = QLabel("Processed Picture")

        # Layout
        layout = QGridLayout(self)
        layout.addWidget(self.label_regularImg, 0, 1, 1, 2)    # (y,x,yspan,xspan)
        layout.addWidget(self.label_processedImg, 0, 3, 1, 2)    # (y,x,yspan,xspan)
        layout.addWidget(self.btnOpen, 4, 1, 1, 1)
        layout.addWidget(self.btnSave, 4, 2, 1, 1)
        layout.addWidget(self.btnProcess, 4, 3, 1, 1)
        layout.addWidget(self.btnQuit, 4, 4, 1, 1)

        # Define the Buttum Function
        self.btnOpen.clicked.connect(self.openSlot)
        self.btnSave.clicked.connect(self.saveSlot)
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
        
        if len(self.img_processed.shape) ==  2:
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
        self.img_processed = cv2.cvtColor(self.img_regular, cv2.COLOR_BGR2GRAY)

        height, width = self.img_processed.shape
        bytesPerline = 1 * width
            
        # Qimage read image
        self.qImg_processed = QImage(self.img_processed.data, width, height, bytesPerline, QImage.Format_Grayscale8)
        
        # show Qimage
        self.label_processedImg.setPixmap(QPixmap.fromImage(self.qImg_processed))
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    mainwindow.show()
    sys.exit(app.exec_())
