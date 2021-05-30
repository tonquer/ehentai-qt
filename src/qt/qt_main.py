import json

from conf import config
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtimg import QtImgMgr
from src.qt.menu.qtabout import QtAbout
from src.qt.menu.qtsetting import QtSetting
from src.qt.com.qtloading import QtLoading
from src.qt.main.qtsearch import QtSearch
from src.qt.read.qtbookinfo import QtBookInfo
from src.qt.read.qtreadimg import QtReadImg
from src.qt.user.qtlogin import QtLogin
from src.qt.user.qtuser import QtUser
from src.qt.util.qttask import QtTask
from src.server import req
from src.util import Log
from ui.main import Ui_MainWindow, QDesktopWidget, QMessageBox, QUrl
from PySide2 import QtWidgets  # 导入PySide2部件
from PySide2.QtGui import QDesktopServices


class QtMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.userInfo = None
        self.setupUi(self)
        self.setWindowTitle("E-hentai")

        self.tags = {}
        self.words = []
        self.InitWords()

        self.msgForm = QtBubbleLabel(self)
        self.loginForm = QtLogin(self)
        self.searchForm = QtSearch(self)
        self.loadingForm = QtLoading(self)
        self.userForm = QtUser(self)
        self.stackedWidget.addWidget(self.loginForm)
        self.stackedWidget.addWidget(self.userForm)

        self.bookInfoForm = QtBookInfo(self)
        self.qtReadImg = QtReadImg(self)

        self.settingForm = QtSetting(self)
        self.settingForm.LoadSetting()

        self.resize(self.settingForm.mainSize)
        self.bookInfoForm.resize(self.settingForm.bookSize)
        self.qtReadImg.resize(self.settingForm.readSize)

        self.loginForm.userIdEdit.setText(self.settingForm.userId)
        self.loginForm.passwdEdit.setText(self.settingForm.passwd)

        self.menusetting.triggered.connect(self.OpenSetting)
        desktop = QDesktopWidget()
        self.resize(desktop.width() // 2, desktop.height() // 2)
        self.move(desktop.width() // 4, desktop.height() // 4)
        self.aboutForm = QtAbout(self)
        self.menuabout.triggered.connect(self.OpenAbout)

    def InitWords(self):
        try:
            f = open("database/translate.json", "r")
            data = f.read()
            f.close()
            self.tags = json.loads(data)
            words = []
            for data in self.tags.values():
                # if data.get('key') == 'character':
                for info in data.get('data', {}).values():
                    words.append(data.get('key', "") + ":" + info.get('src') + "|" + info.get('dest'))
            self.words = words
        except Exception as es:
            Log.Error(es)

    def OpenSetting(self):
        self.settingForm.show()
        pass

    def InitUpdate(self):
        QtTask().AddHttpTask(req.CheckUpdateReq(), self.InitUpdateBack)

    def InitUpdateBack(self, data):
        try:
            r = QMessageBox.information(self, "更新", "当前版本{} ,检查到更新，是否前往更新\n{}".format(config.UpdateVersion,
                                                                                        data),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2))
        except Exception as es:
            Log.Error(es)

    def Init(self):
        if config.CanWaifu2x:
            import waifu2x
            stat = waifu2x.init()
            if stat < 0:
                self.msgForm.ShowError("waifu2x初始化错误")
            else:
                gpuInfo = waifu2x.getGpuInfo()
                if gpuInfo:
                    self.settingForm.SetGpuInfos(gpuInfo)
                if gpuInfo and config.Encode < 0:
                    config.Encode = 0

                waifu2x.initSet(config.Encode, config.Waifu2xThread)
                Log.Info("waifu2x初始化: " + str(stat) + " encode: " + str(config.Encode) + " version:" + waifu2x.getVersion())
                # self.msgForm.ShowMsg("waifu2x初始化成功\n" + waifu2x.getVersion())
        else:
            self.msgForm.ShowError("waifu2x无法启用, "+config.ErrorMsg)
            self.settingForm.checkBox.setEnabled(False)
            self.qtReadImg.frame.qtTool.checkBox.setEnabled(False)
            config.IsOpenWaifu = 0
            QtImgMgr().obj.checkBox.setEnabled(False)
            QtImgMgr().obj.changeButton.setEnabled(False)
            QtImgMgr().obj.changeButton.setEnabled(False)
            QtImgMgr().obj.comboBox.setEnabled(False)
            QtImgMgr().obj.SetStatus(False)

        self.InitUpdate()
        self.loginForm.Init()

    def OpenAbout(self, action):
        if action.text() == "about":
            self.aboutForm.show()
        elif action.text() == "waifu2x":
            QtImgMgr().ShowImg("")
        pass
