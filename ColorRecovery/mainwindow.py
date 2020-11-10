import sys
import numpy as np
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
class Ui_MainWindow(QMainWindow):

    #btn_1이 눌리면 작동할 함수
    def button1Function(self) :
        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"
        fname1 = QFileDialog.getOpenFileName(self, 'File dialog', '',filters, selected_filter)
        fname2 = QFileDialog.getOpenFileName(self, 'File dialog', '',filters, selected_filter)
        print(fname1[0])
        print(fname2[0])
        self.file_lable.setText(fname1[0])
        img = cv2.imread(fname1[0])
        mask = cv2.imread(fname2[0],0)

        damage_recovery = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)

        cv2.imshow('damage_recovery_before',img)
        cv2.imshow('damage_recovery_after',damage_recovery)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''self.image_area.setPixmap(QPixmap(QPixmap(fname[0])))'''
        
    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        print("close_btn Clicked")

    def setupUi(self, QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.file_btn = QtWidgets.QPushButton(self.centralwidget)
        self.file_btn.setGeometry(QtCore.QRect(330, 470, 151, 71))
        self.file_btn.setObjectName("file_btn")
        self.file_btn.clicked.connect(self.button1Function)
        
        self.close_btn = QtWidgets.QPushButton(self.centralwidget)
        self.close_btn.setGeometry(QtCore.QRect(350, 550, 111, 23))
        self.close_btn.setObjectName("close_btn")
        self.close_btn.clicked.connect(self.button2Function)

        self.file_lable = QtWidgets.QLabel(self.centralwidget)
        self.file_lable.setGeometry(QtCore.QRect(130, 420, 561, 20))
        self.file_lable.setObjectName("file_lable")

        self.image_area = QtWidgets.QLabel(self.centralwidget)
        self.image_area.setGeometry(QtCore.QRect(120, 20, 561, 361))
        self.image_area.setObjectName("image_area")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.file_btn.setText(_translate("MainWindow", "File Open"))
        self.close_btn.setText(_translate("MainWindow", "Close Button"))
        self.file_lable.setText(_translate("MainWindow", "File Name"))
        self.image_area.setText(_translate("MainWindow", "image Area"))


if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())