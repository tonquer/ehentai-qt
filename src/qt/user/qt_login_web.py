import sys

from PySide2 import QtCore, QtNetwork, QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from conf import config
from src.qt.qt_main import QtOwner


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(CustomWebEnginePage, self).__init__(*args, **kwargs)

    def certificateError(self, certificateError):
        return True


class QtLoginWeb(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(QtLoginWeb, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        self.setPage(CustomWebEnginePage(self))
        self.page().profile().clearHttpCache()
        self.page().profile().cookieStore().deleteAllCookies()
        self.page().profile().cookieStore().cookieAdded.connect(self.OnCookieAdd)
        self.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
        # self.loadFinished.connect(self.LoadFinished)
        self.cookies = {}
        self.userName = ""
        self.passWord = ""

    def Init(self):
        if config.IsHttpProxy and config.HttpProxy:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            url = config.HttpProxy
            url = url.replace("http://", "")
            url = url.replace("https://", "")
            data = url.split(":")
            if len(data) >= 2:
                proxy.setHostName(data[0])
                proxy.setPort(int(data[1]))
                QtNetwork.QNetworkProxy.setApplicationProxy(proxy)
        elif config.IsOpenDoh and config.LocalProxyPort:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            proxy.setHostName("127.0.0.1")
            proxy.setPort(config.LocalProxyPort)
            QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

    def LoadFinished(self):
        jsStr = "\
        document.getElementsByName('UserName')[0].value = '{}';\
        document.getElementsByName('PassWord')[0].value = '{}';\
        ".format(self.userName, self.passWord)
        self.page().runJavaScript(jsStr)

    def OpenUrl(self, userName, passWord):
        if config.IsHttpProxy and config.HttpProxy:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            url = config.HttpProxy
            url = url.replace("http://", "")
            url = url.replace("https://", "")
            data = url.split(":")
            if len(data) >= 2:
                proxy.setHostName(data[0])
                proxy.setPort(int(data[1]))
                QtNetwork.QNetworkProxy.setApplicationProxy(proxy)
        elif config.IsOpenDoh and config.LocalProxyPort:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            proxy.setHostName("127.0.0.1")
            proxy.setPort(config.LocalProxyPort)
            QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

        if config.Language == "English":
            self.page().profile().setHttpAcceptLanguage("en-us,en;q=0.9")
        elif config.Language == "Chinese-Simplified":
            self.page().profile().setHttpAcceptLanguage("zh-CN,zh;q=0.9")
        else:
            self.page().profile().setHttpAcceptLanguage("zh-HK,zh;q=0.9")

        self.userName = userName
        self.passWord = passWord
        # self.page().load(QtCore.QUrl("https://baidu.com"))
        self.page().load(QtCore.QUrl("https://forums.e-hentai.org/index.php?act=Login&CODE=00"))
        return

    def OnCookieAdd(self, cookie):  # 处理cookie添加的事件
        QtOwner().owner.loginForm.SaveCookie(cookie)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    a = QtLoginWeb()
    a.resize(100, 100)
    a.show()
    a.OpenUrl("", "")
    sts = app.exec_()
    sys.exit(sts)  # 运行程序