import sys
import numpy as np
import cv2

import argparse
import matplotlib.pyplot as plt

from colorizers import *

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
        print(fname1[0])
        self.file_lable.setText(fname1[0])
        img = cv2.imread(fname1[0])
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-i','--img_path', type=str, default=fname1[0])
        parser.add_argument('--use_gpu', action='store_true', help='whether to use GPU')
        parser.add_argument('-o','--save_prefix', type=str, default='saved', help='will save into this file with {eccv16.png, siggraph17.png} suffixes')
        opt = parser.parse_args()

        # load colorizers
        colorizer_eccv16 = eccv16(pretrained=True).eval()
        colorizer_siggraph17 = siggraph17(pretrained=True).eval()
        if(opt.use_gpu):
	        colorizer_eccv16.cuda()
	        colorizer_siggraph17.cuda()

        # default size to process images is 256x256
        # grab L channel in both original ("orig") and resized ("rs") resolutions
        img = load_img(opt.img_path)
        (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
        if(opt.use_gpu):
        	tens_l_rs = tens_l_rs.cuda()

        # colorizer outputs 256x256 ab map
        # resize and concatenate to original L channel
        img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
        out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

        plt.imsave('%s_eccv16.png'%opt.save_prefix, out_img_eccv16)
        plt.imsave('%s_siggraph17.png'%opt.save_prefix, out_img_siggraph17)
        
        # 이미지 불러오기
        pixmap = QPixmap("C:/Users/Hero/Documents/ColorRecovery/ColorRecovery/saved_eccv16.png")

        # 이미지 크기 비율 조정
        if pixmap.width() > pixmap.height() :
            pixmap = pixmap.scaledToWidth(300)
        elif pixmap.width() <= pixmap.height() :
            pixmap = pixmap.scaledToHeight(200)

        self.image_area.setPixmap(QPixmap(pixmap))

    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        print("close_btn Clicked")
        


    def setupUi(self, QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 740)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.file_btn = QtWidgets.QPushButton(self.centralwidget)
        self.file_btn.setGeometry(QtCore.QRect(250, 470, 151, 71))
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
        self.image_area.setGeometry(QtCore.QRect(120, 20, 300, 200))
        self.image_area.setObjectName("image_area")
        self.image_area.hide

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