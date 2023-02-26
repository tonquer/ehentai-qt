# -*- coding: utf-8 -*-
"""第一个程序"""
import os
import sys
# macOS 修复
import time
import traceback


from qt_error import showError, showError2
from tools.log import Log
from tools.str import Str

if sys.platform == 'darwin':
    # 确保工作区为当前可执行文件所在目录
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
    os.chdir(current_dir)
# else:
#     sys.path.insert(0, "lib")

from config import config
try:
    from waifu2x_vulkan import waifu2x_vulkan
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

from PySide6.QtGui import QFont
from PySide6 import QtWidgets  # 导入PySide6部件
from PySide6.QtNetwork import QLocalSocket, QLocalServer
# 此处不能删除
import images_rc


if __name__ == "__main__":
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt, QCoreApplication
        from PySide6.QtGui import QGuiApplication, QFont
        from config.setting import Setting
        Log.Init()
        Setting.Init()
        Setting.InitLoadSetting()
        indexV = Setting.ScaleLevel.GetIndexV()
        if indexV and indexV != "Auto":
            # if indexV == 100:
            #     QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)
            # else:
            QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
            os.environ["QT_SCALE_FACTOR"] = str(indexV / 100)
        else:
            QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    except Exception as es:
        Log.Error(es)
        app = QApplication(sys.argv)
        showError(traceback.format_exc(), app)
        if config.CanWaifu2x:
            waifu2x_vulkan.stop()
        sys.exit(-111)

    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    serverName = 'EHentai-qt'
    socket = QLocalSocket()
    socket.connectToServer(serverName)
    if socket.waitForConnected(500):
        socket.write(b"restart")
        socket.flush()
        socket.close()
        app.quit()
        Log.Warn("server already star")
        exit(1)

    localServer = QLocalServer()  # 没有实例运行，创建服务器
    localServer.listen(serverName)

    Log.Warn("init scene ratio: {}".format(app.devicePixelRatio()))
    try:
        from qt_owner import QtOwner
        Str.Reload()
        QtOwner().SetApp(app)
        QtOwner().SetFont()
        from view.main.main_view import MainView
        main = MainView()
        main.show()  # 显示窗体
        main.Init()
    except Exception as es:
        Log.Error(es)
        showError(traceback.format_exc(), app)
        if config.CanWaifu2x:
            waifu2x_vulkan.stop()
        sys.exit(-111)

    oldHook = sys.excepthook
    def excepthook(exc_type, exc_value, exc_tb):
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        Log.Error(tb)
        showError2(tb, app)

    sys.excepthook = excepthook

    sts = app.exec()
    socket.close()
    main.Stop()
    if config.CanWaifu2x:
        waifu2x_vulkan.stop()
    time.sleep(1)
    sys.exit(sts)  # 运行程序
