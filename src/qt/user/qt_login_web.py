import re
import sys

from PySide2 import QtCore, QtNetwork, QtWidgets
from PySide2.QtCore import QUrl, QByteArray
from PySide2.QtWebEngineCore import QWebEngineUrlRequestInterceptor, QWebEngineUrlSchemeHandler, QWebEngineHttpRequest
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage

from conf import config
from src.qt.qt_main import QtOwner
from src.util import ToolUtil


class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(CustomWebEnginePage, self).__init__(*args, **kwargs)

    def certificateError(self, certificateError):
        return True


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    # Everything requested from static.foo.bar goes to static://
    # //static.foo.bar/1/2/4.jpeg >> static://1/2/4.jpeg
    def interceptRequest(self, info):
        print("interceptRequest")
        url = info.requestUrl()
        host = url.host()
        # info.setHttpHeader(b"host", b"forums.e-hentai.org")
        # print(url.toString())
        # if 'forums.e-hentai.org' == host:
        #     url = QUrl(url.toString().replace(host, "104.20.134.21"))
        #     # url = QUrl("https://baidu.com")
        #     # url.setScheme(MyWebEngineUrlScheme.scheme.decode())
        #     # url.setHost('forums.e-hentai.org')
        #     print('Intercepting and redirecting to: %s' % url)
        #     # info.setHttpHeader(b"host", host.encode("utf-8"))
        #     info.requestMethod()
        #     info.redirect(url)


class QtLoginWeb(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(QtLoginWeb, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        self.interceptor = WebEngineUrlRequestInterceptor()
        self.setPage(CustomWebEnginePage(self))
        # self.page().profile().setRequestInterceptor(self.interceptor)
        self.page().profile().clearHttpCache()
        self.page().profile().cookieStore().deleteAllCookies()
        self.page().profile().cookieStore().cookieAdded.connect(self.OnCookieAdd)
        self.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")
        self.page().profile().setHttpAcceptLanguage("zh-CN,zh;q=0.9")
        self.loadFinished.connect(self.LoadFinished)
        self.cookies = {}
        self.userName = ""
        self.passWord = ""

    def LoadFinished(self):
        jsStr = "\
        document.getElementsByName('UserName')[0].value = '{}';\
        document.getElementsByName('PassWord')[0].value = '{}';\
        ".format(self.userName, self.passWord)
        self.page().runJavaScript(jsStr)

    def OpenUrl(self, userName, passWord):
        if config.HttpProxy and config.ProxySelectIndex == 1:
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
        elif config.ProxySelectIndex == 2:
            proxy = QtNetwork.QNetworkProxy()
            proxy.setType(QtNetwork.QNetworkProxy.HttpProxy)
            proxy.setHostName("127.0.0.1")
            proxy.setPort(config.LocalProxyPort)
            QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

        self.userName = userName
        self.passWord = passWord
        # self.page().load(QtCore.QUrl("https://baidu.com"))
        self.page().load(QtCore.QUrl("https://forums.e-hentai.org/index.php?act=Login&CODE=00"))
        # r = QWebEngineHttpRequest(QtCore.QUrl("https://104.20.134.21/index.php?act=Login&CODE=00"))
        # r.setHeader(b"host", b"forums.e-hentai.org")
        # print(r.header(b"host"))
        # self.page().load(r)
        # self.page().load(QtCore.QUrl("https://www.baidu.com/"))
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