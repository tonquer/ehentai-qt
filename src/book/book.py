import os
import re

from src.server import Server
from src.util import Singleton, Log
from src.server import req


class BookBaseInfo(object):
    def __init__(self):
        self.id = 0
        self.title = ""
        self.bookUrl = ""
        self.category = ""
        self.timeStr = ""
        self.imgData = None
        self.imgUrl = ""
        self.tags = []


class BookPageInfo(object):
    def __init__(self):
        self.kv = {}
        self.posted = ""       # 上传日期
        self.language = ""     # 语言
        self.fileSize = ""     # 大小
        self.pages = 0        # 分页
        self.favorites = 0     # 收藏数
        self.picUrl = {}      # index: url
        self.picRealUrl = {}
        self.showKey = ""     # showKey
        self.comment = []

    def GetImgKey(self, index):
        if index not in self.picUrl:
            return None
        mo = re.search("(?<=/s/)\w+", self.picUrl.get(index))
        return mo.group()

    def Copy(self, o):
        self.kv.update(o.kv)
        self.posted = o.posted
        self.language = o.language
        self.fileSize = o.fileSize
        self.pages = o.pages
        self.favorites = o.favorites
        self.picUrl.update(o.picUrl)
        self.comment = o.comment


class BookInfo(object):
    def __init__(self):
        self.baseInfo = BookBaseInfo()
        self.pageInfo = BookPageInfo()


# 书的管理器
class BookMgr(Singleton):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.books = {}      # id: book

    @property
    def server(self):
        return Server()

    def GetBook(self, bookId) -> BookInfo:
        return self.books.get(bookId)

    def UpdateBookInfoList(self, bookList):
        for info in bookList:
            assert isinstance(info, BookInfo)
            if info.baseInfo.id in self.books:
                continue
            self.books[info.baseInfo.id] = info

    def UpdateBookInfo(self, bookId, info):
        book = self.GetBook(bookId)
        if not book:
            return
        book.pageInfo.Copy(info)
        return

    def UpdateImgUrl(self, bookId, index, url):
        book = self.GetBook(bookId)
        if not book:
            return
        book.pageInfo.picRealUrl[index] = url
        return

    def UpdateImgKey(self, bookId, key):
        book = self.GetBook(bookId)
        if not book:
            return
        book.pageInfo.showKey = key
