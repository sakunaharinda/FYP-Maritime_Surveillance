from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import  *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
from time import sleep

from splash_ui import Ui_splashScreen
from main_ui import Ui_mainWindow

count = 0

filename = ""
err_msg = "Open a video to detect !"
video_formats = ['avi','mp4']
objects = []

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    received = pyqtSignal(list)

    def run(self):
        global filename
        print(filename)
        cap = cv2.VideoCapture(filename)
        FPS = cap.get(cv2.CAP_PROP_FPS)
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cats = ['Basketball','Basketball']
                self.received.emit(cats)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                sleep(1.0/FPS)
        cap.release()


class mainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.btn_quit.clicked.connect(self.quit)
        self.ui.btn_open_vid.clicked.connect(self.open)
        self.ui.btn_detect.clicked.connect(self.detect)
        self.ui.check_track.stateChanged.connect(lambda:self.btnstate(self.ui.check_track))

    def quit(self):
        sys.exit()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.screen.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(list)
    def get_cats(self,l):
        global objects
        for obj in l:
            if obj not in objects:
                objects.append(obj)
                self.ui.text_obj.append(obj)
    
    def open(self):
        global filename
        filename,_ = QFileDialog.getOpenFileName(self, 'Open Video to Detect')
        
        self.ui.text_stat.append("Video Selected : {}".format(filename.split('/')[-1]))
        if (filename != "" and filename.split('.')[-1] in video_formats):
            cap = cv2.VideoCapture(filename)
            _,frame = cap.read()
            
            


    def detect(self):
        global filename, err_msg
        if (filename != "" and filename.split('.')[-1] in video_formats):
            th = Thread(self)
            th.received.connect(self.get_cats)
            th.changePixmap.connect(self.setImage)
            th.start()
        else:
            self.ui.text_stat.append(err_msg)

    def btnstate(self,b):
        if b.isChecked() == True:
            print('Checked')

    


class splashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_splashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        
        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)

        # in ms
        self.timer.start(35)

        self.ui.label_desc.setText("<strong>WELCOME </strong>TO A SAFER SEA")
        QtCore.QTimer.singleShot(1500, lambda:self.ui.label_desc.setText("<strong>LOADING </strong>MODEL . . ."))
        QtCore.QTimer.singleShot(3000, lambda:self.ui.label_desc.setText("<strong>LOADING </strong>INTERFACE . . ."))


        self.show()


    def progress(self):
        global count
        self.ui.progressBar.setValue(count)
        if (count>100):
            self.timer.stop()
            self.main = mainWindow()
            self.main.show()

            self.close()
        count+=1



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = splashScreen()
    sys.exit(app.exec_())