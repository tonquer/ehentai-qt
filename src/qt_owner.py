import weakref

from PySide2.QtCore import QFile

from component.label.msg_label import MsgLabel
from tools.singleton import Singleton


class QtOwner(Singleton):
    def __init__(self):
        Singleton.__init__(self)
        self._owner = None
        self._app = None
        self.backSock = None

    @property
    def downloadView(self):
        return self.owner.downloadView

    @property
    def settingView(self):
        return self.owner.settingView

    def SetSubTitle(self, text):
        return self.owner.setSubTitle(text)
    
    def ShowError(self, msg):
        return MsgLabel.ShowErrorEx(self.owner, msg)

    def ShowMsg(self, msg):
        return MsgLabel.ShowMsgEx(self.owner, msg)

    def ShowMsgOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowMsg(msg)

    def ShowErrOne(self, msg):
        if not hasattr(self.owner, "msgLabel"):
            return
        return self.owner.msgLabel.ShowError(msg)

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

    @property
    def app(self):
        return self._app()

    @property
    def owner(self):
        from view.main.main_view import MainView
        assert isinstance(self._owner(), MainView)
        return self._owner()

    def OpenReadView(self, bookId, name, pageIndex):
        self.owner.totalStackWidget.setCurrentIndex(1)
        self.owner.readView.OpenPage(bookId, name, pageIndex=pageIndex)

    def OpenFavoriteInfo(self, bookId, bookName):
        from view.user.favorite_info_view import FavoriteInfoView
        info = FavoriteInfoView(QtOwner().owner)
        info.OpenFavorite(bookId, bookName)
        info.exec_()
        return

    def OpenBookInfo(self, bookId, token="", site=""):
        arg = {"bookId": bookId, "token": token, "site": site}
        self.owner.SwitchWidget(self.owner.bookInfoView, **arg)

    def OpenSearch(self, text):
        arg = {"text": text}
        self.owner.SwitchWidget(self.owner.searchView, **arg)

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