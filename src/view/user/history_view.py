import os
import time

from PySide2 import QtWidgets
from PySide2.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from interface.ui_history import Ui_History
from tools.log import Log
from tools.str import Str


class QtHistoryData(object):
    def __init__(self):
        self.bookId = ""         # bookId
        self.token = ""
        self.site = ""
        self.name = ""           # name
        self.picIndex = 0           # 图片Index
        self.url = ""
        self.tick = 0


class HistoryView(QtWidgets.QWidget, Ui_History):
    def __init__(self):
        super(self.__class__, self).__init__()
        Ui_History.__init__(self)
        self.setupUi(self)

        # self.bookList.InitBook(self.LoadNextPage)
        self.pageNums = 20
        self.bookList.LoadCallBack = self.LoadNextPage
        self.history = {}
        self.db = QSqlDatabase.addDatabase("QSQLITE", "history")
        path = os.path.join(Setting.GetConfigPath(), "history.db")
        self.db.setDatabaseName(path)
        # self.bookList.InstallDel()

        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists history_ehentai(\
            bookId varchar,\
            token varchar,\
            site varchar,\
            name varchar,\
            picIndex int,\
            url varchar,\
            tick int,\
            primary key(bookId, token)
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
        self.LoadHistory()
        self.bookList.isDelMenu = True
        self.bookList.DelCallBack = self.DelCallBack

    def SwitchCurrent(self, **kwargs):
        self.bookList.clear()
        self.bookList.page = 1
        self.bookList.pages = len(self.history) // self.pageNums + 1
        self.spinBox.setValue(1)
        self.spinBox.setMaximum(self.pageNums)
        self.bookList.UpdateState()
        self.UpdatePageLabel()
        self.RefreshData(self.bookList.page)

    def GetHistory(self, bookId):
        return self.history.get(bookId)

    def DelHistory(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from history_ehentai where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def AddHistory(self, bookId, token, name, site, index, url):
        tick = int(time.time())
        info = self.history.get(bookId)
        if not info:
            info = QtHistoryData()
            self.history[bookId] = info
        info.bookId = bookId
        info.token = token
        info.name = name
        info.site = site
        info.picIndex = index
        info.url = url
        info.tick = tick

        query = QSqlQuery(self.db)

        sql = "INSERT INTO history_ehentai(bookId, token, name, site, url, picIndex, tick) " \
              "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6}) " \
              "ON CONFLICT(bookId, token) DO UPDATE SET name='{2}', site='{3}', url = '{4}', picIndex={5}, tick={6}".\
            format(bookId, token, name.replace("'", "''"), site, url, index, tick)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadHistory(self):
        query = QSqlQuery(self.db)
        query.exec_(
            """
            select * from history_ehentai
            """
        )
        while query.next():
            # bookId, name, epsId, index, url, path
            info = QtHistoryData()
            info.bookId = query.value(0)
            info.token = query.value(1)
            info.name = query.value(3)
            info.site = query.value(2)
            info.url = query.value(5)
            info.index = query.value(4)
            info.tick = query.value(6)
            self.history[info.bookId] = info
        pass

    def JumpPage(self):
        page = int(self.spinBox.text())
        if page > self.bookList.pages:
            return
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData(page)
        self.UpdatePageLabel()

    def LoadNextPage(self):
        self.bookList.page += 1
        self.RefreshData(self.bookList.page)
        self.UpdatePageLabel()

    def RefreshData(self, page):
        sortedList = list(self.history.values())
        sortedList.sort(key=lambda a: a.tick, reverse=True)
        self.bookList.UpdateState()
        start = (page-1) * self.pageNums
        end = start + self.pageNums
        for info in sortedList[start:end]:
            self.bookList.AddBookItemByHistory(info)

    def UpdatePageLabel(self):
        self.pages.setText(Str.GetStr(Str.Page)+"：{}/{}".format(str(self.bookList.page), str(self.bookList.pages)))

    def DelCallBack(self, bookId):
        if bookId not in self.history:
            return
        self.history.pop(bookId)
        self.DelHistory(bookId)

        page = 1
        self.bookList.page = page
        self.bookList.clear()
        self.RefreshData(page)
        self.UpdatePageLabel()
        return
