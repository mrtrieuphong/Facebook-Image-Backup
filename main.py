import os
import re
import threading
import webbrowser
import requests
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from home_ui import HomeClass
ROOT_DIR = os.path.abspath(os.curdir)
ICON_PATH = os.path.join(ROOT_DIR, 'static/logo.png')


def shortDir(file_dir):
    stringNum = len(file_dir)
    if stringNum > 35:
        file_dir = "..." + file_dir[-25:]
    return file_dir


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.ui = HomeClass()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.session = None
        self.saveDir = None
        self.url = None
        self.run = False
        self.shortSaveDir = None
        self.downloadID = None
        self.scan_thread = None
        self.ui.Stop0.hide()
        self.ui.Stop1.hide()
        self.setWindowIcon(QtGui.QIcon(ICON_PATH))
        self.ui.SaveFolder.clicked.connect(self.setSaveFolder)
        self.ui.TagPhotos.clicked.connect(self.downloadTaggedPhotos)
        self.ui.Uploaded.clicked.connect(self.downloadUploadedPhotos)
        self.ui.Exit.clicked.connect(self.close)
        self.ui.Mini.clicked.connect(self.showMinimized)
        self.ui.Name.clicked.connect(self.profile)
        self.ui.Stop0.clicked.connect(self.stopThread)
        self.ui.Stop1.clicked.connect(self.stopThread)
        urlLink = "<a href='https://www.facebook.com/phong.gtvt'>Nguyễn Triệu Phong</a>"
        self.ui.Author.setOpenExternalLinks(True)
        self.ui.Author.setText(urlLink)

    def stopThread(self):
        self.run = False
        self.ui.Stop0.hide()
        self.ui.Stop1.hide()
        self.ui.Uploaded.setDisabled(False)
        self.ui.TagPhotos.setDisabled(False)

    def profile(self):
        profile_link = "https://www.facebook.com/{}".format(self.session['c_user'])
        webbrowser.open(profile_link)

    def getName(self, name):
        self.ui.Name.setText(name)

    def getSession(self, session):
        self.session = session
        self.downloadID = self.session['c_user']

    def getDefaultSaveDir(self, default_dir):
        self.saveDir = os.path.dirname(default_dir)
        self.displaySaveDir()

    def setSaveFolder(self):
        self.saveDir = QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.displaySaveDir()

    def displaySaveDir(self):
        stringNum = len(self.saveDir)
        if stringNum > 20:
            self.shortSaveDir = "..." + os.path.join(self.saveDir, 'Export')[-20:]
        else:
            self.shortSaveDir = os.path.join(self.saveDir, 'Export')
        self.ui.SaveDir.setText(self.shortSaveDir)

    def scan(self):
        req = requests.Session()
        offset = 0
        input_url = self.url
        while self.run is True:
            if self.run is False:
                break
            url = "{}{}".format(input_url, offset)
            res = req.get(url, cookies=self.session)
            html_text = res.text
            match = re.findall(r"/photo.php\?fbid=([0-9]*)&amp;", html_text)
            if match:
                count = 0
                for m in match:
                    f = open("{}/{}.jpg".format(os.path.join(self.saveDir, 'Export'), m), "wb")
                    res = req.get("https://mbasic.facebook.com/photo/view_full_size/?fbid={}".format(m),
                                  cookies=self.session)
                    html_text = res.text
                    z = re.search(r"a href=\"(.*?)\"", html_text)
                    if z:
                        url = str(z.groups()[0]).replace("&amp;", "&")
                        res = req.get(url, cookies=self.session)
                        f.write(res.content)
                        f.close()
                        pixmap = QPixmap("{}/{}.jpg".format(os.path.join(self.saveDir, 'Export'), m))
                        height = pixmap.size().height()
                        width = pixmap.size().width()
                        if height >= width:
                            pixmap = pixmap.scaledToWidth(250)
                        else:
                            pixmap = pixmap.scaledToHeight(250)
                        self.ui.Image0.setPixmap(pixmap)
                        self.ui.Image0.show()
                        count += 1
                        self.ui.Image.setText("Image: {}".format(count))
                    else:
                        break
                offset += 12
                self.ui.Package.setText("Package: {}".format(int(offset / 12)))
            else:
                self.ui.Uploaded.setDisabled(False)
                self.ui.TagPhotos.setDisabled(False)
                break

    def importUserID(self):
        if not os.path.exists(os.path.join(self.saveDir, 'Export')):
            os.makedirs(os.path.join(self.saveDir, 'Export'))
        UserID = self.ui.ProfileInput.text()
        if UserID.isnumeric():
            self.downloadID = UserID
        elif len(UserID) > 3:
            req = requests.Session()
            url = "https://m.facebook.com/{}".format(UserID)
            res = req.get(url, cookies=self.session)
            html_text = res.text
            UID = html_text.split("profile_id=")[1].split("&amp")[0]
            self.downloadID = UID
        return self.downloadID

    def downloadTaggedPhotos(self):
        friend_id = self.importUserID()
        url_photo_tag = "https://mbasic.facebook.com/{}/photoset/pb.{}.-2207520000../?owner_id={}&offset=".format(
            friend_id, friend_id, friend_id)
        self.url = url_photo_tag
        self.run = True
        self.ui.Stop0.show()
        self.ui.Uploaded.setDisabled(True)
        self.scan_thread = threading.Thread(target=self.scan)
        self.scan_thread.start()

    def downloadUploadedPhotos(self):
        friend_id = self.importUserID()
        url_photo_upload = "https://mbasic.facebook.com/{}/photoset/t.{}/?owner_id={}&offset=".format(
            friend_id, friend_id, friend_id)
        self.url = url_photo_upload
        self.run = True
        self.ui.Stop1.show()
        self.ui.TagPhotos.setDisabled(True)
        self.scan_thread = threading.Thread(target=self.scan)
        self.scan_thread.start()