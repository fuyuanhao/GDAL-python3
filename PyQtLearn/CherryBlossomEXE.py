import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyInstaller.CherryBlossom import Ui_MainWindow
from OpenCV_Study.ImageShow import cvreadRGB
from GDAL_Raster.ShowTIF import QshowColorTIFF
import cv2

# 新建CherryBlossomForm类，继承Ui_MainWindow，继承了窗体类，可以继承界面上的所有控件
class CherryBlossomForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # 继承Ui_Form
        super(CherryBlossomForm, self).__init__()  #初始化父类
        self.setupUi(self)
        self.aOpenNaturalPicture.triggered.connect(self.func_aOpenNaturalPicture)
        self.aOpenRGBFromMulti.triggered.connect(self.func_aOpenRGBFromMulti)

    # 关闭程序
    def closeEvent(self, QCloseEvent):
        # 两个按钮是否， 默认No则关闭这个提示框
        res = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit？',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    # 打开自然图像
    def func_aOpenNaturalPicture(self):
        get_filename_path, ok = \
            QFileDialog.getOpenFileName(self, "选取单个文件",
                                        "C:\Projects\Image",
                                        "jpg Files (*.jpg);;TIF Files (*.tif);;All Files (*)")
        if ok:
            self.statusBar().showMessage(str(get_filename_path))
            self.image = cvreadRGB(get_filename_path)
            print(self.image.shape)
            print(self.image.data)
            print(self.image.shape[1])
            print(self.image.shape[0])
            self.image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0],
                                      QtGui.QImage.Format_RGB888).rgbSwapped()
            self.lbl_image.setPixmap(QtGui.QPixmap.fromImage(self.image))

    # 打开多波段影像
    def func_aOpenRGBFromMulti(self):
        get_filename_path, ok = \
            QFileDialog.getOpenFileName(self, "选取单个文件",
                                        "C:\Projects\RasterData",
                                        "TIF Files (*.tif);;All Files (*)")
        if ok:
            self.statusBar().showMessage(str(get_filename_path))
            temp_jpg = QshowColorTIFF(get_filename_path)
            img = cv2.imread(temp_jpg, cv2.IMREAD_COLOR)
            height, width, bytesPerComponent = img.shape
            bytesPerLine = 3 * width
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            QImg = QtGui.QImage(img.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            self.lbl_image.setPixmap(QtGui.QPixmap.fromImage(QImg))

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 指定弹出窗体
    CBshow = CherryBlossomForm()
    CBshow.show()
    sys.exit(app.exec_())