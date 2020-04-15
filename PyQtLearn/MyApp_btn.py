import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton("按钮 1", self)
        btn1.move(30, 50)
        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
        self.statusBar()
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('事件与信号')
        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' 被点击')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())