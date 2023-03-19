import os
import sys
import weakref

from PySide6.QtCore import QFile

from component.label.msg_label import MsgLabel
from config.setting import Setting
from tools.log import Log
from tools.singleton import Singleton
from tools.tool import ToolUtil


class QtOwner(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self._owner = None
        self._app = None
        self._localServer = None
        self.backSock = None
        self.closeType = 1   # 1普通， 2关闭弹窗触发， 3任务栏触发
        self.isOfflineModel = False
        self.cacheWord = []

    @property
    def downloadView(self):
        return self.owner.downloadView

    @property
    def settingView(self):
        return self.owner.settingView

    @property
    def settingView2(self):
        return self.owner.settingView2

    @property
    def historyView(self):
        return self.owner.historyView

    def SetSubTitle(self, text):
        return self.owner.setSubTitle(text)
    
    def ShowError(self, msg):
        return MsgLabel.ShowErrorEx(self.owner, str(msg))

    def ShowMsg(self, msg):
        return MsgLabel.ShowMsgEx(self.owner, str(msg))

    def ShowMsgOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowMsg(str(msg))

    def ShowErrOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowError(str(msg))

    def ShowLoading(self):
        self.owner.loadingDialog.show()
        return

    def CloseLoading(self):
        self.owner.loadingDialog.close()
        return

    def SetOwner(self, owner):
        self._owner = weakref.ref(owner)

    def SetApp(self, app):
        self._app = weakref.ref(app)

    @staticmethod
    def SetFont():
        try:
            from tools.log import Log
            from config.setting import Setting
            from PySide6.QtGui import QFont
            f = QFont()
            from tools.langconv import Converter
            if Converter('zh-hans').convert(Setting.FontName.value) == "默认":
                Setting.FontName.InitValue("", "FontName")

            if not Setting.FontName.value and sys.platform == "win32":
                Setting.FontName.InitValue("微软雅黑", "FontName")

            if Converter('zh-hans').convert(str(Setting.FontSize.value)) == "默认":
                Setting.FontSize.InitValue("", "FontSize")

            if Converter('zh-hans').convert(str(Setting.FontStyle.value)) == "默认":
                Setting.FontStyle.InitValue(0, "FontStyle")

            if not Setting.FontName.value and not Setting.FontSize.value and not Setting.FontStyle.value:
                return

            if Setting.FontName.value:
                f = QFont(Setting.FontName.value)

            if Setting.FontSize.value and Setting.FontSize.value != "Defalut":
                f.setPointSize(int(Setting.FontSize.value))

            if Setting.FontStyle.value:
                fontStyleList = [QFont.Light, QFont.Normal, QFont.DemiBold, QFont.Bold, QFont.Black]
                f.setWeight(fontStyleList[Setting.FontStyle.value - 1])

            QtOwner().app.setFont(f)

        except Exception as es:
            Log.Error(es)

    @property
    def app(self):
        return self._app()

    @property
    def localServer(self):
        return self._localServer()

    @property
    def bookInfoView(self):
        return self.owner.bookInfoView

    @property
    def localReadView(self):
        return self.owner.localReadView

    @property
    def favoriteView(self):
        return self.owner.favorityView

    @property
    def indexView(self):
        return self.owner.indexView

    @property
    def searchView(self):
        return self.owner.searchView

    @property
    def owner(self):
        from view.main.main_view import MainView
        assert isinstance(self._owner(), MainView)
        return self._owner()

    def StartReadIndex(self, index):
        self.owner.bookInfoView.StartReadIndex(index)

    def OpenReadView(self, bookId, token, site, name, pageIndex):
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.owner.readView.OpenPage(bookId, token, site, name, pageIndex=pageIndex, isOffline=QtOwner().isOfflineModel)

    def OpenLocalReadView(self, v):
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.owner.readView.OpenLocalPage(v)

    def OpenFavoriteInfo(self, bookId, bookName):
        from view.user.favorite_info_view import FavoriteInfoView
        info = FavoriteInfoView(QtOwner().owner)
        info.OpenFavorite(bookId, bookName)
        info.exec_()
        return

    def OpenBookInfo(self, bookId, token="", site=""):
        arg = {"bookId": bookId, "token": token, "site": site}
        self.owner.SwitchWidget(self.owner.bookInfoView, **arg)

    def OpenLocalBook(self, bookId):
        self.owner.localReadView.OpenLocalBook(bookId)

    def OpenBookInfoExt(self, task):
        arg = {"task": task}
        self.owner.SwitchWidget(self.owner.bookInfoView, **arg)

    def OpenSearch(self, text):
        arg = {"text": text}
        self.owner.SwitchWidget(self.owner.searchView, **arg)

    def OpenSearch2(self, text):
        arg = {"text": text}
        self.owner.searchView2.searchTab.setText(text)
        self.owner.searchView2.setWindowTitle("TAG: {}".format(ToolUtil.GetStrMaxLen(text)))
        self.owner.SwitchWidget(self.owner.searchView2, **arg)

    def OpenComment(self, bookId, site):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"bookId": bookId, "site": site}
        self.owner.SwitchWidget(self.owner.commentView, **arg)

    def OpenWaifu2xTool(self, data):
        # self.owner.subCommentView.SetOpenEvent(commentId, widget)
        arg = {"data": data}
        self.owner.SwitchWidget(self.owner.waifu2xToolView, **arg)

    def CloseReadView(self):
        self.owner.totalStackWidget.setCurrentIndex(0)
        QtOwner().bookInfoView.ReloadHistory.emit()

    def OpenLoginWebView(self, userId, passwd):
        arg = {"userId": userId, "passwd": passwd}
        self.owner.SwitchWidgetAndClear(self.owner.subStackWidget.indexOf(self.owner.loginWebView), **arg)

    def SetDirty(self):
        pass

    def GetFileData(self, fileName):
        f = QFile(fileName)
        f.open(QFile.ReadOnly)
        data = f.readAll()
        f.close()
        return bytes(data)
    # def ShowMsg(self, data):
    #     return self.owner.msgForm.ShowMsg(data)
    #
    # def ShowError(self, data):
    #     return self.owner.msgForm.ShowError(data)

    # def ShowMsgBox(self, type, title, msg):
    #     msg = QMessageBox(type, title, msg)
    #     msg.addButton("Yes", QMessageBox.AcceptRole)
    #     if type == QMessageBox.Question:
    #         msg.addButton("No", QMessageBox.RejectRole)
    #     if config.ThemeText == "flatblack":
    #         msg.setStyleSheet("QWidget{background-color:#2E2F30}")
    #     return msg.exec_()

    @staticmethod
    def SaveCacheWord():
        path = os.path.join(Setting.GetConfigPath(), "cache_word")
        try:
            f = open(path, "w+", encoding="utf-8")
            f.write("\n".join(QtOwner().cacheWord))
            f.close()
        except Exception as es:
            Log.Error(es)

    @staticmethod
    def LoadCacheWord():
        path = os.path.join(Setting.GetConfigPath(), "cache_word")
        try:
            if not os.path.isfile(path):
                return
            f = open(path, "r", encoding="utf-8")
            data = f.read()
            f.close()
            for v in data.split("\n"):
                if v:
                    QtOwner().cacheWord.append(v)
        except Exception as es:
            Log.Error(es)
        finally:
            return QtOwner().cacheWord