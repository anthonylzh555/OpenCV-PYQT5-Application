from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(636, 482)
        self.ROI_pushButton = QtWidgets.QPushButton(Dialog)
        self.ROI_pushButton.setGeometry(QtCore.QRect(30, 360, 113, 32))
        self.ROI_pushButton.setObjectName("ROI_pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 410, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setEnabled(True)
        self.listView.setGeometry(QtCore.QRect(350, 380, 271, 81))
        self.listView.setObjectName("listView")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(350, 360, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(140, 400, 131, 31))
        self.textEdit.setObjectName("textEdit")
        self.Threshold_pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.Threshold_pushButton_2.setGeometry(QtCore.QRect(30, 440, 113, 32))
        self.Threshold_pushButton_2.setObjectName("Threshold_pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ROI_pushButton.setText(_translate("Dialog", "ROI select"))
        self.label.setText(_translate("Dialog", "Threshold :"))
        self.label_2.setText(_translate("Dialog", "Result :"))
        self.Threshold_pushButton_2.setText(_translate("Dialog", "Enter"))

if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Dialog()

    ui.setupUi(MainWindow) 
    MainWindow.show()
    sys.exit(app.exec_()) 
