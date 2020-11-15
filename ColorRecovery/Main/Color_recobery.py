import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import numpy as np
import cv2

# 두번째 화면
class ColorWindow(QDialog):
    def __init__(self, parent):  #부모 window 설정
        super(ColorWindow, self).__init__(parent)
        option_ui = 'Main/Color_recovery.ui'
        uic.loadUi(option_ui, self)
        self.show()

        #버튼에 기능을 연결하는 코드
        self.file_btn.clicked.connect(self.button1Function)
        self.close_btn.clicked.connect(self.button2Function)

        
         #btn_1이 눌리면 작동할 함수
    def button1Function(self) :
        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"
        fname1 = QFileDialog.getOpenFileName(self, 'File dialog', '',filters, selected_filter)
        fname2 = QFileDialog.getOpenFileName(self, 'File dialog', '',filters, selected_filter)
        print(fname1[0])
        print(fname2[0])
        img = cv2.imread(fname1[0])
        mask = cv2.imread(fname2[0],0)

        damage_recovery = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)

        cv2.imshow('damage_recovery_before',img)
        cv2.imshow('damage_recovery_after',damage_recovery)
        
        fname3 = QFileDialog.getSaveFileName(self, " Save File ", "",filters, selected_filter)
        cv2.imwrite(fname3[0],damage_recovery)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        WindowClass()