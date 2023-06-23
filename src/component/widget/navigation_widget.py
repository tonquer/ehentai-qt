from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QFile, QEvent, Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QScroller, QScrollerProperties

from config import config
from config.setting import Setting
from interface.ui_navigation import Ui_Navigation
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str
from view.user.login_view import LoginView
from server import req, Server, Log


class NavigationWidget(QWidget, Ui_Navigation, QtTaskBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.resize(260, 800)
        self.__ani = QPropertyAnimation(self, b"geometry")
        self.__connect = None
        self.pictureData = ""
        f = QFile(u":/png/icon/logo_round.png")
        f.open(QFile.ReadOnly)
        self.picLabel.SetPicture(f.readAll())
        f.close()
        self.pushButton.clicked.connect(self.OpenLoginView)
        self.swichButton.clicked.connect(self.SwitchSite)
        self.swichButton.setText(Str.GetStr(Str.SwitchSite))
        self.picLabel.installEventFilter(self)
        self.picData = None

        self.isLogin = False

        self.offlineButton.SetState(False)
        self.offlineButton.Switch.connect(self.SwitchOffline)

        if Setting.IsGrabGesture.value:
            QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)
            propertiesOne = QScroller.scroller(self.scrollArea).scrollerProperties()
            propertiesOne.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0)
            propertiesOne.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            propertiesOne.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
            QScroller.scroller(self.scrollArea).setScrollerProperties(propertiesOne)

    def SwitchOffline(self, state):
        QtOwner().isOfflineModel = state
        return

    def SwitchSite(self):
        QtOwner().ShowLoading()
        if config.CurSite == "exhentai":
            self.SwitchSiteBack({"st": Status.Ok}, "e-hentai")
        else:
            self.AddHttpTask(req.GetIndexInfoReq(site="exhentai"), self.SwitchSiteBack, "exhentai")
        return

    def SetSwitchSite(self, site):
        config.CurSite = site
        self.siteLabel.setText(config.CurSite)
        self.UpdateSwitchSite()

    def UpdateSwitchSite(self):
        self.AddHttpTask(req.GetUserIdReq(), self._UpdateSwitchSiteBack)
        return

    def _UpdateSwitchSiteBack(self, data):
        # QtOwner().owner.loadingForm.close()
        st = data["st"]
        if st != Status.Ok:
            Log.Warn("get user name fail")
        else:
            Log.Warn("get user name  success, {}".format(data))
            userName = data.get("userName", "")
            self.SetUserName(userName)
        return


    def SwitchSiteBack(self, data, newSite):
        QtOwner().CloseLoading()
        st = data["st"]
        if st == Status.Ok:
            config.CurSite = newSite
            self.siteLabel.setText(config.CurSite)
            igneous = data.get("igneous")
            if igneous and igneous != "mystery":
                Setting.Igneous.SetValue(igneous)
            QtOwner().ShowMsg(Str.GetStr(Str.Ok))
            self.searchButton.click()
            # QtOwner().owner.SwitchWidgetAndClear(QtOwner().owner.subStackWidget.indexOf(QtOwner().owner.searchView))
        elif data.get("igneous") is not None:
            igneous = data.get("igneous")
            if igneous == "mystery":
                QtOwner().ShowError(Str.GetStr(Str.IgneousMystery))
            else:
                QtOwner().ShowError(Str.GetStr(Str.NotIgneous))
        else:
            QtOwner().ShowError(data)
        return

    def SetUserName(self, userName):
        config.CurLoginName = userName
        self.nameLabel.setText(userName)
        if userName:
            self.UpdatePicLimit()
        return

    def UpdatePicLimit(self):
        self.AddHttpTask(req.HomeReq(), self.UpdatePicLimitBack)
        return

    def UpdatePicLimitBack(self, data):
        if data["st"] == Status.Ok:
            curNum = data["curNum"]
            maxNum = data["maxNum"]
            self.limitLabel.setText("{}/{}".format(curNum, maxNum))

    def OpenLoginView(self):
        isAutoLogin = Setting.AutoLogin.value
        if self.isLogin:
            # self.SwitchSite()
            self.Logout()
            isAutoLogin = 0

        loginView = LoginView(QtOwner().owner, isAutoLogin)
        loginView.show()
        loginView.closed.connect(self.LoginSucBack)
        return

    def Logout(self):
        Server().isLogin = False
        self.isLogin = False
        self.pushButton.setText(Str.GetStr(Str.Login))
        self.SetUserName("")
        config.IsLogin = False
        # self.SwitchSiteBack({"st": Status.Ok}, "e-hentai")
        config.CurSite = "e-hentai"
        self.siteLabel.setText(config.CurSite)
        return

    def LoginSucBack(self):
        if self.isLogin:
            self.pushButton.setText(Str.GetStr(Str.LoginOut))

    def ShowUserImg(self, data, st):
        if st == Status.Ok:

            self.picData = data
            self.SetPicture(data)
        return

    def SetPicture(self, data):
        self.pictureData = data
        self.picLabel.SetPicture(data)
        return

    def aniShow(self):
        """ 动画显示 """
        super().show()
        self.activateWindow()
        self.__ani.setStartValue(QRect(self.x(), self.y(), 30, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 260, self.height()))
        self.__ani.setEasingCurve(QEasingCurve.InOutQuad)
        self.__ani.setDuration(85)
        self.__ani.start()

    def aniHide(self):
        """ 动画隐藏 """
        self.__ani.setStartValue(QRect(self.x(), self.y(), 260, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 30, self.height()))
        self.__connect = self.__ani.finished.connect(self.__hideAniFinishedSlot)
        self.__ani.setDuration(85)
        self.__ani.start()

    def __hideAniFinishedSlot(self):
        """ 隐藏窗体的动画结束 """
        super().hide()
        self.resize(60, self.height())
        if self.__connect:
            self.__ani.finished.disconnect()
            self.__connect = None

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                if self.picData and (obj == self.picLabel):
                    QtOwner().OpenWaifu2xTool(self.picData)
                    return True
                return False
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)

    def SetNewUpdate(self):
        icon2 = QIcon()
        icon2.addFile(u":/png/icon/new.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.helpButton.setIcon(icon2)
        return