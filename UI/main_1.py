# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(994, 605)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_main = QtWidgets.QFrame(self.centralwidget)
        self.frame_main.setStyleSheet("QFrame{\n"
"    background-color:rgb(25, 35, 45);\n"
"    color:rgb(220,220,220);\n"
"    border-radius:10px;\n"
"}")
        self.frame_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main.setObjectName("frame_main")
        self.screen = QtWidgets.QLabel(self.frame_main)
        self.screen.setGeometry(QtCore.QRect(20, 70, 731, 411))
        self.screen.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.screen.setStyleSheet("QLabel {\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:beige;\n"
"    \n"
"}")
        self.screen.setText("")
        self.screen.setScaledContents(True)
        self.screen.setObjectName("screen")
        self.btn_open_vid = QtWidgets.QPushButton(self.frame_main)
        self.btn_open_vid.setGeometry(QtCore.QRect(20, 520, 111, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(13)
        self.btn_open_vid.setFont(font)
        self.btn_open_vid.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: rgb(0, 85, 255);\n"
"    \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    \n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"    \n"
"    background-color: rgb(10, 2, 255);\n"
"}\n"
"\n"
"")
        self.btn_open_vid.setObjectName("btn_open_vid")
        self.btn_detect = QtWidgets.QPushButton(self.frame_main)
        self.btn_detect.setGeometry(QtCore.QRect(430, 520, 131, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(15)
        self.btn_detect.setFont(font)
        self.btn_detect.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: rgb(0, 85, 255);\n"
"    \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    \n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"    \n"
"    background-color: rgb(10, 2, 255);\n"
"}\n"
"\n"
"")
        self.btn_detect.setObjectName("btn_detect")
        self.btn_connect_cam = QtWidgets.QPushButton(self.frame_main)
        self.btn_connect_cam.setGeometry(QtCore.QRect(180, 520, 131, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(12)
        self.btn_connect_cam.setFont(font)
        self.btn_connect_cam.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: rgb(0, 85, 255);\n"
"    \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    \n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"    \n"
"    background-color: rgb(10, 2, 255);\n"
"}\n"
"\n"
"")
        self.btn_connect_cam.setObjectName("btn_connect_cam")
        self.btn_quit = QtWidgets.QPushButton(self.frame_main)
        self.btn_quit.setGeometry(QtCore.QRect(690, 520, 111, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(15)
        self.btn_quit.setFont(font)
        self.btn_quit.setStyleSheet("QPushButton{\n"
"    \n"
"    \n"
"    background-color: rgb(255, 0, 0);\n"
"    \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    \n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    \n"
"    \n"
"    background-color: rgb(255, 73, 60);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"    \n"
"    \n"
"    background-color: rgb(188, 0, 3);\n"
"}\n"
"\n"
"")
        self.btn_quit.setObjectName("btn_quit")
        self.label_obj = QtWidgets.QLabel(self.frame_main)
        self.label_obj.setGeometry(QtCore.QRect(770, 30, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_obj.setFont(font)
        self.label_obj.setAlignment(QtCore.Qt.AlignCenter)
        self.label_obj.setObjectName("label_obj")
        self.text_obj = QtWidgets.QTextEdit(self.frame_main)
        self.text_obj.setGeometry(QtCore.QRect(780, 70, 171, 211))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.text_obj.setFont(font)
        self.text_obj.setStyleSheet("QTextEdit{\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:beige;\n"
"}")
        self.text_obj.setObjectName("text_obj")
        self.text_stat = QtWidgets.QTextEdit(self.frame_main)
        self.text_stat.setGeometry(QtCore.QRect(780, 330, 171, 151))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.text_stat.setFont(font)
        self.text_stat.setStyleSheet("QTextEdit{\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color:beige;\n"
"}")
        self.text_stat.setObjectName("text_stat")
        self.label_stat = QtWidgets.QLabel(self.frame_main)
        self.label_stat.setGeometry(QtCore.QRect(770, 300, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_stat.setFont(font)
        self.label_stat.setAlignment(QtCore.Qt.AlignCenter)
        self.label_stat.setObjectName("label_stat")
        self.label_vid = QtWidgets.QLabel(self.frame_main)
        self.label_vid.setGeometry(QtCore.QRect(290, 30, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_vid.setFont(font)
        self.label_vid.setAlignment(QtCore.Qt.AlignCenter)
        self.label_vid.setObjectName("label_vid")
        self.btn_about = QtWidgets.QPushButton(self.frame_main)
        self.btn_about.setGeometry(QtCore.QRect(850, 520, 101, 41))
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(15)
        self.btn_about.setFont(font)
        self.btn_about.setStyleSheet("QPushButton{\n"
"    \n"
"    background-color: rgb(0, 85, 255);\n"
"    \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    \n"
"}\n"
"\n"
"QPushButton::hover {\n"
"    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"    \n"
"    background-color: rgb(10, 2, 255);\n"
"}\n"
"\n"
"")
        self.btn_about.setObjectName("btn_about")
        self.horizontalLayout.addWidget(self.frame_main)
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.btn_open_vid.setText(_translate("mainWindow", "Open Video ..."))
        self.btn_detect.setText(_translate("mainWindow", "Detect"))
        self.btn_connect_cam.setText(_translate("mainWindow", "Connect a Camera"))
        self.btn_quit.setText(_translate("mainWindow", "Quit"))
        self.label_obj.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Detected </span><span style=\" font-size:16pt;\">Objects</span></p></body></html>"))
        self.label_stat.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Status </span></p></body></html>"))
        self.label_vid.setText(_translate("mainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Video</span><span style=\" font-size:16pt;\"> Feed</span></p></body></html>"))
        self.btn_about.setText(_translate("mainWindow", "About"))

