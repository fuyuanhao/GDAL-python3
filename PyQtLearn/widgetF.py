# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgetF.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(849, 434)
        self.btnOpenImage = QtWidgets.QPushButton(form)
        self.btnOpenImage.setGeometry(QtCore.QRect(520, 100, 81, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.btnOpenImage.setFont(font)
        self.btnOpenImage.setObjectName("btnOpenImage")
        self.splitter = QtWidgets.QSplitter(form)
        self.splitter.setGeometry(QtCore.QRect(180, 40, 411, 31))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.lblDataPath = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.lblDataPath.setFont(font)
        self.lblDataPath.setObjectName("lblDataPath")
        self.tbDataPath = QtWidgets.QTextBrowser(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.tbDataPath.setFont(font)
        self.tbDataPath.setObjectName("tbDataPath")
        self.btnDataPath = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(12)
        self.btnDataPath.setFont(font)
        self.btnDataPath.setObjectName("btnDataPath")

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "widgetF"))
        self.btnOpenImage.setText(_translate("form", "打开图片"))
        self.lblDataPath.setText(_translate("form", "数据路径："))
        self.btnDataPath.setText(_translate("form", "浏览"))
