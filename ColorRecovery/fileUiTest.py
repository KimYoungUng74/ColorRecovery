import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
        pixmap = QPixmap(fname[0])
        print(pixmap.width())
        print(pixmap.height())

        self.file_lable.setText(fname[0])
        self.image_area = QImage(QSize(pixmap.width(), pixmap.height()), QImage.Format_RGB32)
        self.image_area.load("saved_siggraph17.png", "PNG")
        self.drawing = False
        self.brush_size = 5
        self.brush_color = Qt.black
        self.last_point = QPoint()

    #btn_2가 눌리면 작동할 함수
    def button2Function(self) :
        print("close_btn Clicked")

    def paintEvent(self, e):
        canvas = QPainter(self)
        # canvas.drawImage(self.image_area.rect(), self.image_area, self.image_area.rect())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image_area)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    def save(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if fpath:
            self.image_area.save(fpath)

    def clear(self):
        self.image_area.fill(Qt.white)
        self.update()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()