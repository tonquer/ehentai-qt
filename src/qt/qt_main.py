import json

from PySide2 import QtWidgets  # 导入PySide2部件
from PySide2.QtGui import QDesktopServices

from conf import config
import weakref

from src.server import req, Singleton
from src.util import Log, ToolUtil
from ui.main import Ui_MainWindow, QDesktopWidget, QMessageBox, QUrl


class QtOwner(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self._owner = None

    @property
    def owner(self):
        assert isinstance(self._owner(), QtMainWindow)
        return self._owner()

    def SetOwner(self, owner):
        self._owner = weakref.ref(owner)


class QtMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.userInfo = None
        self.setupUi(self)
        self.setWindowTitle("E-hentai")
        QtOwner().SetOwner(self)
        self._app = weakref.ref(app)
        self.tags = {}
        self.words = []
        self.InitWords()
        from src.qt.main.qt_favorite_info import QtFavoriteInfo
        from src.qt.com.qtbubblelabel import QtBubbleLabel
        from src.qt.menu.qtabout import QtAbout
        from src.qt.menu.qtsetting import QtSetting
        from src.qt.com.qtloading import QtLoading
        from src.qt.main.qtsearch import QtSearch
        from src.qt.read.qtbookinfo import QtBookInfo
        from src.qt.read.qtreadimg import QtReadImg
        from src.qt.user.qtlogin import QtLogin
        from src.qt.user.qtuser import QtUser

        from src.qt.user.qt_login_web import QtLoginWeb

        self.loginWebForm = QtLoginWeb(self)
        self.msgForm = QtBubbleLabel(self)
        self.loginForm = QtLogin(self)
        self.searchForm = QtSearch(self)
        from src.qt.main.qt_favorite import QtFavorite
        self.favoriteForm = QtFavorite(self)
        self.loadingForm = QtLoading(self)
        self.userForm = QtUser(self)
        self.favoriteInfoForm = QtFavoriteInfo(self)
        self.stackedWidget.addWidget(self.loginForm)
        self.stackedWidget.addWidget(self.userForm)
        self.stackedWidget.addWidget(self.loginWebForm)

        self.bookInfoForm = QtBookInfo()
        self.qtReadImg = QtReadImg()

        self.settingForm = QtSetting(self)
        self.settingForm.LoadSetting()

        if self.settingForm.mainSize:
            self.resize(self.settingForm.mainSize)
        else:
            desktop = QDesktopWidget()
            self.resize(desktop.width() // 4 * 2, desktop.height() // 4 * 2)
            self.move(desktop.width() // 4, desktop.height() // 4)
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
        ToolUtil.SetIcon(self)

    @property
    def app(self):
        return self._app()

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
        from src.qt.util.qttask import QtTask
        QtTask().AddHttpTask(req.CheckUpdateReq(config.UpdateUrl), self.InitUpdateBack)

    def InitUpdateBack(self, data):
        try:
            if not data:
                from src.qt.util.qttask import QtTask
                QtTask().AddHttpTask(req.CheckUpdateReq(config.UpdateUrlBack), self.InitUpdateBack2)
                return
            r = QMessageBox.information(self, "更新", "当前版本{} ,检查到更新，是否前往更新\n{}".format(config.UpdateVersion,
                                                                                        data),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2))
        except Exception as es:
            Log.Error(es)

    def InitUpdateBack2(self, data):
        try:
            if not data:
                return
            r = QMessageBox.information(self, "更新", "当前版本{} ,检查到更新，是否前往更新\n{}".format(config.UpdateVersion,
                                                                                        data),
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2Back))
        except Exception as es:
            Log.Error(es)

    def Init(self):
        from src.qt.com.qtimg import QtImgMgr
        IsCanUse = False
        if config.CanWaifu2x:
            import waifu2x
            stat = waifu2x.init()
            if stat < 0:
                self.msgForm.ShowError("waifu2x初始化错误")
            else:
                IsCanUse = True
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

        if not IsCanUse:
            self.settingForm.checkBox.setEnabled(False)
            self.qtReadImg.frame.qtTool.checkBox.setEnabled(False)
            config.DownloadAuto = 0
            self.downloadForm.radioButton.setEnabled(False)
            from src.qt.com.qtimg import QtImgMgr
            QtImgMgr().obj.checkBox.setEnabled(False)
            QtImgMgr().obj.changeButton.setEnabled(False)
            QtImgMgr().obj.changeButton.setEnabled(False)
            QtImgMgr().obj.comboBox.setEnabled(False)
            QtImgMgr().obj.SetStatus(False)
            config.IsOpenWaifu = 0

        self.InitUpdate()
        self.loginForm.Init()

    def OpenAbout(self, action):
        from src.qt.com.qtimg import QtImgMgr
        if action.text() == "about":
            self.aboutForm.show()
        elif action.text() == "waifu2x":
            QtImgMgr().ShowImg("")
        pass
