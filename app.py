import os
import sys
import ctypes

from PyQt5 import QtWidgets, QtCore, QtGui

from splash_ui import SplashClass
from login import Dialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable high dpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use high dpi icons

myapp_id = 'www.nguyentrieuphong.com'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)

ROOT_DIR = os.path.abspath(os.curdir)
ICON_PATH = os.path.join(ROOT_DIR, 'static/logo.png')


class SplashScreen(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = SplashClass()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.counter = 0
        self.n = 100
        self.ui.Image_1.hide()
        self.ui.Image_2.hide()
        self.ui.Image_3.hide()
        self.ui.Image_4.hide()
        self.ui.Image_5.hide()
        self.ui.Title.adjustSize()
        self.ui.Progress.setRange(0, self.n)
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)
        self.myApp = None

    def loading(self):
        self.ui.Progress.setValue(self.counter)
        if self.counter == int(self.n * 0.1):
            self.ui.Image_0.hide()
            self.ui.Image_1.show()
        elif self.counter == int(self.n * 0.3):
            self.ui.Image_1.hide()
            self.ui.Image_2.show()
        elif self.counter == int(self.n * 0.5):
            self.ui.Image_2.hide()
            self.ui.Image_3.show()
        elif self.counter == int(self.n * 0.7):
            self.ui.Image_3.hide()
            self.ui.Image_4.show()
        elif self.counter == int(self.n * 0.9):
            self.ui.Image_4.hide()
            self.ui.Image_5.show()
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()
            self.myApp = Dialog()
            self.myApp.show()

        self.counter += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
