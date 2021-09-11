Url = "https://e-hentai.org"       # 域名
ExUrl = "https://exhentai.org"       # 域名
FormUrl = "https://forums.e-hentai.org"       # 域名
ApiUrl = "https://api.e-hentai.org/api.php"

IsUpdate = 1                   # 是否在启动时检查更新
Language = 'Chinese-Simplified'           # 选择的语言
ThreadNum = 10                                # 线程
DownloadThreadNum = 5                        # 下载线程
IsHttpProxy = 0
HttpProxy = ""                               # 代理

SavePath = ''
SavePathDir = "commies"       # 下载目录
ResetCnt = 5                  # 下载重试次数

IsUseCache = True             # 是否使用cache
CachePathDir = "cache"        # cache目录
# CacheExpired = 24 * 60 * 60    # cache过期时间24小时
PreLoading = 10    # 预加载5页

IsLoadingPicture = True

UpdateUrl = "https://github.com/tonquer/ehentai-windows/releases/latest"
UpdateUrlBack = "https://hub.fastgit.org/tonquer/ehentai-windows/releases/latest"
UpdateUrl2 = "https://github.com/tonquer/ehentai-windows/releases"
UpdateUrl2Back = "https://hub.fastgit.org/tonquer/ehentai-windows/releases"
UpdateVersion = "v1.0.3"

CurSite = "e-hentai"   # 当前站点

# waifu2x
CanWaifu2x = True
ErrorMsg = ""

Encode = 0
Waifu2xThread = 2
Format = "jpg"
Waifu2xPath = "waifu2x"
IsOpenWaifu = 0

ThemeText = ""  # 主题

LogIndex = 0   # Warn Info Debug
IsTips = 1

ChatSendAction = 2

DownloadModel = 0
DownloadNoise = 3
DownloadScale = 2.0
DownloadAuto = 0

LookModel = 0
LookNoise = 3
LookScale = 2.0

LookReadMode = 1      # 看图模式
# LookReadScale = 2     # 默认缩放
LookReadFull = 0      # 是否全屏

# https://ehwiki.org/wiki/IPs
IsOpenDoh = 1         # 是否使用Doh进行Dns查询
DohAddress = "https://1.1.1.1/dns-query"
LocalProxyPort = 0
ProxySelectIndex = 1

DomainDns = {
    "e-hentai.org": "104.20.135.21",
    "exhentai.org": "178.175.128.254",
    "ehgt.org": "37.48.89.44",
    "forums.e-hentai.org": "104.20.135.21",
    "gt0.ehgt.org": "37.48.89.44",
    "api.e-hentai.org": "104.20.135.21",
}

DomainMapping = {
    "gt0.ehgt.org": "ehgt.org",
    "forums.e-hentai.org": "e-hentai.org"
}