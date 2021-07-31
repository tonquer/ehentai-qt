import re

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, QEvent
from PySide2.QtGui import QPixmap

from resources import resources
from src.qt.com.qtimg import QtImgMgr
from src.qt.qt_main import QtOwner
from ui.user import Ui_User


class QtUser(QtWidgets.QWidget, Ui_User):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_User.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("E-hentai")

        pix = QtGui.QPixmap()
        pix.loadFromData(resources.DataMgr.GetData("placeholder_avatar"))
        pix.scaled(self.icon.size(), Qt.KeepAspectRatio)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(pix)
        self.pictureData = None
        self.icon.installEventFilter(self)
        self.buttonGroup.buttonClicked.connect(self.Switch)
        self.stackedWidget.addWidget(QtOwner().owner.searchForm)
        self.stackedWidget.addWidget(QtOwner().owner.favoriteForm)

    def SetPicture(self, data):
        a = QPixmap()
        a.loadFromData(data)
        self.pictureData = data
        self.icon.setPixmap(a)

    def Switch(self, button):
        if isinstance(button, int):
            index = button
        else:
            index = int(re.findall(r"\d+", button.objectName())[0])
        self.stackedWidget.setCurrentIndex(index)
        self.stackedWidget.currentWidget().SwitchCurrent()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.pictureData:
                    QtImgMgr().ShowImg(self.pictureData)
                return True
            else:
                return False
        else:
            return super(self.__class__, self).eventFilter(obj, event)