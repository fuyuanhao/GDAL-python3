import sys
from os import *
from PyInstaller.widgetF import Ui_form
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import *
from OpenCV_Study.ImageShow import cvshowimgRGB

# 新建widgetFForm类，继承Ui_CherryBlossom，继承了窗体类，可以继承界面上的所有控件
class widgetFForm(QtWidgets.QWidget, Ui_form):
    def __init__(self):
        # 继承Ui_Form
        super(widgetFForm, self).__init__()  #初始化父类
        self.setupUi(self)
        # 绑定输入数据路径按钮事件
        self.btnDataPath.clicked.connect(self.func_btn_datapath)
        # 绑定打开图像按钮事件
        self.btnOpenImage.clicked.connect(self.func_btn_openimage)


    # 关闭程序
    def closeEvent(self, QCloseEvent):
        # 两个按钮是否， 默认No则关闭这个提示框
        res = QMessageBox.question(self, '消息', '是否关闭这个窗口？',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    # 输入目录选择按钮事件
    def func_btn_datapath(self):
        get_filename_path, ok = \
            QFileDialog.getOpenFileName(self, "选取单个文件",
                                        "C:\Projects\Image",
                                        "jpg Files (*.jpg);;TIF Files (*.tif);;All Files (*)")
        if ok:
            self.tbDataPath.setText(str(get_filename_path))

    def func_btn_openimage(self):
        input_path = self.tbDataPath.toPlainText()
        print("input_path:::" + input_path)
        # 判断输入路径不为空
        if input_path:
            # 获取界面上的输入路径参数
            print("to do:::")
            # plotTest()
            # ReadVectorFile(input_path)
            #RasterIO_TIFProcess.showTiFF(input_path)
            cvshowimgRGB(input_path)
            msg_box = QMessageBox(QMessageBox.Warning, "Alert", input_path + "打开成功!")
            msg_box.exec_()

        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Alert", "请选择输入路径!")
            msg_box.exec_()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    # 指定弹出窗体
    WFshow=widgetFForm()
    WFshow.show()
    sys.exit(app.exec_())