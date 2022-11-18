import os

from PySide2.QtSql import QSqlDatabase, QSqlQuery

from config.setting import Setting
from tools.log import Log
from view.download.download_item import DownloadItem


class DownloadDb(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "download")
        path = Setting.GetConfigPath()
        self.db.setDatabaseName(os.path.join(path, "download.db"))
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists download(\
            bookId varchar primary key,\
            curPreDownloadIndex int,\
            curPreConvertId int,\
            picCnt int,\
            title varchar,\
            savePath varchar,\
            convertPath varchar,\
            status varchar,\
            convertStatus varchar,\
            token varchar,\
            domain varchar,\
            size bigint\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

    def DelDownloadDB(self, bookId):
        query = QSqlQuery(self.db)
        sql = "delete from download where bookId='{}'".format(bookId)
        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())

    def AddDownloadDB(self, task):
        assert isinstance(task, DownloadItem)

        query = QSqlQuery(self.db)
        sql = "INSERT INTO download(bookId, curPreDownloadIndex, curPreConvertId, picCnt, title, " \
              "savePath, convertPath, status, convertStatus, token, domain, size) " \
              "VALUES ('{0}', {1}, {2}, {3}, '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', {11}) " \
              "ON CONFLICT(bookId) DO UPDATE SET curPreDownloadIndex={1}, curPreConvertId={2}, picCnt={3}, " \
              "title = '{4}', savePath = '{5}', convertPath= '{6}', status = '{7}', convertStatus = '{8}', token = '{9}', domain= '{10}', size={11}".\
            format(task.bookId, task.curDownloadPic, task.curPreConvertId, task.maxDownloadPic, task.title.replace("'", "''"),
                   task.savePath.replace("'", "''"), task.convertPath.replace("'", "''"), task.status, task.convertStatus, task.token, task.site, task.size)

        suc = query.exec_(sql)
        if not suc:
            Log.Warn(query.lastError().text())
        return

    def LoadDownload(self, owner):
        query = QSqlQuery(self.db)
        suc = query.exec_(
            """
            select * from download
            """
        )
        if not suc:
            Log.Warn(query.lastError().text())
        downloads = {}
        while query.next():
            # bookId, downloadEpsIds, curDownloadEpsId, curConvertEpsId, title, savePath, convertPath
            info = DownloadItem()
            info.bookId = query.value(0)
            info.curDownloadPic = query.value(1)
            info.curPreConvertId = query.value(2)
            info.maxDownloadPic = query.value(3)
            info.title = query.value(4)
            info.savePath = query.value(5)
            info.convertPath = query.value(6)
            info.status = query.value(7)
            info.convertStatus = query.value(8)
            info.token = query.value(9)
            info.site = query.value(10)
            info.size = query.value(11)
            downloads[info.bookId] = info

        return downloads