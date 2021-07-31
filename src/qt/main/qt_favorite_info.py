from PySide2 import QtWidgets, QtCore

from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.com.qtloading import QtLoading
from src.qt.util.qttask import QtTaskBase
from src.server import req, Status
from ui.favorite import Ui_favorite
from ui.favorite_info import Ui_Favorite_Info


class QtFavoriteInfo(QtWidgets.QWidget, Ui_Favorite_Info, QtTaskBase):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_favorite.__init__(self)
        QtTaskBase.__init__(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.loadingForm = QtLoading(self)
        self.setupUi(self)
        self.bookId = ""
        self.isUpdate = True

    def OpenFavorite(self, bookId, bookName):
        self.show()
        self.loadingForm.show()
        self.AddHttpTask(req.AddFavoritesReq(bookId), self.GetFavoriteBack, (bookId, bookName))

    def GetFavoriteBack(self, data, v):
        self.loadingForm.close()
        bookId, bookName = v
        if data["st"] == Status.Ok:
            note = data["note"]
            favorites = data["favorites"]
            isUpdate = data["update"]
            self.lineEdit.setText(note)
            self.bookId = bookId
            self.nameLabel.setText(bookName)
            self.isUpdate = isUpdate
            if not self.isUpdate:
                self.pushButton.setText("保存")
            else:
                self.pushButton.setText("更改")
            for k, v in favorites.items():
                if v:
                    self.comboBox.setCurrentIndex(int(k))

            pass
        else:
            QtBubbleLabel().ShowErrorEx(self, "出错了")
            self.close()

    def SaveFavorite(self):
        if not self.bookId:
            return
        self.loadingForm.show()
        self.AddHttpTask(req.AddFavorites2Req(self.bookId, self.comboBox.currentIndex(), self.lineEdit.text(), self.isUpdate), self.SaveFavoriteBack)

    def SaveFavoriteBack(self, data):
        self.loadingForm.close()
        if data["st"] != Status.Ok:
            QtBubbleLabel().ShowErrorEx(self, "出错了")
        else:
            QtBubbleLabel().ShowMsgEx(self, "保存成功")
        self.close()
