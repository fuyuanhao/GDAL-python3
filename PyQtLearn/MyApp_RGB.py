from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QFrame, QApplication)
from PyQt5.QtGui import QColor
import sys

class RGBSquareExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #-------------------------画界面，并给按钮添加事件-------------------------
        self.col = QColor(0, 0, 0)#默认颜色
        redb = QPushButton('Red', self)#红色按钮
        redb.setCheckable(True)#选择设定
        redb.move(10, 10)#按钮在窗体中的位置，距左上的距离
        redb.clicked[bool].connect(self.setColor)#点击事件
        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)
        greenb.clicked[bool].connect(self.setColor)
        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)
        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        #设置方块大小,前两个值是离窗体左上角的位置，后两个值是方块的宽和高
        self.square.setGeometry(150, 30, 200, 100)
        #按照指令更改方块的样式，类似于网页中的css样式
        self.square.setStyleSheet("QWidget { background-color: %s }" %
                                  self.col.name())
        #窗体大小，前两个值是离屏幕左上角坐标的位置(300, 300)的位置分别为，后两项分别是窗体宽度和高度
        self.setGeometry(300, 300, 400, 200)
        #窗体标题
        self.setWindowTitle('Toggle button')
        #弹出窗体
        self.show()
    #-----------------------------画界面结束------------------------

    #---------------界面事件的执行程序-------------------------------
    def setColor(self, pressed):
        source = self.sender()
        if pressed:
            val = 255
        else: val = 0

        if source.text() == "Red":
            self.col.setRed(val)#255,0,0
        elif source.text() == "Green":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)
        #按照指令更改方块的样式，类似于网页中的css样式
        self.square.setStyleSheet("QFrame { background-color: %s }" %
                                  self.col.name())
        #-----------------------界面事件结束------------------------------

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RGBSquareExample()
    sys.exit(app.exec_())