import os
import requests
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel
from cookie import getCookie
from login_ui import LoginClass
from main import Window
ROOT_DIR = os.path.abspath(os.curdir)
ICON_PATH = os.path.join(ROOT_DIR, 'static/logo.png')


def shortDir(file_dir):
    stringNum = len(file_dir)
    if stringNum > 35:
        file_dir = "..." + file_dir[-25:]
    return file_dir


class Dialog(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.ui = LoginClass()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.ui.Login.setEnabled(False)
        self.openFileNameLabel = QLabel()
        self.fileDir = None
        self.fileName = None
        self.cookie = None
        self.session = None
        self.name = None
        self.home = None
        self.ui.Exit.clicked.connect(self.close)
        self.ui.Mini.clicked.connect(self.showMinimized)
        self.ui.Browser.clicked.connect(self.setOpenFileName)
        self.ui.Login.clicked.connect(self.logIn)

    def setOpenFileName(self):
        self.fileDir, _ = QFileDialog.getOpenFileName(
            self,
            "Open cookie file", self.openFileNameLabel.text(),
            "JSON (*.json)"
        )
        if self.fileDir:
            self.ui.Login.setEnabled(True)
            stringNum = len(self.fileDir)

            if stringNum > 25:
                self.fileName = "..." + self.fileDir[-25:]
            else:
                self.fileName = self.fileDir
            self.ui.Filename.setText(self.fileName)
            self.cookie = getCookie(self.fileDir)
            if self.cookie:
                self.ui.Login.setEnabled(True)
            else:
                self.ui.Filename.setText("Load cookie fail!")

    def logIn(self):
        self.session = {
            "c_user": self.cookie[0],
            "xs": self.cookie[1]
        }
        req = requests.Session()
        url = "{}{}".format("https://mbasic.facebook.com/profile.php", 0)
        res = req.get(url, cookies=self.session)
        content = res.text
        self.name = content.split('id="mbasic_logout_button">')[1].split("</a>")[0].split('(')[1].strip(')')
        if self.name:
            self.close()
            self.home = Window()
            self.home.getName(self.name)
            self.home.getSession(self.session)
            self.home.getDefaultSaveDir(self.fileDir)
            self.home.show()
