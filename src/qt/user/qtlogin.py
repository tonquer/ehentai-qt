import json

import requests
from PySide2 import QtWidgets, QtCore
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.qt_main import QtOwner
from src.qt.user.qt_login_web import QtLoginWeb
from src.qt.util.qttask import QtTaskBase
from src.server import Server, req, Log
from src.util.status import Status
from ui.login import Ui_Login


class QtLogin(QtWidgets.QWidget, Ui_Login, QtTaskBase):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_Login.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("登陆")
        self.speedTest = []
        self.speedIndex = 0
        self.cookieList = ["ipb_session_id", "ipb_member_id", "ipb_pass_hash"]
        self.cookie = {}
        self.isLogin = False
        self.isTestLogin = False

    def OpenLoginUrl(self):
        QtOwner().owner.stackedWidget.setCurrentIndex(2)
        QtOwner().owner.loginWebForm.OpenUrl(self.userIdEdit.text(), self.passwdEdit.text())

    def SaveCookie(self, cookie):
        if ".e-hentai.org" in cookie.domain():
            if str(cookie.name(), encoding='utf-8') in self.cookieList:
                self.cookie[str(cookie.name(), encoding='utf-8')] = str(cookie.value(), encoding='utf-8')
            isClose = True
            if self.isLogin:
                return
            for i in self.cookieList:
                if i not in self.cookie:
                    isClose = False
            if isClose:
                QtOwner().owner.stackedWidget.setCurrentIndex(0)
                load_cookies = {
                    "ipb_member_id": self.cookie.get("ipb_member_id"),
                    "ipb_pass_hash": self.cookie.get("ipb_pass_hash"),
                    "ipb_session_id": self.cookie.get("ipb_session_id")
                }
                self.isLogin = True
                self.LoginByCookie(load_cookies)
        return

    def LoginByCookie(self, load_cookies):
        QtOwner().owner.loadingForm.show()
        Server().session.cookies = requests.utils.cookiejar_from_dict(load_cookies, cookiejar=None, overwrite=True)
        self.AddHttpTask(req.GetUserIdReq(), self.GetUserBack)
        return

    def Login(self):
        userId = self.userIdEdit.text()
        passwd = self.passwdEdit.text()
        lastUserId = QtOwner().owner.settingForm.GetSettingV("userId", "")
        memberId = QtOwner().owner.settingForm.GetSettingV("ipb_member_id", "")
        passHash = QtOwner().owner.settingForm.GetSettingV("ipb_pass_hash", "")
        sessionId = QtOwner().owner.settingForm.GetSettingV("ipb_session_id", "")
        if userId == lastUserId and memberId and passHash:
            load_cookies = {
                "ipb_member_id": memberId,
                "ipb_pass_hash": passHash,
                "ipb_session_id": sessionId
            }
            self.LoginByCookie(load_cookies)
        else:

            if self.isTestLogin:
                self.OpenLoginUrl()
            else:
                QtOwner().owner.loadingForm.show()
                self.AddHttpTask(req.LoginReq(userId, passwd), self.LoginBack)

    def GetUserBack(self, data):
        if data["st"] != Status.Ok:
            Log.Warn("login fail, relogin")
            self.cookie.clear()
            self.isLogin = False
            QtBubbleLabel().ShowErrorEx(self, "登陆失败")
        else:
            Log.Warn("login success, {}".format(data))
            userName = data.get("userName", "")
            if self.cookie:
                QtOwner().owner.settingForm.SetSettingV("userId", userName)
                QtOwner().owner.settingForm.SetSettingV("ipb_member_id", self.cookie.get("ipb_member_id", ""))
                QtOwner().owner.settingForm.SetSettingV("ipb_pass_hash", self.cookie.get("ipb_pass_hash"))
                QtOwner().owner.settingForm.SetSettingV("ipb_session_id", self.cookie.get("ipb_session_id"))
                QtOwner().owner.settingForm.SetSettingV("ipb_coppa", self.cookie.get("ipb_coppa"))
            self.SkipLogin(userName)
        return

    def LoginBack(self, data):
        QtOwner().owner.loadingForm.close()
        st = data["st"]
        if st == Status.Ok:
            QtOwner().owner.settingForm.SetSettingV("userId", self.userIdEdit.text())
            QtOwner().owner.settingForm.SetSettingV("ipb_member_id", data["ipb_member_id"])
            QtOwner().owner.settingForm.SetSettingV("ipb_pass_hash", data["ipb_pass_hash"])
            QtOwner().owner.settingForm.SetSettingV("ipb_session_id", data["ipb_session_id"])
            QtOwner().owner.settingForm.SetSettingV("ipb_coppa", data["ipb_coppa"])
            self.AddHttpTask(req.GetUserIdReq(), self.GetUserBack)
            self.isTestLogin = True
        elif st == Status.UserError:
            QtBubbleLabel.ShowErrorEx(self, st)
        else:
            self.isTestLogin = True
            self.isLogin = False
            self.OpenLoginUrl()

    def UpdateUserBack(self, msg):
        return

    def ShowUserImg(self, data, st):
        if st == Status.Ok:
            QtOwner().owner.userForm.SetPicture(data)

    def SkipLogin(self, userName=""):
        QtOwner().owner.stackedWidget.setCurrentIndex(1)
        if isinstance(userName, str):
            QtOwner().owner.userForm.name.setText(str(userName))
        else:
            QtOwner().owner.userForm.toolButton1.hide()
        QtOwner().owner.userForm.toolButton0.click()
        return

    def Init(self):
        return

