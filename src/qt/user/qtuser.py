import re

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, QEvent, QTimer
from PySide2.QtGui import QPixmap

from conf import config
from resources import resources
from src.qt.com.qtimg import QtImgMgr
from src.qt.qt_main import QtOwner
from src.qt.util.qttask import QtTaskBase
from src.server import req
from src.util.status import Status
from ui.user import Ui_User


class QtUser(QtWidgets.QWidget, Ui_User, QtTaskBase):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_User.__init__(self)
        QtTaskBase.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("E-hentai")

        # self.icon.setScaledContents(True)
        self.icon.SetPicture(resources.DataMgr.GetData("logo_round"))
        self.pictureData = None
        self.icon.installEventFilter(self)
        self.buttonGroup.buttonClicked.connect(self.Switch)
        self.stackedWidget.addWidget(QtOwner().owner.searchForm)
        self.stackedWidget.addWidget(QtOwner().owner.favoriteForm)
        self.stackedWidget.addWidget(QtOwner().owner.downloadForm)

        self.loginTimer = QTimer()
        self.loginTimer.timeout.connect(self.UpdatePicLimit)
        self.loginTimer.setInterval(60000)
        self.dirty = True

    def SetPicture(self, data):
        self.pictureData = data
        self.icon.SetPicture(data)

    def Switch(self, button):
        if isinstance(button, int):
            index = button
        else:
            index = int(re.findall(r"\d+", button.objectName())[0])
        self.stackedWidget.setCurrentIndex(index)
        self.stackedWidget.currentWidget().SwitchCurrent()

    def SetDirty(self):
        if not self.name.text():
            return
        if self.dirty:
            return

        self.dirty = True
        if not self.loginTimer.isActive():
            self.loginTimer.start()

    def SetLoginName(self, name):
        self.name.setText(name)
        self.UpdatePicLimit()
        return

    def UpdatePicLimit(self):
        self.AddHttpTask(req.HomeReq(), self.UpdatePicLimitBack)
        self.loginTimer.stop()
        self.dirty = False
        return

    def UpdatePicLimitBack(self, data):
        if data["st"] == Status.Ok:
            curNum = data["curNum"]
            maxNum = data["maxNum"]
            self.limitLabel.setText("{}/{}".format(curNum, maxNum))

    def SwithSite(self):
        QtOwner().owner.loadingForm.show()
        if config.CurSite == "exhentai":
            self.SwitchSiteBack({"st": Status.Ok}, "e-hentai")
        else:
            self.AddHttpTask(req.GetIndexInfoReq(site="exhentai"), self.SwitchSiteBack, "exhentai")
        return

    def SwitchSiteBack(self, data, newSite):
        QtOwner().owner.loadingForm.close()
        if data["st"] == Status.Ok:
            config.CurSite = newSite
            self.siteLabel.setText(config.CurSite)
            igneous = data.get("igneous")
            if igneous and igneous != "mystery":
                QtOwner().owner.settingForm.SetSettingV("igneous", igneous)
            QtOwner().ShowMsg(self.tr("成功"))
            QtOwner().owner.userForm.toolButton0.click()
        else:
            QtOwner().ShowError(self.tr("切换失败"))
        return

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