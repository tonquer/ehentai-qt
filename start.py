# -*- coding: utf-8 -*-
"""第一个程序"""
import os
import sys
current_path = os.path.abspath(__file__)
current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
os.chdir(current_dir)

from conf import config

from PySide2 import QtWidgets  # 导入PySide2部件
from src.qt.qt_main import QtMainWindow
from src.util import Log

import platform
if not platform.system().upper() == 'DARWIN':
    sys.path.insert(0, "lib")

try:
    import waifu2x
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

if __name__ == "__main__":
    Log.Init()
    Log.UpdateLoggingLevel()
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    # app.addLibraryPath("./resources")
    main = QtMainWindow()

    main.show()  # 显示窗体
    main.Init()
    sts = app.exec_()
    sys.exit(sts)  # 运行程序
