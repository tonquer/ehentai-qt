import requests

from component.dialog.base_mask_dialog import BaseMaskDialog
from config import config
from config.setting import Setting
from interface.ui_login import Ui_Login
from qt_owner import QtOwner
from server import req, Server
from tools.log import Log
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str


class LoginView(BaseMaskDialog, Ui_Login, QtTaskBase):
    def __init__(self, parent=None):
        BaseMaskDialog.__init__(self, parent)
        Ui_Login.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self.widget)
        self.switchButton.clicked.connect(self._SwitchLoginMode)
        self.closeButton.clicked.connect(self.close)
        self.loginButton.clicked.connect(self.Login)
        self.loginModel = True
        self.SetLoginMode()
        self.SetErrMsg()

        self.cookieList = ["ipb_member_id", "ipb_pass_hash"]
        self.cookie = {}
        self.isLogin = False
        self.isTestLogin = False
        self.protyButton.clicked.connect(self.OpenSetting)
        if Setting.IpbMemberId.value:
            self._SwitchLoginMode()
            self.memberLabel.setText(Setting.IpbMemberId.value)
            self.hashLabel.setText(Setting.IpbPassHash.value)
            self.igneousLabel.setText(Setting.Igneous.value)

    def _SwitchLoginMode(self):
        self.loginModel = not self.loginModel
        self.SetLoginMode()

    def SetErrMsg(self, textType=0):
        if not textType:
            self.errLabel.setVisible(False)
            return
        self.errLabel.setVisible(True)
        self.errLabel.setText(Str.GetStr(textType))
        return

    def SetLoginMode(self):
        if not self.loginModel:
            self.stackedWidget.setCurrentIndex(1)
            self.switchButton.setText(Str.GetStr(Str.LoginUser))
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.switchButton.setText(Str.GetStr(Str.LoginCookie))
        return

    def Login(self):
        self.SetErrMsg()
        userId = self.userEdit.text()
        passwd = self.passwdEdit.text()
        if self.loginModel:
            if not userId or not passwd:
                self.SetErrMsg(Str.NotSpace)
                return
            QtOwner().ShowLoading()
            self.AddHttpTask(req.LoginReq(userId, passwd), self._LoginBack)
        else:
            hash = self.hashLabel.text()
            member = self.memberLabel.text()
            if not hash or not member:
                self.SetErrMsg(Str.NotSpace)
                return
            cookie = {
                "ipb_member_id": member,
                "ipb_pass_hash": hash,
            }
            igneous = self.igneousLabel.text()
            if igneous:
                cookie["igneous"] = igneous
            self.LoginByCookie(cookie)

    def SetCookie(self, cookie):
        if cookie:
            self.loginModel = False
            self.SetLoginMode()
            self.cookie = cookie[:]
            self.memberLabel.setText(self.cookie.get("ipb_member_id"))
            self.hashLabel.setText(self.cookie.get("ipb_pass_hash"))
            self.igneousLabel.setText(self.cookie.get("igneous", ""))
        return

    def LoginByCookie(self, load_cookies):
        # QtOwner().owner.loadingForm.show()
        QtOwner().ShowLoading()
        Server().session.cookies = requests.utils.cookiejar_from_dict(load_cookies, cookiejar=None, overwrite=True)
        self.AddHttpTask(req.GetUserIdReq(), self._GetUserBack, dict(load_cookies))
        return

    def _LoginBack(self, data):
        # QtOwner().owner.loadingForm.close()
        QtOwner().CloseLoading()
        st = data["st"]
        if st == Status.Ok:
            # QtOwner().owner.settingForm.SetSettingV("userId", self.userEdit.text())
            # QtOwner().owner.settingForm.SetSettingV("ipb_member_id", data["ipb_member_id"])
            # QtOwner().owner.settingForm.SetSettingV("ipb_pass_hash", data["ipb_pass_hash"])
            memberId = data["ipb_member_id"]
            passHash = data["ipb_pass_hash"]
            Setting.IpbMemberId.SetValue(memberId)
            Setting.IpbPassHash.SetValue(passHash)
            self.AddHttpTask(req.GetUserIdReq(), self._GetUserBack, {})
            self.isTestLogin = True
        elif st == Status.UserError:
            self.SetErrMsg(Str.UserError)
        elif st == Status.NeedGoogle:
            self.SetErrMsg(Str.NeedGoogle)
            self.isTestLogin = True
            self.isLogin = False
            self.OpenLoginUrl()
        else:
            self.isTestLogin = True
            self.isLogin = False
            self.OpenLoginUrl()

    def OpenLoginUrl(self):
        self.close()
        QtOwner().OpenLoginWebView(self.userEdit.text(), self.passwdEdit.text())
        return

    def OpenSetting(self):
        self.close()
        QtOwner().owner.navigationWidget.settingButton.click()
        return

    def _GetUserBack(self, data, load_cookies):
        # QtOwner().owner.loadingForm.close()
        QtOwner().CloseLoading()
        if data["st"] != Status.Ok:
            Log.Warn("login fail, relogin")
            self.cookie.clear()
            self.isLogin = False
            self.SetErrMsg(Str.LoginFail)
        else:
            Log.Warn("login success, {}, cookie".format(data, load_cookies))
            userName = data.get("userName", "")
            self.close()
            QtOwner().owner.LoginSucBack(userName)
            # if load_cookies:
                # QtOwner().owner.settingForm.SetSettingV("ipb_member_id", load_cookies.get("ipb_member_id", ""))
                # QtOwner().owner.settingForm.SetSettingV("ipb_pass_hash", load_cookies.get("ipb_pass_hash", ""))
                # QtOwner().owner.settingForm.SetSettingV("igneous", load_cookies.get("igneous", ""))
            # self.SkipLogin(userName)
        return
