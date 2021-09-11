# -*- coding: utf-8 -*-
"""第一个程序"""
import os
import sys

from PySide2.QtCore import Qt

from conf import config


if sys.platform == 'darwin':
    # 确保工作区为当前可执行文件所在目录
    current_path = os.path.abspath(__file__)
    current_dir = os.path.abspath(os.path.dirname(current_path) + os.path.sep + '.')
    os.chdir(current_dir)
else:
    sys.path.insert(0, "lib")

try:
    import waifu2x
    config.CanWaifu2x = True
except Exception as es:
    config.CanWaifu2x = False
    if hasattr(es, "msg"):
        config.ErrorMsg = es.msg

from PySide2 import QtWidgets  # 导入PySide2部件
from src.qt.qt_main import QtMainWindow
from src.util import Log


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    Log.Init()
    Log.UpdateLoggingLevel()
    app = QtWidgets.QApplication(sys.argv)  # 建立application对象
    # app.addLibraryPath("./resources")
    main = QtMainWindow(app)

    main.show()  # 显示窗体
    main.Init()
    sts = app.exec_()
    main.Stop()
    sys.exit(sts)  # 运行程序
