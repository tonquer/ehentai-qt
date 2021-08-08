from PySide2.QtSql import QSqlDatabase, QSqlQuery

from src.util import Log


class Translate(object):
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE", "translate")
        self.db.setDatabaseName("download.db")
        if not self.db.open():
            Log.Warn(self.db.lastError().text())

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists translate(\
            bookId varchar primary key,\
            downloadEpsIds varchar,\
            curDownloadEpsId int,\
            curConvertEpsId int,\
            title varchar,\
            savePath varchar,\
            convertPath varchar,\
            status varchar,\
            convertStatus varchar\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)

        query = QSqlQuery(self.db)
        sql = """\
            create table if not exists download_eps(\
            bookId varchar,\
            epsId int,\
            epsTitle varchar,\
            picCnt int,\
            curPreDownloadIndex int,\
            curPreConvertId int,\
            primary key (bookId,epsId)\
            )\
            """
        suc = query.exec_(sql)
        if not suc:
            a = query.lastError().text()
            Log.Warn(a)
