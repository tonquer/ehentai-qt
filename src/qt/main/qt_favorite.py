from PySide2 import QtWidgets

from conf import config
from src.qt.com.qtmsg import QtMsgLabel
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req, Status
from ui.favorite import Ui_favorite


class QtFavorite(QtWidgets.QWidget, Ui_favorite, QtTaskBase):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_favorite.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.bookList.InitFavorite()
        # action = self.bookList.popMenu.addAction("删除")
        # action.triggered.connect(self.DeleteHandler)
        # for i in range(0, 10):
        #     self.comboBox.addItem("收藏"+str(i))

    def SwitchCurrent(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.clear()
        self.GetFavorites()
        pass

    def GetFavorites(self, page=1):
        curIndex = self.comboBox.currentIndex()
        if curIndex <= 0:
            favcat = ""
        else:
            favcat = str(curIndex-1)
        QtOwner().owner.loadingForm.show()
        self.AddHttpTask(req.GetFavoritesReq(favcat, page), self.GetFavoritesBack, page)

    def GetFavoritesBack(self, data, page):
        QtOwner().owner.loadingForm.close()
        self.bookList.UpdateState()
        if data['st'] == Status.Ok:
            bookList = data["bookList"]
            maxPages = data["maxPages"]
            favoriteList = data["favoriteList"]
            self.bookList.UpdatePage(page, maxPages)
            allNum = sum(favoriteList.values())
            self.comboBox.setItemText(0, self.tr("所有")+"({})".format(str(allNum)))
            for k, v in favoriteList.items():
                self.comboBox.setItemText(k+1, self.tr("收藏")+"{}({})".format(str(k), str(v)))
            for info in bookList:
                _id = info.baseInfo.id
                title = info.baseInfo.title
                url = info.baseInfo.imgUrl
                category = QtOwner().owner.GetCategoryName(info.baseInfo.category)
                path = "{}/{}-cover".format(config.CurSite, _id)
                self.bookList.AddBookItem(_id, title, self.tr("分类：")+category, url, path, "")
        else:
            QtMsgLabel().ShowErrorEx(self, QtOwner.owner.GetStatusStr(data['st']))
        pass

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.GetFavorites(page)
        return

    def JumpFavcat(self):
        self.bookList.UpdatePage(1, 1)
        self.bookList.clear()
        self.GetFavorites(1)
        return

    def LoadNextPage(self):
        self.GetFavorites(self.bookList.page + 1)
        return

    def DeleteHandler(self):
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
            QtMsgLabel.ShowMsgEx(self, self.tr("删除成功"))
        self.SwitchCurrent()
