import sys
import numpy as np
import cv2
import argparse
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from colorizers import *

# 두번째 화면
class ColorWindow(QDialog):
    # 전역 변수 선언
    out_img_eccv16 = ""
    out_img_siggraph17 = ""

    def __init__(self, parent):  #부모 window 설정
        super(ColorWindow, self).__init__(parent)
        option_ui = 'Main/Color_recovery.ui'
        uic.loadUi(option_ui, self)

        self.siggraph17_btn.hide()
        self.eccv16_btn.hide()

        self.show()

        # 버튼에 기능을 연결하는 코드
        self.file_btn.clicked.connect(self.ConvertFunction)
        self.close_btn.clicked.connect(self.CloseFunction)
        self.eccv16_btn.clicked.connect(self.eccv16_SaveFunction)
        self.siggraph17_btn.clicked.connect(self.siggraph17_SaveFunction)
    
    #btn_1이 눌리면 작동 할 함수
    def ConvertFunction(self) :

        # 파일 불러오기
        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"
        fname1 = QFileDialog.getOpenFileName(self, 'File dialog', '',filters, selected_filter)
        print(fname1[0])
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

        # 전역 변수 선언
        global out_img_eccv16
        global out_img_siggraph17

        # colorizer outputs 256x256 ab map
        # resize and concatenate to original L channel
        img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
        out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

        plt.imsave('%s_eccv16.png'%opt.save_prefix, out_img_eccv16)
        plt.imsave('%s_siggraph17.png'%opt.save_prefix, out_img_siggraph17)
        
        # 이미지 불러오기
        pixmap1 = QPixmap("C:/Users/Hero/Documents/ColorRecovery/ColorRecovery/saved_eccv16.png")
        pixmap2 = QPixmap("C:/Users/Hero/Documents/ColorRecovery/ColorRecovery/saved_siggraph17.png")

        # eccv16 이미지 크기 비율 조정
        if pixmap1.width() > pixmap1.height() :
            pixmap1 = pixmap1.scaledToWidth(350)
        elif pixmap1.width() <= pixmap1.height() :
            pixmap1 = pixmap1.scaledToHeight(230)

        # siggraph17 이미지 크기 비율 조정
        if pixmap2.width() > pixmap2.height() :
            pixmap2 = pixmap2.scaledToWidth(350)
        elif pixmap2.width() <= pixmap2.height() :
            pixmap2 = pixmap2.scaledToHeight(230)

        # 이미지크기에 따라 위치 변경
        self.eccv16_image.setGeometry(QtCore.QRect(50+((350-pixmap1.width())/2), 60, 350, 230))
        self.siggraph17_image.setGeometry(QtCore.QRect(420+((350-pixmap2.width())/2), 60, 350, 230))

        # 이미지 출력
        self.eccv16_image.setPixmap(QPixmap(pixmap1))
        self.siggraph17_image.setPixmap(QPixmap(pixmap2))

        # 저장하기 버튼 출력
        self.siggraph17_btn.show()
        self.eccv16_btn.show()

    #btn_2가 눌리면 작동할 함수
    def CloseFunction(self) :
        self.close()

    # ecc16변환 이미지 저장
    def eccv16_SaveFunction(self) :
        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"

        fname = QFileDialog.getSaveFileName(self, " Save File ", "",filters, selected_filter)
        plt.imsave(fname[0], out_img_eccv16)

    # siggraph17변환 이미지 저장
    def siggraph17_SaveFunction(self) :
        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"

        fname = QFileDialog.getSaveFileName(self, " Save File ", "",filters, selected_filter)
        plt.imsave(fname[0], out_img_siggraph17)