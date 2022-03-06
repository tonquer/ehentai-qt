import json

from PySide2.QtWidgets import QWidget, QAbstractItemView

from config import config
from config.setting import Setting
from interface.ui_search import Ui_Search
from qt_owner import QtOwner
from server import req, Log, Status
from task.qt_task import QtTaskBase
from tools.str import Str
from tools.tool import ToolUtil


class SearchView(QWidget, Ui_Search, QtTaskBase):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        Ui_Search.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.isInit = False
        self.categories = ""
        self.text = ""
        self.bookList.LoadCallBack = self.LoadNextPage

        self.searchButton.clicked.connect(self.lineEdit.Search)
        self.tagWidget.itemClicked.connect(self.ClickKeywordListItem)
        self.tagWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    def retranslateUi(self, search):
        Ui_Search.retranslateUi(self, search)
        search.tagWidget.clear()
        for key, value in ToolUtil.Category.items():
            if Setting.Language.autoValue == 3:
                search.tagWidget.AddItem(key)
            else:
                search.tagWidget.AddItem(value)

    def ClickKeywordListItem(self, item):
        data = item.text()
        self.categories = data
        self.lineEdit.setText("")
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(self.categories)
        self.bookList.clear()
        self.SendSearchCategories(1)

    def InitWord(self):
        pass
        # self.AddSqlTask("book", "", SqlServer.TaskTypeSelectWord, self.InitWordBack)
        return

    def InitWordBack(self, data):
        if not data:
            return
        self.lineEdit.words = data

    def SwitchCurrent(self, **kwargs):
        text = kwargs.get("text")
        refresh = kwargs.get("refresh")
        self.categories = kwargs.get("categories", "")

        if self.categories:
            self.lineEdit.setText("")
            self.lineEdit.setPlaceholderText(self.categories)
            self.bookList.clear()
            self.SendSearchCategories(1)
        elif text is not None:
            self.text = text
            self.lineEdit.setText(self.text)
            self.bookList.clear()
            self.SendSearch(1)
        elif refresh:
            self.text = ""
            self.lineEdit.setText(self.text)
            self.bookList.clear()
            self.SendSearch(1)
        pass

    def SendSearchCategories(self, page):
        for k, v in ToolUtil.Category.items():
            if v == self.categories or k == self.categories:
                QtOwner().ShowLoading()
                self.AddHttpTask(req.GetCategoryInfoReq(page, k), self.SendSearchBack, page)

                break

    def SendSearchBack(self, data, page):
        QtOwner().CloseLoading()
        try:
            self.bookList.UpdateState()
            st = data.get("st")
            if st == Status.Ok:
                pages = data.get("maxPages")
                self.bookList.UpdatePage(page, pages)
                self.spinBox.setMaximum(pages)
                pageText = Str.GetStr(Str.Page) + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for info in data.get("bookList"):
                    _id = info.baseInfo.id
                    title = info.baseInfo.title
                    url = info.baseInfo.imgUrl
                    category = ToolUtil.GetCategoryName(info.baseInfo.category)
                    path = "{}/{}_{}_cover".format(config.CurSite, _id, info.baseInfo.token)
                    self.bookList.AddBookItem(_id, title, Str.GetStr(Str.Classify) + ":" + category, url, path, "")
                # self.CheckCategoryShowItem()
            else:
                QtOwner().ShowError(Str.GetStr(st))

        except Exception as es:
            Log.Error(es)
        pass

    def SendSearch(self, page):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.GetIndexInfoReq(page, self.text), self.SendSearchBack, page)

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        if not self.categories:
            self.SendSearch(page)
        else:
            self.SendSearchCategories(page)
        return

    def LoadNextPage(self):
        if not self.categories:
            self.SendSearch(self.bookList.page + 1)
        else:
            self.SendSearchCategories(self.bookList.page + 1)
        return
