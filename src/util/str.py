from enum import Enum

from PySide6.QtCore import QObject


class QtStrObj(QObject):
    def __init__(self):
        QObject.__init__(self)


class Str:
    obj = QtStrObj()
    strDict = dict()

    # Enum

    Ok = 1001              # "成功"
    Load = 1002            # "加载"
    Error = 1003           # "错误"
    WaitLoad = 1004        # "等待"
    NetError = 1005        # "网络错误，请检查代理设置"
    UserError = 1006       # "用户名密码错误"
    RegisterError = 1007   # "注册失败"
    UnKnowError = 1008     # "未知错误，"
    NotFoundBook = 1009    # "未找到书籍"
    ParseError = 1010      # "解析出错了"
    NeedGoogle = 1011      # "需要谷歌验证"

    Success = 2001         # "下载完成"
    Reading = 2002         # "获取信息"
    ReadingEps = 2003      # "获取分页"
    ReadingPicture = 2004  # "获取下载地址"
    DownloadCover = 2005   # "正在下载封面"
    Downloading = 2006     # "正在下载"
    Waiting = 2007         # "等待中"
    Pause = 2008           # "暂停"
    DownError = 2009       # "出错了"
    NotFound = 2010        # "原始文件不存在"
    Converting = 2011      # "转换中"
    ConvertSuccess = 2012  # "转换成功"

    LoadingPicture = 1     # "图片加载中..."
    LoadingFail = 2        # "图片加载失败"
    LoginCookie = 3        # "使用Cookie登录"
    LoginUser = 4          # "使用账号登录"
    NotSpace = 5           # "不能为空"
    LoginFail = 6          # "登录失败"

    @classmethod
    def reload(cls):
        cls.strDict[cls.Ok] = cls.obj.tr("成功")
        cls.strDict[cls.Load] = cls.obj.tr("加载")
        cls.strDict[cls.Error] = cls.obj.tr("错误")
        cls.strDict[cls.WaitLoad] = cls.obj.tr("等待")
        cls.strDict[cls.NetError] = cls.obj.tr("网络错误，请检查代理设置")
        cls.strDict[cls.UserError] = cls.obj.tr("用户名密码错误")
        cls.strDict[cls.RegisterError] = cls.obj.tr("注册失败")
        cls.strDict[cls.UnKnowError] = cls.obj.tr("未知错误")
        cls.strDict[cls.NotFoundBook] = cls.obj.tr("未找到书籍")
        cls.strDict[cls.ParseError] = cls.obj.tr("解析出错了")
        cls.strDict[cls.NeedGoogle] = cls.obj.tr("需要谷歌验证")

        cls.strDict[cls.LoadingPicture] = cls.obj.tr("图片加载中...")
        cls.strDict[cls.LoadingFail] = cls.obj.tr("图片加载失败")
        cls.strDict[cls.LoginCookie] = cls.obj.tr("使用Cookie登录")
        cls.strDict[cls.LoginUser] = cls.obj.tr("使用账号登录")
        cls.strDict[cls.NotSpace] = cls.obj.tr("不能为空")
        cls.strDict[cls.LoginFail] = cls.obj.tr("登录失败")
        cls.strDict[cls.Success] = cls.obj.tr("下载完成")
        cls.strDict[cls.Reading] = cls.obj.tr("获取信息")
        cls.strDict[cls.ReadingEps] = cls.obj.tr("获取分页")
        cls.strDict[cls.ReadingPicture] = cls.obj.tr("获取下载地址")
        cls.strDict[cls.DownloadCover] = cls.obj.tr("正在下载封面")
        cls.strDict[cls.Downloading] = cls.obj.tr("正在下载")
        cls.strDict[cls.Waiting] = cls.obj.tr("等待中")
        cls.strDict[cls.Pause] = cls.obj.tr("暂停")
        cls.strDict[cls.DownError] = cls.obj.tr("出错了")
        cls.strDict[cls.NotFound] = cls.obj.tr("原始文件不存在")
        cls.strDict[cls.Converting] = cls.obj.tr("转换中")
        cls.strDict[cls.ConvertSuccess] = cls.obj.tr("转换成功")

    @classmethod
    def GetStr(cls, enumType):
        return cls.strDict.get(enumType)