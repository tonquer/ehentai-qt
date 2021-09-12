import json
import weakref

import requests
from PySide2 import QtWidgets, QtGui  # 导入PySide2部件
from PySide2.QtCore import QSettings, QLocale, QTranslator
from PySide2.QtGui import QDesktopServices

from conf import config
from src.server import req, Singleton, Server
from src.util import Log, ToolUtil
from src.util.status import Status
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

    def SetDirty(self):
        self.owner.userForm.SetDirty()

    def ShowMsg(self, data):
        return self.owner.msgForm.ShowMsg(data)

    def ShowError(self, data):
        return self.owner.msgForm.ShowError(data)

    def GetV(self, k, defV=""):
        return self.owner.settingForm.GetSettingV(k, defV)

    def SetV(self, k, v):
        return self.owner.settingForm.SetSettingV(k, v)

    def ShowMsgBox(self, type, title, msg):
        msg = QMessageBox(type, title, msg)
        msg.addButton("Yes", QMessageBox.AcceptRole)
        if type == QMessageBox.Question:
            msg.addButton("No", QMessageBox.RejectRole)
        if config.ThemeText == "flatblack":
            msg.setStyleSheet("QWidget{background-color:#2E2F30}")
        return msg.exec_()


class QtMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        config.Language = QSettings('config.ini', QSettings.IniFormat).value('Language', '')

        self.translator_about = None
        self.translator_bookinfo = None
        self.translator_booksimple = None
        self.translator_category = None
        self.translator_chatroom = None
        self.translator_chatroomsg = None
        self.translator_comment = None
        self.translator_download = None
        self.translator_favorite = None
        self.translator_favorite_info = None
        self.translator_fried = None
        self.translator_fried_msg = None
        self.translator_game = None
        self.translator_gameinfo = None
        self.translator_history = None
        self.translator_img = None
        self.translator_index = None
        self.translator_leavemsg = None
        self.translator_loading = None
        self.translator_login = None
        self.translator_login_proxy = None
        self.translator_main = None
        self.translator_qtespinfo = None
        self.translator_rank = None
        self.translator_readimg = None
        self.translator_register = None
        self.translator_search = None
        self.translator_setting = None
        self.translator_user = None
        self.translator_user_info = None
        self.translator_common = None
        self.translator_dns = None

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self._app = weakref.ref(app)
        self.LoadTranslate()

        self.userInfo = None
        self.setupUi(self)
        self.setWindowTitle("E-hentai")
        QtOwner().SetOwner(self)

        self.tags = {}
        self.words = []
        self.InitWords()
        from src.qt.main.qt_favorite_info import QtFavoriteInfo
        from src.qt.com.qtmsg import QtMsgLabel
        from src.qt.menu.qtabout import QtAbout
        from src.qt.menu.qtsetting import QtSetting
        from src.qt.com.qtloading import QtLoading
        from src.qt.main.qtsearch import QtSearch
        from src.qt.read.qtbookinfo import QtBookInfo
        from src.qt.read.qtreadimg import QtReadImg
        from src.qt.user.qtlogin import QtLogin
        from src.qt.user.qtuser import QtUser

        from src.qt.util.qttask import QtTask
        from src.qt.user.qt_login_web import QtLoginWeb

        self.settingForm = QtSetting(self)
        self.qtReadImg = QtReadImg()
        self.settingForm.LoadSetting()
        self.qtReadImg.LoadSetting()

        self.loginWebForm = QtLoginWeb(self)
        self.msgForm = QtMsgLabel(self)
        self.loginForm = QtLogin(self)
        self.searchForm = QtSearch(self)
        from src.qt.main.qt_favorite import QtFavorite
        self.favoriteForm = QtFavorite(self)
        self.loadingForm = QtLoading(self)
        from src.qt.download.qtdownload import QtDownload
        self.downloadForm = QtDownload()
        self.qtTask = QtTask()
        self.userForm = QtUser(self)
        self.favoriteInfoForm = QtFavoriteInfo(self)

        self.stackedWidget.addWidget(self.loginForm)
        self.stackedWidget.addWidget(self.userForm)
        self.stackedWidget.addWidget(self.loginWebForm)
        from src.qt.menu.qt_dns import QtDns
        self.dohDnsForm = QtDns(self)
        self.bookInfoForm = QtBookInfo()

        if self.settingForm.mainSize:
            self.resize(self.settingForm.mainSize)
        else:
            desktop = QDesktopWidget()
            self.resize(desktop.width() // 4 * 2, desktop.height() // 4 * 2)
            self.move(desktop.width() // 4, desktop.height() // 4)
        self.bookInfoForm.resize(self.settingForm.bookSize)
        self.qtReadImg.resize(self.settingForm.readSize)

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

    def LoadTranslate(self):
        installTag = ""
        if config.Language == "":
            locale = QLocale.system().name()
            Log.Info("Init translate {}".format(locale))
            if locale[:3].lower() == "zh_":
                if locale.lower() != "zh_cn":
                    config.Language = "Chinese-Traditional"
                    installTag = "tc"
                else:
                    config.Language = "Chinese-Simplified"

            else:
                config.Language = "English"

        if config.Language == "Chinese-Traditional":
            install = True
            installTag = "tc"
        elif config.Language == "English":
            install = True
            installTag = "en"
        else:
            install = False

        self.loadTrans(self.app, 'about', installTag, install)
        self.loadTrans(self.app, 'bookinfo', installTag, install)
        self.loadTrans(self.app, 'common', installTag, install)
        self.loadTrans(self.app, 'comment', installTag, install)
        self.loadTrans(self.app, 'download', installTag, install)
        self.loadTrans(self.app, 'img', installTag, install)
        self.loadTrans(self.app, 'favorite', installTag, install)
        self.loadTrans(self.app, 'favorite_info', installTag, install)

        self.loadTrans(self.app, 'login', installTag, install)
        self.loadTrans(self.app, 'dns', installTag, install)

        self.loadTrans(self.app, 'main', installTag, install)
        self.loadTrans(self.app, 'readimg', installTag, install)
        self.loadTrans(self.app, 'search', installTag, install)
        self.loadTrans(self.app, 'setting', installTag, install)
        self.loadTrans(self.app, 'user', installTag, install)

    def loadTrans(self, app, ui, lang, isInstall):
        setattr(self, "translator_{0}".format(ui), QTranslator())
        translator = getattr(self, "translator_{0}".format(ui))
        translator.load(QLocale(), "./translate/{0}_{1}.qm".format(ui, lang))
        if isInstall:
            if not app.installTranslator(translator):
                Log.Warn("{0}_{1}.qm load failed".format(ui, lang))
        else:
            app.removeTranslator(translator)

    def RetranslateUi(self):
        self.retranslateUi(self)
        self.aboutForm.retranslateUi(self.aboutForm)
        self.bookInfoForm.retranslateUi(self.bookInfoForm)
        self.downloadForm.retranslateUi(self.downloadForm)
        self.qtReadImg.qtTool.retranslateUi(self.qtReadImg.qtTool)
        self.loginForm.retranslateUi(self.loginForm)
        self.searchForm.retranslateUi(self.searchForm)
        self.settingForm.retranslateUi(self.settingForm)
        self.userForm.retranslateUi(self.userForm)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        super().closeEvent(a0)
        userId = self.loginForm.userIdEdit.text()
        passwd = self.loginForm.passwdEdit.text()
        self.bookInfoForm.close()
        self.settingForm.ExitSaveSetting(self.size(), self.bookInfoForm.size(), self.qtReadImg.size(), userId, passwd)

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

    def OpenSetting(self, action):
        if action.text() == "setting":
            self.settingForm.show()
        elif action.text() == "login":
            self.downloadForm.StopAll()
            # 清除cookie
            Server().session = requests.session()
            self.stackedWidget.setCurrentIndex(0)
            self.loginForm.Init()
        pass

    def InitUpdate(self):
        from src.qt.util.qttask import QtTask
        QtTask().AddHttpTask(req.CheckUpdateReq(config.UpdateUrl), self.InitUpdateBack)

    def InitUpdateBack(self, data):
        try:
            if not data:
                self.qtTask.AddHttpTask(req.CheckUpdateReq(config.UpdateUrlBack), self.InitUpdateBack2)
                return
            r = QMessageBox.information(self, self.tr("更新"), self.tr("当前版本") + config.UpdateVersion + ", "+ self.tr("检查到更新，是否前往更新\n") + data,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2))
        except Exception as es:
            Log.Error(es)

    def InitUpdateBack2(self, data):
        try:
            if not data:
                return
            r = QMessageBox.information(self, self.tr("更新"), self.tr("当前版本") + config.UpdateVersion + ", "+ self.tr("检查到更新，是否前往更新\n") + data,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if r == QMessageBox.Yes:
                QDesktopServices.openUrl(QUrl(config.UpdateUrl2Back))
        except Exception as es:
            Log.Error(es)

    def Init(self):
        from src.qt.user.login_web_proxy import Init as ProxyInit
        ProxyInit()
        from src.qt.util.qt_domain import QtDomainMgr
        QtDomainMgr().Update()
        self.loginWebForm.Init()
        IsCanUse = False
        if config.CanWaifu2x:
            import waifu2x
            stat = waifu2x.init()
            if stat < 0:
                self.msgForm.ShowError(self.tr("waifu2x初始化错误"))
            else:
                IsCanUse = True
                gpuInfo = waifu2x.getGpuInfo()
                if gpuInfo:
                    self.settingForm.SetGpuInfos(gpuInfo)
                if gpuInfo and config.Encode < 0:
                    config.Encode = 0

                waifu2x.initSet(config.Encode, config.Waifu2xThread)
                Log.Info(self.tr("waifu2x初始化: ") + str(stat) + " encode: " + str(config.Encode) + " version:" + waifu2x.getVersion())
                # self.msgForm.ShowMsg("waifu2x初始化成功\n" + waifu2x.getVersion())
        else:
            self.msgForm.ShowError(self.tr("waifu2x无法启用, ")+config.ErrorMsg)

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

    def GetCategoryName(self, category):
        if config.Language != "English":
            return ToolUtil.Category.get(category.lower())
        return category

    def OpenAbout(self, action):
        from src.qt.com.qtimg import QtImgMgr
        if action.text() == "about":
            self.aboutForm.show()
        elif action.text() == "waifu2x":
            QtImgMgr().ShowImg("")
        elif action.text() == "Doh dns":
           self.dohDnsForm.show()
        pass

    def Stop(self):
        from src.qt.user.login_web_proxy import Stop as ProxyStop
        ProxyStop()

    def GetStatusStr(self, data):
        if data == Status.NetError:
            return self.tr("网络错误，请检查代理设置")
        elif data == Status.UserError:
            return self.tr("用户名密码错误")
        elif data == Status.RegisterError:
            return self.tr("注册失败")
        elif data == Status.NotFoundBook:
            return self.tr("未找到书籍")
        elif data == Status.ParseError:
            return self.tr("解析出错了")
        elif data == Status.NeedGoogle:
            return self.tr("需要谷歌验证")
        return data