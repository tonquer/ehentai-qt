from PySide2 import QtWidgets, QtCore

from component.dialog.base_mask_dialog import BaseMaskDialog
from interface.ui_favorite_info import Ui_FavoriteInfo
from qt_owner import QtOwner
from src.server import req, Status
from task.qt_task import QtTaskBase

from tools.str import Str


class FavoriteInfoView(BaseMaskDialog, Ui_FavoriteInfo, QtTaskBase):
    def __init__(self, parent=None):
        BaseMaskDialog.__init__(self, parent)
        Ui_FavoriteInfo.__init__(self)
        QtTaskBase.__init__(self)

        self.widget.SaveFavorite = self.SaveFavorite
        self.setupUi(self.widget)
        self.closeButton.clicked.connect(self.close)
        self.bookId = ""
        self.isUpdate = True

    def OpenFavorite(self, bookId, bookName):
        QtOwner().ShowLoading()
        self.AddHttpTask(req.AddFavoritesReq(bookId), self.GetFavoriteBack, (bookId, bookName))

    def GetFavoriteBack(self, data, v):
        QtOwner().CloseLoading()
        bookId, bookName = v
        st = data["st"]
        if st == Status.Ok:
            note = data["note"]
            favorites = data["favorites"]
            isUpdate = data["update"]
            self.lineEdit.setText(note)
            self.bookId = bookId
            self.nameLabel.setText(bookName)
            self.isUpdate = isUpdate
            if not self.isUpdate:
                self.pushButton.setText(Str.GetStr(Str.Save))
            else:
                self.pushButton.setText(Str.GetStr(Str.Change))

            for k, v in favorites.items():
                if v:
                    self.comboBox.setCurrentIndex(int(k))

            pass
        else:
            QtOwner().ShowError(Str.GetStr(st))
            self.close()

    def SaveFavorite(self):
        if not self.bookId:
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.AddFavorites2Req(self.bookId, self.comboBox.currentIndex(), self.lineEdit.text(), self.isUpdate), self.SaveFavoriteBack)

    def SaveFavoriteBack(self, data):
        QtOwner().CloseLoading()
        st = data["st"]
        self.close()
        if st != Status.Ok:
            QtOwner().ShowError(Str.GetStr(st))
        else:
            QtOwner().ShowMsg(Str.GetStr(Str.SaveSuc))
