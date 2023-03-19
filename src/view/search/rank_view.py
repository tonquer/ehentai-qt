import json
from functools import partial

from PySide6 import QtWidgets

from config import config
from interface.ui_rank import Ui_Rank
from qt_owner import QtOwner
from server import req, Log, Status, ToolUtil
from task.qt_task import QtTaskBase
from tools.str import Str


class RankView(QtWidgets.QWidget, Ui_Rank, QtTaskBase):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_Rank.__init__(self)
        QtTaskBase.__init__(self)

        self.isInitKind = False
        self.setupUi(self)

        self.isInit = False
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.currentChanged.connect(self.SwitchPage)
        self.indexDict = {
            0: "15",
            1: "13",
            2: "12",
            3: "11"
        }
        self.indexToList = {
            0: self.dayBookList,
            1: self.monthBookList,
            2: self.yearBookList,
            3: self.allBookList
        }
        self.dayBookList.LoadCallBack = partial(self.LoadNextPage, 0)
        self.monthBookList.LoadCallBack = partial(self.LoadNextPage, 1)
        self.yearBookList.LoadCallBack = partial(self.LoadNextPage, 2)
        self.allBookList.LoadCallBack = partial(self.LoadNextPage, 3)

    def SwitchCurrent(self, **kwargs):
        refresh = kwargs.get("refresh")
        self.isInit = True
        if refresh:
            self.dayBookList.clear()
            self.monthBookList.clear()
            self.yearBookList.clear()
            self.allBookList.clear()
            self.Init()
        pass

    def SwitchPage(self, index):
        if not self.isInit:
            return
        bookList = self.indexToList.get(index)
        if bookList.count() > 0:
            return
        QtOwner().ShowLoading()
        bookList.UpdatePage(1, 200)
        self.AddHttpTask(req.GetRankInfoReq(self.indexDict.get(index)), self.InitBack, backParam=(index, 1))
        return

    def LoadNextPage(self, index):
        bookList = self.indexToList.get(index)
        if bookList.page >= bookList.pages:
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetRankInfoReq(self.indexDict.get(index)), self.InitBack, backParam=(index, bookList.page+1))
        return

    def Init(self):
        if self.tabWidget.currentIndex() == 0:
            self.SwitchPage(0)
        else:
            self.tabWidget.setCurrentIndex(0)

    def InitBack(self, raw, backParam):
        index, page = backParam
        QtOwner().CloseLoading()
        bookList = self.indexToList.get(index)
        bookList.UpdatePage(page, 200)
        bookList.UpdateState()
        try:
            st = raw["st"]
            if st == Status.Ok:
                data = raw
                for info in data.get("bookList"):
                    _id = info.baseInfo.id
                    title = info.baseInfo.title
                    url = info.baseInfo.imgUrl
                    token = info.baseInfo.token
                    category = ToolUtil.GetCategoryName(info.baseInfo.category)
                    path = "{}/{}_{}_cover".format(config.CurSite, _id, info.baseInfo.token)
                    bookList.AddBookItem(_id, title, Str.GetStr(Str.Classify) + ":" + category, url, path, "", token=token)
            else:
                QtOwner().ShowError(Str.GetStr(st))
        except Exception as es:
            Log.Error(es)

