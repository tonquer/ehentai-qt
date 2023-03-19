import re

from server.server import Server
from config import config
from tools.log import Log
from tools.singleton import Singleton


class BookBaseInfo(object):
    def __init__(self):
        self.id = 0
        self.title = ""
        self.bookUrl = ""
        self.token = ""       # 收藏和下载使用
        self.apiUid = ""      # TODO
        self.apiKey = ""      # TODO
        self.category = ""
        self.timeStr = ""
        self.imgData = None
        self.imgUrl = ""
        self.tags = []

    def Copy(self, o):
        self.id = o.id
        self.title = o.title
        self.bookUrl = o.bookUrl
        self.token = o.token
        self.apiUid = o.apiUid
        self.category = o.category
        self.timeStr = o.timeStr
        self.imgData = o.imgData
        self.imgUrl = o.imgUrl
        self.tags = o.tags


class BookPageInfo(object):
    def __init__(self):
        self.kv = {}
        self.posted = ""       # 上传日期
        self.language = ""     # 语言
        self.fileSize = ""     # 大小
        self.pages = 0        # 分页
        self.favorites = 0     # 收藏数
        self.picUrl = {}       # index: url
        self.preUrl = {}       # index: url
        self.picRealUrl = {}   # 每张图片对应的下载链接
        self.showKey = ""      # 上下切页需要用的，showKey
        self.comment = []

    def GetImgKey(self, index):
        if index not in self.picUrl:
            return None

        mo = re.search("(?<=/s/)\w+", self.picUrl.get(index))
        return mo.group()

    def Copy(self, o):
        if not o.pages:
            return

        self.kv.update(o.kv)
        self.posted = o.posted
        self.language = o.language
        self.fileSize = o.fileSize
        self.pages = o.pages
        self.favorites = o.favorites
        self.picUrl.update(o.picUrl)
        self.preUrl.update(o.preUrl)
        if len(o.comment) > len(self.comment):
            self.comment = o.comment


class BookInfo(object):
    def __init__(self):
        self.baseInfo = BookBaseInfo()
        self.pageInfo = BookPageInfo()
        self.curPage = 0
        self.maxPage = 1
        self.stepPage = 0
        self.loadPages = set()

    def GetPicInPages(self, index):
        if self.stepPage:
            return index // self.stepPage + 1
        else:
            pages = list(set(range(1, self.maxPage+1)) - self.loadPages)
            pages.sort()
            return pages[0]

    def IsNeedLoadPage(self, index):
        page = self.GetPicInPages(index)
        return page not in self.loadPages

    # 书的管理器
class BookMgr(Singleton):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.books = {"e-hentai": {}, "exhentai": {}}      # id: site: books

    @property
    def server(self):
        return Server()

    def GetBook(self, bookId) -> BookInfo:
        books = self.books.get(config.CurSite, {})
        return books.get(bookId)

    def RemoveBook(self, bookId, site):
        books = self.books.get(site, {})
        if bookId in books:
            del books[bookId]

    def GetBookBySite(self, bookId, site) -> BookInfo:
        books = self.books.get(site, {})
        return books.get(bookId)

    def UpdateBookInfoList(self, bookList, site):
        for info in bookList:
            assert isinstance(info, BookInfo)
            if self.GetBookBySite(info.baseInfo.id, site):
                continue
            info.stepPage = len(info.pageInfo.picUrl)
            self.books[site][info.baseInfo.id] = info
        # Log.Warn("update book list, {}, {}, {}".format(site, len(bookList), len(self.books[site])))

    def UpdateBookInfo(self, bookId, info, curPage, maxPage, site):
        book = self.GetBookBySite(bookId, site)
        assert isinstance(info, BookInfo)
        if not book:
            info.loadPages.add(curPage)
            info.maxPage = maxPage
            self.books[site][bookId] = info
            info.stepPage = len(info.pageInfo.picUrl)
            return
        book.baseInfo.Copy(info.baseInfo)
        book.pageInfo.Copy(info.pageInfo)
        book.maxPage = maxPage
        book.loadPages.add(curPage)

        step = len(info.pageInfo.picUrl)
        if not book.stepPage:
            book.stepPage = step
        if step and curPage != maxPage and step != book.stepPage:
            book.stepPage = 0
        return

    def UpdateImgUrl(self, bookId, index, url, site):
        book = self.GetBookBySite(bookId, site)
        if not book:
            return
        book.pageInfo.picRealUrl[index] = url
        return

    def UpdateImgKey(self, bookId, key, site):
        book = self.GetBookBySite(bookId, site)
        if not book:
            return
        book.pageInfo.showKey = key
