from PySide2 import QtWidgets

from src.book.book import BookMgr
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Log
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

    def SwitchCurrent(self):
        if not self.isInit:
            self.isInit = True
            self.Search()
        pass

    def Search(self, categories=None):
        data = self.searchEdit.text()
        self.data = data
        if not categories:
            self.categories = []
        else:
            pass
        self.categories = ""
        self.bookList.clear()
        self.bookList.UpdatePage(1, 1)
        self.bookList.UpdateState()
        self.searchEdit.setPlaceholderText("")
        self.SendSearch(self.data, 1)

    def SendSearch(self, data, page):
        QtOwner().owner.loadingForm.show()
        self.index = 1
        self.AddHttpTask(req.GetIndexInfoReq(page, data), self.SendSearchBack, page)

    def SendSearchBack(self, data, page):
        QtOwner().owner.loadingForm.close()
        try:
            self.bookList.UpdateState()
            st = data.get("st")
            if st == Status.Ok:
                pages = data.get("maxPages")
                self.bookList.UpdatePage(page, pages)
                self.spinBox.setMaximum(pages)
                pageText = "页：" + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for info in data.get("bookList"):
                    _id = info.baseInfo.id
                    title = info.baseInfo.title
                    url = info.baseInfo.imgUrl
                    self.bookList.AddBookItem(_id, title, "", url, "", "")
                # self.CheckCategoryShowItem()
            else:
                QtOwner().owner.msgForm.ShowError(st)
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
        self.SendSearch(self.data, page)
        return

    def LoadNextPage(self):
        self.SendSearch(self.data, self.bookList.page + 1)
        return

    def ChangeSort(self, pos):
        self.bookList.page = 1
        self.bookList.clear()
        self.SendSearch(self.data, 1)

    def ClickCategoryListItem(self, item):
        isClick = self.categoryList.ClickItem(item)
        data = item.text()
        if isClick:
            QtOwner().owner.msgForm.ShowMsg("屏蔽" + data)
        else:
            QtOwner().owner.msgForm.ShowMsg("取消屏蔽" + data)
        self.CheckCategoryShowItem()

    def CheckCategoryShowItem(self):
        data = self.categoryList.GetAllSelectItem()
        for i in range(self.bookList.count()):
            item = self.bookList.item(i)
            widget = self.bookList.itemWidget(item)
            isHidden = False
            for name in data:
                if name in widget.param:
                    item.setHidden(True)
                    isHidden = True
                    break
            if not isHidden:
                item.setHidden(False)

    def ClickKeywordListItem(self, item):
        data = item.text()
        self.searchEdit.setText(data)
        self.Search()
