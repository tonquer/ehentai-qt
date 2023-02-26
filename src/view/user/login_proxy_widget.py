from copy import deepcopy

from PySide6 import QtWidgets
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from config import config
from config.setting import Setting
from interface.ui_login_proxy_widget import Ui_LoginProxyWidget
from qt_owner import QtOwner
from server import req, Log
from server.server import Server
from task.qt_task import QtTaskBase
from tools.str import Str


class LoginProxyWidget(QtWidgets.QWidget, Ui_LoginProxyWidget, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginProxyWidget.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.speedTest = []
        self.speedIndex = 0
        self.speedPingNum = 0
        self.pingBackNumCnt = {}
        self.pingBackNumDict = {}
        self.needBackNum = 0
        self.eGroup.setId(self.radio_e_1, 1)
        self.eGroup.setId(self.radio_e_2, 2)
        self.eGroup.setId(self.radio_e_3, 3)

        self.exGroup.setId(self.radio_ex_1, 1)
        self.exGroup.setId(self.radio_ex_2, 2)
        self.exGroup.setId(self.radio_ex_3, 3)

        self.apiGroup.setId(self.radio_api_1, 1)
        self.apiGroup.setId(self.radio_api_2, 2)
        self.apiGroup.setId(self.radio_api_3, 3)

        self.ehGroup.setId(self.radio_eh_1, 1)
        self.ehGroup.setId(self.radio_eh_2, 2)
        self.ehGroup.setId(self.radio_eh_3, 3)

        self.LoadSetting()
        self.UpdateServer()

        self.radioProxyGroup.setId(self.proxy_0, 0)
        self.radioProxyGroup.setId(self.proxy_1, 1)
        self.radioProxyGroup.setId(self.proxy_2, 2)
        self.radioProxyGroup.setId(self.proxy_3, 3)
        self.maxNum = 3

    def Init(self):
        self.LoadSetting()

    def ClickButton(self):
        self.SaveSetting()

    def SetEnabled(self, enabled):
        self.testSpeedButton.setEnabled(enabled)
        self.proxy_0.setEnabled(enabled)
        self.proxy_1.setEnabled(enabled)
        self.proxy_2.setEnabled(enabled)
        self.proxy_3.setEnabled(enabled)
        self.httpLine.setEnabled(enabled)
        self.sockEdit.setEnabled(enabled)
        self.radio_api_1.setEnabled(enabled)
        self.radio_api_2.setEnabled(enabled)
        self.radio_api_3.setEnabled(enabled)
        self.radio_e_1.setEnabled(enabled)
        self.radio_e_2.setEnabled(enabled)
        self.radio_e_3.setEnabled(enabled)
        self.radio_ex_1.setEnabled(enabled)
        self.radio_ex_2.setEnabled(enabled)
        self.radio_ex_3.setEnabled(enabled)

        self.radio_eh_1.setEnabled(enabled)
        self.radio_eh_2.setEnabled(enabled)
        self.radio_eh_3.setEnabled(enabled)

        self.httpsBox.setEnabled(enabled)
        self.ipDirect.setEnabled(enabled)

    def SpeedTest(self):
        self.speedIndex = 0
        # self.speedPingNum = 0
        self.speedTest = []

        for i in range(1, self.maxNum+1):
            label = getattr(self, "label_e_" + str(i))
            label.setText("")
            label = getattr(self, "label_ex_" + str(i))
            label.setText("")
            label = getattr(self, "label_api_" + str(i))
            label.setText("")
            label = getattr(self, "label_eh_" + str(i))
            label.setText("")
            self.speedTest.append(("e", "", False, False, i))
            self.speedTest.append(("ex", "", False, False, i))
            self.speedTest.append(("api", "", False, False, i))
            self.speedTest.append(("eh", "", False, False, i))

        self.SetEnabled(False)
        self.needBackNum = 0
        self.speedPingNum = 0
        self.StartSpeedPing()

    def StartSpeedPing(self):
        if len(self.speedTest) <= self.speedPingNum:
            self.UpdateServer()
            self.SetEnabled(True)
            return
        # for v in self.speedTest:
        addressName, _, isHttpProxy, _, i = self.speedTest[self.speedPingNum]
        httpProxy = self.httpLine.text()
        isHttpProxy = True

        domain = getattr(self, "label_"+str(addressName)).text()
        ip = getattr(self, "radio_{}_{}".format(addressName, i)).text()

        request = req.SpeedTestPingReq(ip, domain)
        request.isUseHttps = self.httpsBox.isChecked()

        if self.radioProxyGroup.checkedId() == 1:
            request.proxy = {"http": httpProxy, "https": httpProxy}
        elif self.radioProxyGroup.checkedId() == 3:
            request.proxy = ""
        else:
            request.proxy = {"http": None, "https": None}

        # if isProxyUrl:
        #     if "user-agent" in request.headers:
        #         request.headers.pop("user-agent")
        #     request.proxyUrl = isProxyUrl[0]
        # else:
        #     request.proxyUrl = ""

        if self.radioProxyGroup.checkedId() == 2:
            self.SetSock5Proxy(True)
        else:
            self.SetSock5Proxy(False)

        self.pingBackNumCnt[addressName] = 0
        self.pingBackNumDict[addressName] = [0, 0, 0]
        # request1 = deepcopy(request)
        # request2 = deepcopy(request)
        self.AddHttpTask(lambda x: Server().TestSpeedPing(request, x), self.SpeedTestPingBack, (addressName, i, 0))
        # self.AddHttpTask(lambda x: Server().TestSpeedPing(request1, x), self.SpeedTestPingBack, (addressName, i, 1))
        # self.AddHttpTask(lambda x: Server().TestSpeedPing(request2, x), self.SpeedTestPingBack, (addressName, i, 2))
        self.needBackNum += 1
        return

    def SpeedTestPingBack(self, raw, v):
        addressName, i, backNum = v
        data = raw["data"]
        st = raw["st"]
        key = "{}_{}".format(addressName, i)
        label = getattr(self, "label_{}".format(key))
        if float(data) > 0.0:
            self.pingBackNumDict[addressName][backNum] = int(float(data))
            label.setText("<font color=#7fb80e>{}</font>".format(str(int(float(data))) + "ms"))
        else:
            self.pingBackNumDict[addressName][backNum] = str(st)
            label.setText("<font color=#d71345>{}</font>".format(Str.GetStr(st)))
        self.pingBackNumCnt[addressName] += 1

        if self.pingBackNumCnt[addressName] >= 1:
            self.speedPingNum += 1
            self.StartSpeedPing()
            return

    def LoadSetting(self):
        # config.PreferCDNIP = QtOwner().settingView.GetSettingV("Proxy/PreferCDNIP", config.PreferCDNIP)
        # config.ProxySelectIndex = QtOwner().settingView.GetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        # config.IsUseHttps = QtOwner().settingView.GetSettingV("Proxy/IsUseHttps", config.IsUseHttps)
        # httpProxy = QtOwner().settingView.GetSettingV("Proxy/Http", config.HttpProxy)

        self.httpsBox.setChecked(Setting.IsUseHttps.value)
        self.ipDirect.setChecked(Setting.IpDirect.value)

        self.httpLine.setText(Setting.HttpProxy.value)
        self.sockEdit.setText(Setting.Sock5Proxy.value)

        button = getattr(self, "proxy_{}".format(int(Setting.IsHttpProxy.value)))
        button.setChecked(True)
        button = getattr(self, "radio_e_{}".format(Setting.ProxyEIndex.value))
        button.setChecked(True)
        button = getattr(self, "radio_ex_{}".format(Setting.ProxyExIndex.value))
        button.setChecked(True)
        button = getattr(self, "radio_api_{}".format(Setting.ProxyApiIndex.value))
        button.setChecked(True)
        button = getattr(self, "radio_eh_{}".format(Setting.ProxyEhIndex.value))
        button.setChecked(True)

    def UpdateServer(self):
        for adressName, index in [("e", Setting.ProxyEIndex.value), ("ex", Setting.ProxyExIndex.value), ("api", Setting.ProxyApiIndex.value), ("eh", Setting.ProxyEhIndex.value)]:
            domain = getattr(self, "label_{}".format(adressName)).text()
            ip =  getattr(self, "radio_{}_{}".format(adressName, index)).text()
            Server().UpdateDns(domain, ip)
            QtOwner().settingView.SetSock5Proxy()
            Log.Info("update proxy, domain: {}, ip: {}".format(domain, ip))

    def SaveSetting(self):
        Setting.IsHttpProxy.SetValue(int(self.radioProxyGroup.checkedId()))
        Setting.Sock5Proxy.SetValue(self.sockEdit.text())
        Setting.HttpProxy.SetValue(self.httpLine.text())
        Setting.IsUseHttps.SetValue(int(self.httpsBox.isChecked()))
        Setting.IpDirect.SetValue(int(self.ipDirect.isChecked()))

        Setting.ProxyEIndex.SetValue(self.eGroup.checkedId())
        Setting.ProxyExIndex.SetValue(self.exGroup.checkedId())
        Setting.ProxyApiIndex.SetValue(self.apiGroup.checkedId())
        Setting.ProxyEhIndex.SetValue(self.ehGroup.checkedId())
        # QtOwner().settingView.SetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        # QtOwner().settingView.SetSettingV("Proxy/PreferCDNIP", config.PreferCDNIP)
        # QtOwner().settingView.SetSettingV("Proxy/Http", httpProxy)
        # QtOwner().settingView.SetSettingV("Proxy/IsHttp", config.IsHttpProxy)
        # QtOwner().settingView.SetSettingV("Proxy/IsUseHttps", config.IsUseHttps)

        self.UpdateServer()
        QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
        return

    def OpenUrl(self):
        QtOwner().owner.helpView.OpenProxyUrl()

    def SetSock5Proxy(self, isProxy):
        import socket
        import socks
        if not QtOwner().backSock:
            QtOwner().backSock = socket.socket
        if isProxy:
            data = self.sockEdit.text().replace("http://", "").replace("https://", "").replace("sock5://", "")
            data = data.split(":")
            if len(data) == 2:
                host = data[0]
                port = data[1]
                socks.set_default_proxy(socks.SOCKS5, host, int(port))
                socket.socket = socks.socksocket
        else:
            socks.set_default_proxy()
            socket.socket = QtOwner().backSock