import sys

from PySide2 import QtCore, QtNetwork, QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from config import config
from config.setting import Setting
from qt_owner import QtOwner


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(CustomWebEnginePage, self).__init__(*args, **kwargs)

    def certificateError(self, certificateError):
        return True


class LoginWebView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(LoginWebView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        self.setPage(CustomWebEnginePage(self))
        self.page().profile().clearHttpCache()
        self.page().profile().cookieStore().deleteAllCookies()
        self.page().profile().cookieStore().cookieAdded.connect(self.OnCookieAdd)
        self.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
        self.loadFinished.connect(self.LoadFinished)
        self.cookies = {}
        self.userName = ""
        self.passWord = ""

        self.cookieList = ["ipb_member_id", "ipb_pass_hash"]
        self.cookie = {}
        self.isLogin = False

    def SwitchCurrent(self, **kwargs):
        self.Init()
        self.OpenUrl()
        return

    def Init(self):
        if Setting.IsHttpProxy.value and Setting.HttpProxy.value:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            url = Setting.HttpProxy.value
            url = url.replace("http://", "")
            url = url.replace("https://", "")
            data = url.split(":")
            if len(data) >= 2:
                proxy.setHostName(data[0])
                proxy.setPort(int(data[1]))
                QtNetwork.QNetworkProxy.setApplicationProxy(proxy)
        elif Setting.IsOpenDoh.value and config.LocalProxyPort:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            proxy.setHostName("127.0.0.1")
            proxy.setPort(config.LocalProxyPort)
            QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

    def LoadFinished(self):
        QtOwner().CloseLoading()
        jsStr = "\
        document.getElementsByName('UserName')[0].value = '{}';\
        document.getElementsByName('PassWord')[0].value = '{}';\
        ".format(self.userName, self.passWord)
        self.page().runJavaScript(jsStr)

    def OpenUrl(self):
        QtOwner().ShowLoading()
        self.isLogin = False
        self.cookie.clear()
        if Setting.IsHttpProxy.value and Setting.HttpProxy.value:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            url = Setting.HttpProxy.value
            url = url.replace("http://", "")
            url = url.replace("https://", "")
            data = url.split(":")
            if len(data) >= 2:
                proxy.setHostName(data[0])
                proxy.setPort(int(data[1]))
                QtNetwork.QNetworkProxy.setApplicationProxy(proxy)
        elif Setting.IsOpenDoh.value and config.LocalProxyPort:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            proxy.setHostName("127.0.0.1")
            proxy.setPort(config.LocalProxyPort)
            QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

        if Setting.Language.autoValue == 3:
            self.page().profile().setHttpAcceptLanguage("en-us,en;q=0.9")
        elif Setting.Language.autoValue == 1:
            self.page().profile().setHttpAcceptLanguage("zh-CN,zh;q=0.9")
        else:
            self.page().profile().setHttpAcceptLanguage("zh-HK,zh;q=0.9")

        # self.page().load(QtCore.QUrl("https://baidu.com"))
        self.page().load(QtCore.QUrl("https://forums.e-hentai.org/index.php?act=Login&CODE=00"))
        return

    def OnCookieAdd(self, cookie):  # 处理cookie添加的事件
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
                self.isLogin = True
                Setting.IpbMemberId.SetValue(self.cookie.get("ipb_member_id"))
                Setting.IpbPassHash.SetValue(self.cookie.get("ipb_pass_hash"))
                QtOwner().owner.OpenLoginView()
        return
