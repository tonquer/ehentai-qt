from PySide2 import QtWidgets
from PySide2.QtWidgets import QAbstractItemView

from conf import config
from src.book.book import BookMgr
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log
from src.util import ToolUtil
from src.util.status import Status
from ui.search import Ui_search


class QtSearch(QtWidgets.QWidget, Ui_search, QtTaskBase):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_search.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.index = 1
        self.data = ""
        self.bookList.InitBook(self.LoadNextPage)

        self.categories = ""
        self.isInit = False
        self.searchEdit.words = QtOwner().owner.words

        self.categoryList.itemClicked.connect(self.ClickKeywordListItem)
        self.categoryList.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

    def retranslateUi(self, search):
        Ui_search.retranslateUi(self, search)
        search.categoryList.clear()
        for key, value in ToolUtil.Category.items():
            if config.Language == "English":
                search.categoryList.AddItem(key)
            else:
                search.categoryList.AddItem(value)

    def SwitchCurrent(self):
        self.Search()

    def Search(self, categories=""):
        data = self.searchEdit.text()
        if not categories:
            self.data = data
            self.categories = ""
        else:
            self.categories = categories
        self.bookList.clear()
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        if self.categories:
            self.searchEdit.setText("")
            self.searchEdit.setPlaceholderText(categories)
            self.SendSearch(self.categories, 1, True)
        else:
            self.searchEdit.setPlaceholderText("")
            self.SendSearch(self.data, 1)

    def SendSearch(self, data, page, isCategory=False):
        QtOwner().owner.loadingForm.show()
        self.index = 1
        if not isCategory:
            self.AddHttpTask(req.GetIndexInfoReq(page, data), self.SendSearchBack, page)
        else:
            for k, v in ToolUtil.Category.items():
                if v == data or k == data:
                    self.AddHttpTask(req.GetCategoryInfoReq(page, k), self.SendSearchBack, page)
                    break

    def SendSearchBack(self, data, page):
        QtOwner().owner.loadingForm.close()
        try:
            self.bookList.UpdateState()
            st = data.get("st")
            if st == Status.Ok:
                pages = data.get("maxPages")
                self.bookList.UpdatePage(page, pages)
                self.spinBox.setMaximum(pages)
                pageText = self.tr("页：") + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for info in data.get("bookList"):
                    _id = info.baseInfo.id
                    title = info.baseInfo.title
                    url = info.baseInfo.imgUrl
                    category = QtOwner().owner.GetCategoryName(info.baseInfo.category)
                    path = "{}/{}-cover".format(config.CurSite, _id)
                    self.bookList.AddBookItem(_id, title, self.tr("分类：")+category, url, path, "")
                # self.CheckCategoryShowItem()
            else:
                QtOwner().owner.msgForm.ShowError(QtOwner().owner.GetStatusStr(st))
        except Exception as es:
            Log.Error(es)
        pass

    def OpenSearch(self, modelIndex):
        index = modelIndex.row()
        item = self.bookList.item(index)
        if not item:
            return
        widget = self.bookList.itemWidget(item)
        if not widget:
            return
        bookId = widget.id
        if not bookId:
            return
        QtOwner().owner.bookInfoForm.OpenBook(bookId)

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        if self.categories:
            self.SendSearch(self.categories, page, True)
        else:
            self.SendSearch(self.data, page, False)
        return

    def LoadNextPage(self):
        if self.categories:
            self.SendSearch(self.categories, self.bookList.page + 1, True)
        else:
            self.SendSearch(self.data, self.bookList.page + 1, False)
        return

    def ChangeSort(self, pos):
        self.bookList.page = 1
        self.bookList.clear()
        self.SendSearch(self.data, 1)

    def ClickKeywordListItem(self, item):
        data = item.text()
        self.searchEdit.setText("")
        self.Search(data)
