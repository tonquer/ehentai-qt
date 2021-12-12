# -*- coding: utf-8 -*-
"""第一个程序"""
import os
import sys
# macOS 修复
import time

from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtGui import QGuiApplication

from config import config
from config.setting import Setting
from qt_owner import QtOwner
from tools.log import Log
from tools.str import Str
from view.main.main_view import MainView

if sys.platform == 'darwin':
    # 确保工作区为当前可执行文件所在目录
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
    os.chdir(current_dir)
# else:
#     sys.path.insert(0, "lib")

try:
    from waifu2x_vulkan import waifu2x_vulkan
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

from PySide2 import QtWidgets  # 导入PySide2部件

# 此处不能删除
import images_rc


if __name__ == "__main__":
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
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.Floor)
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    Log.Warn("init scene ratio: {}".format(app.devicePixelRatio()))
    Str.Reload()
    try:
        QtOwner().SetApp(app)
        main = MainView()
    except Exception as es:
        Log.Error(es)
        sys.exit(-111)
    main.show()  # 显示窗体
    main.Init()
    sts = app.exec_()
    main.Stop()
    if config.CanWaifu2x:
        waifu2x_vulkan.stop()
    time.sleep(1)
    sys.exit(sts)  # 运行程序
