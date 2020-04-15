from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Only needed for access to command line arguments
import sys,os


# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("如梦令")

        widget = QComboBox()
        widget.addItems(["昨夜雨疏风骤", "浓睡不消残酒", "试问卷帘人", "却道海棠依旧"])

        # The default signal from currentIndexChanged sends the index
        widget.currentIndexChanged.connect(self.index_changed)

        # The same signal can send a text string
        widget.currentIndexChanged[str].connect(self.text_changed)

        #self.setCentralWidget(widget)
        self.setMenuWidget(widget)

    def index_changed(self, i):  # i is an int
        print(i)

    def text_changed(self, s):  # s is a str
        print(s)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()

# Your application won't reach here until you exit and the event
# loop has stopped.














