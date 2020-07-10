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
        self.img = np.ndarray(())
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        deifine the user interface
        """
        # Define Size
        self.resize(400, 300)

        # Define Buttum
        self.btnOpen = QPushButton('Open', self)
        self.btnSave = QPushButton('Save', self)
        self.btnProcess = QPushButton('Process', self)
        self.btnQuit = QPushButton('Quit', self)

        # Define Label
        self.label = QLabel()

        # Layout
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 3, 4)    # (y,x,yspan,xspan)
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
        self.img = cv2.imread(fileName)

        # Return to the main UI
        if self.img.size == 1:
            return
        
        self.refreshShow()

    def refreshShow(self):
        """
        Transform OpenCV image into Qimage
        Then Refresh
        """
        if len(self.img.shape) == 3 :
            height, width, channel = self.img.shape
            bytesPerline = 3 * width

            # Qimage read image
            self.qImg = QImage(self.img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        
            # show Qimage
            self.label.setPixmap(QPixmap.fromImage(self.qImg))

        elif  len(self.img.shape) == 2 :
            height, width = self.img.shape
            bytesPerline = 1 * width
            
            # Qimage read image
            self.qImg = QImage(self.img.data, width, height, bytesPerline, QImage.Format_Grayscale8)
        
            # show Qimage
            self.label.setPixmap(QPixmap.fromImage(self.qImg))
        
    def saveSlot(self):
        """
        Save Photo
        """
        fileName, tmp = QFileDialog.getSaveFileName(self, 'Save Image', 'Image', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        if self.img.size == 1:
            return

        # Calling OpenCV function to save photo
        cv2.imwrite(fileName, self.img)

    def processSlot(self):
        """
        Process Data Here
        """
        if self.img.size == 1:
            return
        
        #Processing Image
        #self.img = cv2.blur(self.img, (5, 5))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.refreshShow()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    mainwindow.show()
    sys.exit(app.exec_())
