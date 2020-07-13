import cv2
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication

class CutImage(QLabel):
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
        pixmap2 = pqscreen.grabWindow(self.winId(), min(self.x0, self.x1), min(self.y0, self.y1), abs(self.x1-self.x0), abs(self.y1-self.y0))
        pixmap2.save('cut.png')

class mainUI(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.resize(400, 300)
        self.setWindowTitle('Cut Image')
        
        self.lb = CutImage(self)
        
        img = cv2.imread('sample.jpg')
        
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.lb.setPixmap(pixmap)
        
        self.lb.setCursor(Qt.CrossCursor)
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = mainUI()
    sys.exit(app.exec_())
