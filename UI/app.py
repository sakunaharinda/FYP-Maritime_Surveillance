from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os

from PyQt5.QtWidgets import  *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
from time import sleep
import typing


from opts import opts
from opts_flir import opts_flir
from detectors.detector_factory import detector_factory
from vis import draw_bboxes
from track import tracking
from sort import *
from vis_utils import draw_bboxes_notrack


from splash_ui import Ui_splashScreen
from main_ui import Ui_mainWindow
from about_ui import Ui_about

image_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4', 'mov', 'avi', 'mkv']
time_stats = ['tot', 'load', 'pre', 'net', 'dec', 'post', 'merge']

color = [[255,255,255],[237,2,11],
[244,101,40],
[255,202,43],
[64,120,211],
[238,47,127],
[127,176,5],
[255,169,206],
[204,255,0],
[173,222,250],
[189,122,246]]



count = 0
domain = "Maritime"
filename = ""
state = 2
detector_smd = ""
detector_flir = ""
err_msg = "Open a video to detect !"
video_formats = ['avi','mp4']
objects = []
model = 'CenterNet'
mot_tracker = Sort()

class Worker(QObject):
    changePixmap = pyqtSignal(QImage)
    received = pyqtSignal(list)
    finished = pyqtSignal()
    
    def run(self):

        global filename, objects, state,domain,mot_tracker
        #mot_tracker = Sort()
        mot_tracker.reset()
        cap = cv2.VideoCapture(filename)
        FPS = cap.get(cv2.CAP_PROP_FPS)
        print(filename,FPS)

        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret:
                if domain == "Maritime" :
                    ret = detector_smd.run(frame)
                    bboxes = ret['results']
                    if state==0:
                        frame, cats = draw_bboxes_notrack(frame,bboxes,colors=color)
                    else:
                        
                        tracked = tracking(bboxes,mot_tracker)
                    
                        frame, cats  = draw_bboxes(frame, tracked,colors = color)
                elif domain == "Urban Driving":
                    ret = detector_flir.run(frame)
                    bboxes = ret['results']
                    if state==0:
                        

                        frame, cats = draw_bboxes_notrack(frame,bboxes,'flir',thresh=0.3,colors=color)
                    else:
                        
                        tracked = tracking(bboxes,mot_tracker)
                    
                        frame, cats  = draw_bboxes(frame, tracked,'flir',thresh=0.3,colors = color)

                self.received.emit(list(cats))
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1920, 1080, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                #sleep(1.0/30)
            else:

                cap.release()
                self.finished.emit()
                




class aboutWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_about()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)

        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.frame.setGraphicsEffect(self.shadow)

        self.ui.btn_ok.clicked.connect(self.about_ok)

        self.center()


    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def about_ok(self):
        self.close()

class mainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)

        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        self.ui.btn_quit.clicked.connect(self.quit)
        self.ui.btn_open_vid.clicked.connect(self.open)
        self.ui.btn_detect.clicked.connect(self.detect)
        #self.ui.check_track.stateChanged.connect(lambda:self.btnstate(self.ui.check_track))
        self.ui.btn_about.clicked.connect(self.about)
        self.ui.checkBox.stateChanged.connect(lambda:self.entrack(self.ui.checkBox))
        self.ui.radio_maritime.toggled.connect(self.get_domain)
        self.ui.radio_urban.toggled.connect(self.get_domain)
        self.center()

    def get_domain(self,val):
        global domain
        rbtn = self.sender()
        if rbtn.isChecked() == True:
            domain = rbtn.text()
            self.ui.text_stat.append("Selected Domain : {}".format(domain))

    def entrack(self,b):
        global state
        state = b.checkState()
        self.ui.text_stat.append("Tracking Enabled : {}".format("Yes" if state == 2 else "No"))
        mot_tracker.reset()
        

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


    def quit(self):
        sys.exit()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.screen.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(list)
    def getCats(self,l):
        global objects
        for obj in l:
            if obj not in objects:
                objects.append(obj)
                self.ui.text_obj.append(obj)

    def clear(self):
        self.ui.text_obj.setText("")

    def open(self):
        global filename
        filename,_ = QFileDialog.getOpenFileName(self, 'Open Video to Detect')
        cap = cv2.VideoCapture(filename)
        mot_tracker = Sort()
        _,frame = cap.read()
        rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.ui.screen.setPixmap(QPixmap(p))
        self.ui.text_stat.append("Video Selected : {}".format(filename.split('/')[-1]))

    def detect(self):
        global filename, err_msg, mot_tracker
        mot_tracker = Sort()
        if (filename != "" and filename.split('.')[-1] in video_formats):
            self.clear()
            self.th = QThread()
            self.worker = Worker()
            self.worker.moveToThread(self.th)
            self.th.started.connect(self.worker.run)
            self.worker.changePixmap.connect(self.setImage)

            self.worker.received.connect(self.getCats)
            self.worker.finished.connect(self.th.terminate)
            self.worker.finished.connect(self.worker.deleteLater)
            self.th.finished.connect(self.th.quit)
            
            mot_tracker = Sort()

            self.th.start()
        else:
            self.ui.text_stat.append(err_msg)

    def btnstate(self,b):
        if b.isChecked() == True:
            print('Checked')

    def about(self):
        self.ab = aboutWindow()
        self.ab.show()


class splashScreen(QMainWindow):
    def __init__(self):
        global detector_smd, model
        QMainWindow.__init__(self)
        self.ui = Ui_splashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)

        self.shadow.setColor(QColor(0,0,0,60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.center()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)

        # in ms
        self.timer.start(35)

        self.ui.label_desc.setText("<strong>WELCOME </strong>TO A SAFER SEA")

        QtCore.QTimer.singleShot(1400, lambda:self.ui.label_desc.setText("<strong>LOADING </strong>MODEL : {}. . .".format(model)))
        QtCore.QTimer.singleShot(2000, lambda:self.load_model())
        QtCore.QTimer.singleShot(3000, lambda:self.ui.label_desc.setText("<strong>LOADING </strong>INTERFACE . . ."))


        self.show()

    def load_model(self):
        global detector_smd, detector_flir

        opt = opts().init()
        opt.load_model = "../Center_SMD/exp/smd/dla_34/rgb/smd_split1/model_best.pth"
        os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
        opt.debug = max(opt.debug, 1)
        Detector = detector_factory[opt.task]
        detector_smd = Detector(opt)

        opt_flir = opts_flir().init()
        opt_flir.load_model = "../Center_SMD/exp/flir/dla_34/rgb/coco_dla/model_best.pth"
        os.environ['CUDA_VISIBLE_DEVICES'] = opt_flir.gpus_str
        opt_flir.debug = max(opt_flir.debug, 1)
        Detector_flir = detector_factory[opt_flir.task]
        detector_flir= Detector_flir(opt_flir)


        self.ui.label_desc.setText("<strong>LOADING </strong>MODEL . . .")


    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

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
