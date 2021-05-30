from PySide2 import QtWidgets
import weakref

from PySide2.QtWidgets import QCheckBox, QLabel, QCompleter

from src.book.book import BookMgr
from src.qt.com.qtlistwidget import QtBookList, QtIntLimit, QtCategoryList
from src.server import Server, req, Log, json

from src.qt.util.qttask import QtTask
from src.util.status import Status
from ui.search import Ui_search


class QtSearch(QtWidgets.QWidget, Ui_search):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_search.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.index = 1
        self.data = ""
        self.bookList = QtBookList(self, self.__class__.__name__, owner)
        self.bookList.InitBook(self.LoadNextPage)

        self.bookLayout.addWidget(self.bookList)
        self.categories = ""
        self.jumpLine.setValidator(QtIntLimit(1, 1, self))
        self.isInit = False
        self.searchEdit.words = self.owner().words

    def SwitchCurrent(self):
        if not self.isInit:
            self.isInit = True
            self.Search()
        pass

    def InitCheckBox(self):
        # TODO 分类标签有点问题 暂时不显示
        return
        size = len(CateGoryMgr().idToCateGoryBase)
        hBoxLayout = QtWidgets.QHBoxLayout(self)
        a = QCheckBox("全部分类", self.groupBox)
        hBoxLayout.addWidget(a)

        for index, info in enumerate(CateGoryMgr().idToCateGoryBase, 2):
            if index % 9 == 0:
                self.comboBoxLayout.addLayout(hBoxLayout)
                hBoxLayout = QtWidgets.QHBoxLayout(self)
            a = QCheckBox(info.title, self.groupBox)
            hBoxLayout.addWidget(a)
        self.comboBoxLayout.addLayout(hBoxLayout)
        return

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
        self.owner().loadingForm.show()
        self.index = 1
        QtTask().AddHttpTask(req.GetIndexInfoReq(page, data), self.SendSearchBack, page)

    def SendSearchBack(self, raw, page):
        self.owner().loadingForm.close()
        try:
            self.bookList.UpdateState()
            data = json.loads(raw)
            st = data.get("st")
            if st == Status.Ok:
                pages =  data.get("pages")
                self.bookList.UpdatePage(page, pages)
                self.jumpLine.setValidator(QtIntLimit(1, pages, self))
                pageText = "页：" + str(self.bookList.page) + "/" + str(self.bookList.pages)
                self.label.setText(pageText)
                for bookId in data.get("bookList"):
                    _id = bookId
                    info = BookMgr().GetBook(bookId)
                    title = info.baseInfo.title
                    url = info.baseInfo.imgUrl
                    self.bookList.AddBookItem(_id, title, "", url, "", "")
                # self.CheckCategoryShowItem()
            else:
                self.owner().msgForm.ShowError(st)
        except Exception as es:
            Log.Error(es)
        pass

    def SendKeywordBack(self, raw):
        try:
            data = json.loads(raw)
            if data.get("code") == 200:
                self.keywordList.clear()
                for keyword in data.get('data', {}).get("keywords", []):
                    self.keywordList.AddItem(keyword)
                pass
            else:
                pass
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
        self.owner().bookInfoForm.OpenBook(bookId)

    def JumpPage(self):
        page = int(self.jumpLine.text())
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
            self.owner().msgForm.ShowMsg("屏蔽" + data)
        else:
            self.owner().msgForm.ShowMsg("取消屏蔽" + data)
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
