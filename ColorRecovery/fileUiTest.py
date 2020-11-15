import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("fileUi.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 연결하는 코드
        self.file_btn.clicked.connect(self.button1Function)
        self.close_btn.clicked.connect(self.button2Function)

    #btn_1이 눌리면 작동할 함수
    def button1Function(self) :

        filters = "Text files (*.txt);;Images (*.png *.xpm *.jpg)"
        selected_filter = "Images (*.png *.xpm *.jpg)"
        fname = QFileDialog.getOpenFileName(self, " File dialog ", "",filters, selected_filter)
        print(fname[0])
        self.file_lable.setText(fname[0])
        self.image_area.setPixmap(QPixmap(QPixmap(fname[0])))
    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        print("close_btn Clicked")


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()