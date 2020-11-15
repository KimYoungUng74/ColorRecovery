import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from Color_recobery import ColorWindow

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
main_ui = uic.loadUiType("Main/main.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, main_ui) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
         #버튼에 기능을 연결하는 코드
        self.color_btn.clicked.connect(self.ColorBtnFunction)
        self.demege_btn.clicked.connect(self.button2Function)
        self.producer_btn.clicked.connect(self.button3Function)

    #btn_1가 눌리면 작동할 함수
    def ColorBtnFunction(self) :
        ColorWindow(self)
    
    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        print("close_btn Clicked")
    
    #btn_3가 눌리면 작동할 함수
    def button3Function(self) :
        print("close_btn Clicked")

        


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()