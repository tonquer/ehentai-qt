import sys

Url = "https://e-hentai.org"       # 域名
FormUrl = "https://forums.e-hentai.org"       # 域名
ApiUrl = "https://api.e-hentai.org/api.php"

ThreadNum = 10                                # 线程
DownloadThreadNum = 5                        # 下载线程
HttpProxy = ""                               # 代理

SavePath = ''
SavePathDir = "commies"       # 下载目录
ResetCnt = 5                  # 下载重试次数

IsUseCache = True             # 是否使用cache
CachePathDir = "cache"        # cache目录
# CacheExpired = 24 * 60 * 60    # cache过期时间24小时
PreLoading = 5    # 预加载5页

IsLoadingPicture = True

UpdateUrl = "https://github.com/tonquer/ehentai-windows/releases/latest"
UpdateUrl2 = "https://github.com/tonquer/ehentai-windows/releases"
UpdateVersion = "v1.0.0"

# waifu2x
CanWaifu2x = True

Encode = 0
Waifu2xThread = 2
Format = "jpg"
Waifu2xPath = "waifu2x"
IsOpenWaifu = True

LookModel = 0       # 默认值
DownloadModel = 0   # 默认值
LogIndex = 1
IsTips = 1

Model1 = "cunet"     # 通用
Model2 = "photo"     # 写真
Model3 = "anime_style_art_rgb"  # 动漫

