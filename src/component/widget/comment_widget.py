import json

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from config import config
from interface.ui_comment import Ui_Comment
from qt_owner import QtOwner
from server import req, Status
from task.qt_task import QtTaskBase
from tools.book import BookMgr
from tools.log import Log
from tools.str import Str
from tools.tool import ToolUtil


class CommentWidget(QtWidgets.QWidget, Ui_Comment, QtTaskBase):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        Ui_Comment.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)
        self.spinBox.setVisible(False)
        self.skipButton.setVisible(False)

        self.bookId = ""
        self.site = ""
        self.pushButton.clicked.connect(self.SendComment)

    def SwitchCurrent(self, **kwargs):
        bookId = kwargs.get("bookId")
        site = kwargs.get("site")
        refresh = kwargs.get("refresh")
        if not bookId and self.listWidget.count() > 0 and not refresh:
            return

        self.bookId = bookId
        self.site = site
        self.LoadComment()
        pass

    def ClearCommnetList(self):
        self.listWidget.SetWheelStatus(True)
        self.listWidget.clear()
        self.listWidget.UpdatePage(1, 1)
        self.listWidget.UpdateState()
        # self.spinBox.setValue(1)
        # self.nums.setText("分页：{}/{}".format(str(1), str(1)))
        self.ClearTask()

    def LoadComment(self):
        # QtOwner().ShowLoading()
        self.ClearCommnetList()
        info = BookMgr().GetBookBySite(self.bookId, self.site)
        if not info:
            QtOwner().ShowError(Str.GetStr(Str.Error))
            return
        data = []
        for v in info.pageInfo.comment:
            tick, name = ToolUtil.ConvertEhentaiDate(v[0])
            data.append((tick, name, v[1]))

        data.sort(key=lambda a: a[0], reverse=True)
        for index, v in enumerate(data):
            floor = len(data) - index
            tick, name, comment = v
            self.listWidget.AddUserItem(ToolUtil.ConvertDate(tick) + "     by "+name, comment, floor)
        # self.AddHttpTask(self.reqGetComment(self.bookId, self.listWidget.page), self.GetCommnetBack)
        return

    def SendComment(self):
        data = self.commentLine.text()
        if not data:
            return
        if not config.CurLoginName:
            QtOwner().ShowError(Str.GetStr(Str.NotLogin))
            return
        QtOwner().ShowLoading()
        self.AddHttpTask(req.SendCommentReq(self.bookId, data), callBack=self.SendCommentBack)

    def SendCommentBack(self, raw):
        QtOwner().CloseLoading()
        try:
            st = raw["st"]
            msg = raw.get("msg")
            if st != Status.Ok:
                QtOwner().ShowError(Str.GetStr(st))
                return
            if msg:
                QtOwner().ShowError(msg)
                return
            self.commentLine.setText("")
            self.LoadComment()
        except Exception as es:
            Log.Error(es)
