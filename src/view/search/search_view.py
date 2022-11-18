import json
from functools import partial

from PySide2.QtWidgets import QWidget, QAbstractItemView, QVBoxLayout, QLabel, QPushButton

from component.layout.flow_layout import FlowLayout
from component.scroll_area.smooth_scroll_area import SmoothScrollArea
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
        self.tagWidget.clicked.connect(self.ClickKeywordListItem)
        self.tagWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.jumpPage.clicked.connect(self.JumpPage)

    def retranslateUi(self, search):
        Ui_Search.retranslateUi(self, search)
        search.tagWidget.clear()
        for key, value in ToolUtil.Category.items():
            if Setting.Language.autoValue == 3:
                search.tagWidget.AddItem(key)
            else:
                search.tagWidget.AddItem(value)

    def ClickKeywordListItem(self, modelIndex):
        index = modelIndex.row()
        item = self.tagWidget.item(index)

        if not item:
            return
        widget = self.tagWidget.itemWidget(item)
        data = widget.text()
        self.categories = data
        self.lineEdit.setText("")
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(self.categories)
        self.bookList.clear()
        self.bookList.UpdatePage(1, 1)
        self.bookList.nextId = ""
        self.SendSearchCategories()

    def InitWord(self):
        self.lineEdit.InitCacheWords()
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
        if self.CheckDirechLink(text):
            return

        if self.categories:
            self.lineEdit.setText("")
            self.lineEdit.setPlaceholderText(self.categories)
            self.bookList.clear()
            self.bookList.UpdatePage(1, 1)
            self.bookList.nextId = ""
            self.SendSearchCategories()
        elif text is not None:
            self.text = text
            self.lineEdit.setText(self.text)
            self.bookList.clear()
            self.bookList.UpdatePage(1, 1)
            self.bookList.nextId = ""
            self.SendSearch()
            self.lineEdit.AddCacheWord(self.text)
        elif refresh:
            self.text = ""
            self.lineEdit.setText(self.text)
            self.bookList.nextId = ""
            self.bookList.clear()
            self.bookList.UpdatePage(1,  1)
            self.SendSearch()
        pass

    def SendSearchCategories(self, nextId=""):
        for k, v in ToolUtil.Category.items():
            if v == self.categories or k == self.categories:
                QtOwner().ShowLoading()
                QtOwner().ShowLoading()
                if nextId:
                    page = self.bookList.page+1
                else:
                    page = 1
                self.AddHttpTask(req.GetCategoryInfoReq(nextId, k), self.SendSearchBack, page)

                break

    def SendSearchBack(self, data, page):
        QtOwner().CloseLoading()
        try:
            self.bookList.UpdateState()
            st = data.get("st")
            if st == Status.Ok:
                nextId = data.get("nextId")
                if nextId:
                    self.bookList.UpdatePage(page, page + 1)
                    self.bookList.nextId = nextId
                    self.jumpPage.setEnabled(True)
                else:
                    self.bookList.UpdatePage(page, page)
                    self.jumpPage.setEnabled(False)
                pageText = Str.GetStr(Str.Page) + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for info in data.get("bookList"):
                    _id = info.baseInfo.id
                    title = info.baseInfo.title
                    url = info.baseInfo.imgUrl
                    token = info.baseInfo.token
                    category = ToolUtil.GetCategoryName(info.baseInfo.category)
                    path = "{}/{}_{}_cover".format(config.CurSite, _id, info.baseInfo.token)
                    self.bookList.AddBookItem(_id, title, Str.GetStr(Str.Classify) + ":" + category, url, path, "", token=token)
                # self.CheckCategoryShowItem()
            else:
                QtOwner().ShowError(Str.GetStr(st))

        except Exception as es:
            Log.Error(es)
        pass

    def SendSearch(self, nextId=""):
        QtOwner().ShowLoading()
        if nextId:
            page = self.bookList.page+1
        else:
            page = 1
        self.AddHttpTask(req.GetIndexInfoReq(nextId, self.text), self.SendSearchBack, page)

    def JumpPage(self):
        if self.bookList.page >= self.bookList.pages:
            return
        if not self.bookList.nextId:
            return
        self.bookList.clear()
        if not self.categories:
            self.SendSearch(self.bookList.nextId)
        else:
            self.SendSearchCategories(self.bookList.nextId)
        return

    def LoadNextPage(self):
        if not self.bookList.nextId:
            return
        if not self.categories:
            self.SendSearch(self.bookList.nextId)
        else:
            self.SendSearchCategories(self.bookList.nextId)
        return

    def CheckDirechLink(self, text):
        if not text:
            return False
        import re
        mo = re.search("(?<=/g/).*", text)
        if mo:
            data = mo.group().split("/")
            if len(data) >= 2:
                bookId = data[0]
                token = data[1]
                if bookId and bookId.isdigit():
                    self.lineEdit.AddCacheWord(text)
                    QtOwner().OpenBookInfo(bookId, token)
                    return True
        return False