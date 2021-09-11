import json

from PySide2 import QtWidgets
from PySide2.QtCore import QUrl
from PySide2.QtGui import QDesktopServices, Qt
from src.qt.com.qtmsg import QtMsgLabel
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, config, Server, Log, Status
from ui.login_proxy import Ui_LoginProxy

# set window icon
from src.util import ToolUtil
from src.qt.user.login_web_proxy import UpdateDns, ClearDns


class QtLoginProxy(QtWidgets.QWidget, Ui_LoginProxy, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_LoginProxy.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        ToolUtil.SetIcon(self)  # set window icon
        self.setWindowModality(Qt.ApplicationModal)
        self.speedTest = []
        self.dohNum = 0
        self.speedPingNum = 0
        self.buttonGroup.setId(self.radioButton_1, 1)
        self.buttonGroup.setId(self.radioButton_2, 2)
        self.LoadSetting()
        self.UpdateServer()

    def show(self):
        self.LoadSetting()
        super(self.__class__, self).show()

    def SetEnabled(self, enabled):
        self.testDoHButton.setEnabled(enabled)
        self.saveButton.setEnabled(enabled)
        self.proxyBox.setEnabled(enabled)
        self.httpLine.setEnabled(enabled)
        self.radioButton_1.setEnabled(enabled)
        self.radioButton_2.setEnabled(enabled)
        self.pushButton.setEnabled(enabled)
        self.comboBox_1.setEnabled(enabled)
        self.comboBox_2.setEnabled(enabled)
        self.comboBox_3.setEnabled(enabled)
        self.comboBox_4.setEnabled(enabled)
        self.comboBox_5.setEnabled(enabled)

    def StartDoh(self):
        self.dohNum = 0
        self.SetEnabled(False)
        for i in range(1, 5+1):
            label = getattr(self, "boxLabel_" + str(i))
            label.setText("")
            combox = getattr(self, "comboBox_" + str(i))
            host = getattr(self, "host_" + str(i))
            combox.clear()
            domain = host.text()
            self.dohNum += 1
            self.AddHttpTask(req.DnsOverHttpsReq(domain), self.DohBack, i)
        return

    def DohBack(self, data, i):
        label = getattr(self, "boxLabel_" + str(i))
        if data["st"] == Status.Ok:
            label.setText("<font color=#7fb80e>Success</font>")
            combox = getattr(self, "comboBox_" + str(i))
            addresss = []
            for info in data["Answer"]:
                addresss.append(info.get("data"))
            combox.addItems(addresss)
        else:
            label.setText("<font color=#d71345>Fail</font>")
        self.dohNum -= 1
        if self.dohNum <= 0:
            self.SetEnabled(True)
            self.UpdateAllDns()
        return

    def SpeedTest(self):
        self.speedPingNum = 0
        self.SetEnabled(False)
        for i in range(1, 5+1):
            label = getattr(self, "boxLabel_" + str(i))
            label.setText("")
            combox = getattr(self, "comboBox_" + str(i))
            host = getattr(self, "host_" + str(i))
            address = combox.currentText()
            domain = host.text()

            self.speedPingNum += 1

            request = req.SpeedTestPingReq(domain)
            request.proxy = {}

            self.UpdateDns(domain, address)
            self.AddHttpTask(lambda x: Server().TestSpeedPing(request, x), self.SpeedTestPingBack, i)
        return

    def SpeedTestPingBack(self, data, i):
        label = getattr(self, "boxLabel_" + str(i))
        data = data["data"]
        if float(data) > 0.0:
            label.setText("<font color=#7fb80e>{}</font>".format(str(int(float(data)*500)) + "ms"))
        else:
            label.setText("<font color=#d71345>{}</font>".format("fail"))
        self.speedPingNum -= 1

        if self.speedPingNum <= 0:
            Server().ClearDns()
            self.UpdateAllDns()
            self.SetEnabled(True)
        return

    def LoadSetting(self):
        config.ProxySelectIndex = QtOwner().owner.settingForm.GetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        httpProxy = QtOwner().owner.settingForm.GetSettingV("Proxy/Http", config.HttpProxy)
        DomainAddress = QtOwner().owner.settingForm.GetSettingV("Proxy/DomainAddress", "{}")
        DomainAddress = json.loads(DomainAddress)
        for k, v in config.DomainDns.items():
            v2 = DomainAddress.get(k)
            if v2:
                config.DomainDns[k] = v2

        self.proxyBox.setChecked(config.IsHttpProxy)
        self.httpLine.setText(httpProxy)
        button = getattr(self, "radioButton_{}".format(config.ProxySelectIndex))
        button.setChecked(True)
        for i in range(1, 5+1):
            label = getattr(self, "host_"+str(i))
            combox = getattr(self, "comboBox_"+str(i))
            address = config.DomainDns.get(label.text())
            combox.setCurrentText(address)
        self.UpdateAllDns()

    def UpdateAllDns(self):
        if config.ProxySelectIndex == 1:
            ClearDns()
            Server().ClearDns()
        for k, v in config.DomainDns.items():
            if k in config.DomainMapping:
                v = config.DomainDns.get(config.DomainMapping.get(k))
            UpdateDns(k, v)
            Server().UpdateDns(k, v)

    def UpdateServer(self):
        self.UpdateAllDns()
        Log.Info("update proxy, setId:{}, dns:{}".format(config.ProxySelectIndex, config.DomainDns))

    def SaveSetting(self):
        config.IsHttpProxy = int(self.proxyBox.isChecked())
        httpProxy = self.httpLine.text()
        config.ProxySelectIndex = self.buttonGroup.checkedId()

        QtOwner().owner.settingForm.SetSettingV("Proxy/ProxySelectIndex", config.ProxySelectIndex)
        QtOwner().owner.settingForm.SetSettingV("Proxy/Http", httpProxy)
        QtOwner().owner.settingForm.SetSettingV("Proxy/IsHttp", config.IsHttpProxy)
        QtOwner().owner.settingForm.SetSettingV("Proxy/DomainAddress", json.dumps(config.DomainDns))

        self.UpdateServer()
        QtMsgLabel().ShowMsgEx(self, self.tr("保存成功"))
        self.close()
        return

    def OpenUrl(self):
        QDesktopServices.openUrl(QUrl(config.ProxyUrl))