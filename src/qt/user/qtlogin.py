import base64
import json

import requests
from PySide2 import QtWidgets, QtCore
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

from src.qt.com.qtmsg import QtMsgLabel
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
        self.cookieList = ["ipb_member_id", "ipb_pass_hash"]
        self.cookie = {}
        self.isLogin = False
        self.isTestLogin = False
        self.buttonGroup.buttonClicked.connect(self.UpdateEnable)

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
                    "ipb_pass_hash": self.cookie.get("ipb_pass_hash")
                }
                self.isLogin = True
                self.LoginByCookie(load_cookies)
        return

    def LoginByCookie(self, load_cookies):
        QtOwner().owner.loadingForm.show()
        Server().session.cookies = requests.utils.cookiejar_from_dict(load_cookies, cookiejar=None, overwrite=True)
        self.AddHttpTask(req.GetUserIdReq(), self.GetUserBack, dict(load_cookies))
        return

    def Login(self):
        userId = self.userIdEdit.text()
        passwd = self.passwdEdit.text()
        if self.userRadio.isChecked():
            QtOwner().owner.loadingForm.show()
            self.AddHttpTask(req.LoginReq(userId, passwd), self.LoginBack)
        else:
            hash = self.passLine.text()
            member = self.memberLine.text()
            if not hash or not member:
                QtOwner().ShowError(self.tr("不能为空"))
                return
            cookie = {
                "ipb_member_id": member,
                "ipb_pass_hash": hash,
            }
            igneous = self.igneousLine.text()
            if igneous:
                cookie["igneous"] = igneous
            self.LoginByCookie(cookie)

    def GetUserBack(self, data, load_cookies):
        if data["st"] != Status.Ok:
            Log.Warn("login fail, relogin")
            self.cookie.clear()
            self.isLogin = False
            QtMsgLabel().ShowErrorEx(self, self.tr("登陆失败"))
        else:
            Log.Warn("login success, {}, cookie".format(data, load_cookies))
            userName = data.get("userName", "")
            if load_cookies:
                QtOwner().owner.settingForm.SetSettingV("ipb_member_id", load_cookies.get("ipb_member_id", ""))
                QtOwner().owner.settingForm.SetSettingV("ipb_pass_hash", load_cookies.get("ipb_pass_hash", ""))
                QtOwner().owner.settingForm.SetSettingV("igneous", load_cookies.get("igneous", ""))
            self.SkipLogin(userName)
        return

    def LoginBack(self, data):
        QtOwner().owner.loadingForm.close()
        st = data["st"]
        if st == Status.Ok:
            QtOwner().owner.settingForm.SetSettingV("userId", self.userIdEdit.text())
            QtOwner().owner.settingForm.SetSettingV("ipb_member_id", data["ipb_member_id"])
            QtOwner().owner.settingForm.SetSettingV("ipb_pass_hash", data["ipb_pass_hash"])
            self.AddHttpTask(req.GetUserIdReq(), self.GetUserBack, {})
            self.isTestLogin = True
        elif st == Status.UserError:
            QtMsgLabel.ShowErrorEx(self, QtOwner().owner.GetStatusStr(st))
        elif st == Status.NeedGoogle:
            QtMsgLabel.ShowErrorEx(self, QtOwner().owner.GetStatusStr(st))
            self.isTestLogin = True
            self.isLogin = False
            self.OpenLoginUrl()
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

            QtOwner().owner.userForm.SetLoginName(str(userName))
        else:
            QtOwner().owner.userForm.toolButton1.hide()
        QtOwner().owner.userForm.toolButton0.click()
        return

    def OpenProxy(self):
        QtOwner().owner.loginProxyForm.show()

    def Init(self):
        userId = QtOwner().owner.settingForm.GetSettingV("UserId", "")
        passwd = QtOwner().owner.settingForm.GetSettingV("Passwd2", "")
        passwd = base64.b64decode(passwd).decode("utf-8") if passwd else ""
        memberId = QtOwner().owner.settingForm.GetSettingV("ipb_member_id", "")
        passHash = QtOwner().owner.settingForm.GetSettingV("ipb_pass_hash", "")
        igneous = QtOwner().owner.settingForm.GetSettingV("igneous", "")
        self.userIdEdit.setText(userId)
        self.passwdEdit.setText(passwd)
        self.memberLine.setText(memberId)
        self.passLine.setText(passHash)
        self.igneousLine.setText(igneous)
        if memberId and passHash:
            self.cookieRadio.setChecked(True)
            self.UpdateEnable()
        return

    def UpdateEnable(self):
        if self.userRadio.isChecked():
            enable = True
        else:
            enable = False
        self.userIdEdit.setEnabled(enable)
        self.userLabel.setEnabled(enable)
        self.passwdLabel.setEnabled(enable)
        self.passwdEdit.setEnabled(enable)
        self.memberLine.setEnabled(not enable)
        self.memberLabel.setEnabled(not enable)
        self.passLine.setEnabled(not enable)
        self.passLabel.setEnabled(not enable)
        self.igneousLine.setEnabled(not enable)
        self.igneousLabel.setEnabled(not enable)

