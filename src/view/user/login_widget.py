import base64
from functools import partial

from PySide6 import QtWidgets

from config.setting import Setting, SettingValue
from interface.ui_login_widget import Ui_LoginWidget
from qt_owner import QtOwner
from server import req, Status, config, Log, Server
from task.qt_task import QtTaskBase
from tools.str import Str


class LoginWidget(QtWidgets.QWidget, Ui_LoginWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        # self.buttonGroup = QtWidgets.QButtonGroup(self)
        # self.buttonGroup.addButton(self.selectIp1)
        # self.selectIp1.setChecked(True)
        self.autoBox.setChecked(bool(Setting.AutoLogin.value))
        self.loginOpen.setChecked(bool(Setting.LoginOpen.value))
        # self.saveBox.setChecked(bool(Setting.SavePassword.value))
        self.autoBox.clicked.connect(partial(self.CheckButtonEvent, Setting.AutoLogin, self.autoBox))
        self.loginOpen.clicked.connect(partial(self.CheckButtonEvent, Setting.LoginOpen, self.loginOpen))
        # self.saveBox.clicked.connect(partial(self.CheckButtonEvent, Setting.SavePassword, self.saveBox))

    def CheckButtonEvent(self, setItem, button):
        assert isinstance(setItem, SettingValue)
        setItem.SetValue(int(button.isChecked()))
        return

    def Init(self):
        # self.userEdit_2.setText()
        # request = req.InitReq()
        # request.proxy = {}
        # self.AddHttpTask(request, self.InitBack)
        return

    def ClickButton(self):
        self.Login()

    def Login(self):
        QtOwner().ShowLoading()
        ipb_member_id = self.memberId.text()
        ipb_pass_hash = self.passHash.text()
        if not ipb_member_id or not ipb_pass_hash:
            return
        Server().isLogin = True
        Setting.IpbMemberId.SetValue(ipb_member_id)
        Setting.IpbPassHash.SetValue(ipb_pass_hash)
        Setting.Igneous.SetValue(self.igneous.text())
        self.AddHttpTask(req.GetUserIdReq(), self._GetUserBack)
        # self.close()
        # self.owner().show()

    def _GetUserBack(self, data):
        # QtOwner().owner.loadingForm.close()
        QtOwner().CloseLoading()
        st = data["st"]
        if st != Status.Ok:
            Log.Warn("login fail, relogin")
            Server().isLogin = False
            QtOwner().ShowError(Str.GetStr(st))
        else:
            Log.Warn("login success, {}".format(data))
            userName = data.get("userName", "")
            QtOwner().owner.LoginSucBack(userName)
            Server().isLogin = True
            self.parent().parent().parent().parent().close()
            # if load_cookies:
                # QtOwner().owner.settingForm.SetSettingV("ipb_member_id", load_cookies.get("ipb_member_id", ""))
                # QtOwner().owner.settingForm.SetSettingV("ipb_pass_hash", load_cookies.get("ipb_pass_hash", ""))
                # QtOwner().owner.settingForm.SetSettingV("igneous", load_cookies.get("igneous", ""))
            # self.SkipLogin(userName)
        return
