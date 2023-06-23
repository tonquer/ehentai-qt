import urllib
from copy import deepcopy

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from config import config
from config.setting import Setting
from interface.ui_host import Ui_LoginHostWidget
from qt_owner import QtOwner
from server import req, Log
from server.server import Server
from task.qt_task import QtTaskBase
from tools.str import Str
from urllib3.util.ssl_ import is_ipaddress


class LoginHostWidget(QtWidgets.QWidget, Ui_LoginHostWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginHostWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.LoadConfig()

    def LoadConfig(self):
        config.Hosts = {}
        for v in Setting.OwnerHosts.value.split("\n"):
            try:
                v = v.strip("\r")
                if not v:
                    continue
                if "：" in v:
                    data= v.split("：")
                else:
                    data= v.split(":")
                if len(data) < 2:
                    Log.Warn("pass host error, {}".format(v))
                else:
                    domain = data[0]
                    ip = data[1]
                    if is_ipaddress(ip):
                        config.Hosts[domain] = ip
                    else:
                        Log.Warn("pass host error2, {}".format(v))
            except Exception as es:
                Log.Error(es)
        Log.Info("load hosts data, {}".format(config.Hosts))

    def Init(self):
        self.LoadConfig()
        self.plainTextEdit.setPlainText(Setting.OwnerHosts.value)
        pass

    def ClickButton(self):
        Setting.OwnerHosts.SetValue(self.plainTextEdit.toPlainText())
        self.LoadConfig()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        pass
