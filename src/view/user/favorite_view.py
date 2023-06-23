import json

from PySide6 import QtWidgets

from config import config
from interface.ui_favority import Ui_Favority
from qt_owner import QtOwner
from server import req, Log
from task.qt_task import QtTaskBase
from tools.status import Status
from tools.str import Str
from tools.tool import ToolUtil


class FavoriteView(QtWidgets.QWidget, Ui_Favority, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Favority.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookList.isDelMenu = True
        self.bookList.LoadCallBack = self.LoadNextPage
        self.bookList.DelCallBack = self.DelCallBack
        self.resetCnt = 5

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        if not config.IsLogin:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        if refresh:
            self.bookList.clear()
            self.GetFavorites()

    def GetFavorites(self, nextId=""):
        curIndex = self.comboBox.currentIndex()
        if curIndex <= 0:
            favcat = ""
        else:
            favcat = str(curIndex-1)
        QtOwner().ShowLoading()
        if nextId:
            page = self.bookList.page+1
        else:
            page = 1
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetFavoritesReq(favcat, nextId), self.GetFavoritesBack, page)

    def GetFavoritesBack(self, data, page):
        QtOwner().CloseLoading()
        self.bookList.UpdateState()
        st = data['st']
        if st == Status.Ok:
            bookList = data["bookList"]
            nextId = data["nextId"]
            favoriteList = data["favoriteList"]
            if nextId:
                self.bookList.UpdatePage(page, page+1)
                self.bookList.nextId = nextId
                self.jumpButton.setEnabled(True)
            else:
                self.bookList.UpdatePage(page, page)
                self.jumpButton.setEnabled(False)
            allNum = sum(favoriteList.values())
            self.comboBox.setItemText(0, Str.GetStr(Str.All)+" ({})".format(str(allNum)))
            for k, v in favoriteList.items():
                self.comboBox.setItemText(k+1, Str.GetStr(Str.Favorite)+" {}({})".format(str(k), str(v)))
            for info in bookList:
                _id = info.baseInfo.id
                title = info.baseInfo.title
                url = info.baseInfo.imgUrl
                token = info.baseInfo.token
                category = ToolUtil.GetCategoryName(info.baseInfo.category)
                path = "{}/{}_{}_cover".format(config.CurSite, _id, info.baseInfo.token)
                self.bookList.AddBookItem(_id, title, Str.GetStr(Str.Classify)+ ":" +category, url, path, "", token=token)
        else:
            QtOwner().ShowMsg(Str.GetStr(st))
        pass

    def JumpPage(self):
        if self.bookList.page >= self.bookList.pages:
            return
        if not self.bookList.nextId:
            return
        self.bookList.clear()
        self.bookList.nextId = ""
        self.GetFavorites(self.bookList.nextId)
        return

    def JumpFavcat(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.clear()
        self.bookList.nextId = ""
        self.GetFavorites()
        return

    def LoadNextPage(self):
        if not self.bookList.nextId:
            return
        self.GetFavorites(self.bookList.nextId)
        return

    def DelCallBack(self):
        selected = self.bookList.selectedItems()
        if not selected:
            return

        data = ''
        QtOwner().owner.loadingForm.show()
        for item in selected:
            widget = self.bookList.itemWidget(item)
            bookId = widget.id
            self.AddHttpTask(req.DelFavoritesReq(bookId), self.DeleteBack)
        return

    def DeleteBack(self, data):
        QtOwner().owner.loadingForm.close()
        if data["st"] == Status.Ok:
            QtOwner().ShowMsg(Str.GetStr(Str.DeleteSuc))
            self.bookList.clear()
            self.GetFavorites()