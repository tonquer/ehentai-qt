import base64

from PySide2 import QtWidgets
from PySide2.QtCore import QSettings, Qt, QSize
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QFileDialog

from conf import config
from qss.qss import QssDataMgr
from src.qt.com.qtbubblelabel import QtBubbleLabel
from src.qt.qt_main import QtOwner
from src.util import Log
from ui.setting import Ui_Setting


class QtSetting(QtWidgets.QWidget, Ui_Setting):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_Setting.__init__(self)
        self.setupUi(self)
        self.settings = QSettings('config.ini', QSettings.IniFormat)
        self.setWindowModality(Qt.ApplicationModal)
        self.mainSize = None
        self.bookSize = QSize(900, 1020)
        self.readSize = QSize(1120, 1020)
        self.userId = ""
        self.passwd = ""
        self.gpuInfos = []
        # for text in QssDataMgr.files:
        #     self.themeBox.addItem(text)


    def show(self):
        self.LoadSetting()
        super(self.__class__, self).show()

    def LoadSetting(self):
        config.DownloadThreadNum = int(self.settings.value("DownloadThreadNum") or config.DownloadThreadNum)
        self.comboBox.setCurrentIndex(config.DownloadThreadNum-2)

        httpProxy = self.settings.value("Proxy/Http") or config.HttpProxy
        if httpProxy:
            config.HttpProxy = httpProxy
            self.httpEdit.setText(config.HttpProxy)

        isProxy = self.settings.value("Proxy/IsHttp")
        if isProxy is None:
            isProxy = not not config.HttpProxy
        config.IsHttpProxy = not not isProxy
        self.httpProxy.setChecked(config.IsHttpProxy)
        if not config.IsHttpProxy:
            config.HttpProxy = ""

        config.SavePath = self.GetSettingV("SavePath", config.SavePath)
        self.saveEdit.setText(config.SavePath)

        config.PreLoading = self.GetSettingV("PreLoading", config.PreLoading)
        self.preDownNum.setValue(config.PreLoading)

        x = self.settings.value("MainSize_x")
        y = self.settings.value("MainSize_y")
        if x and y:
            self.mainSize = QSize(int(x), int(y))

        x = self.settings.value("BookSize_x")
        y = self.settings.value("BookSize_y")
        if x and y:
            self.bookSize = QSize(int(x), int(y))

        x = self.settings.value("ImgRead_x")
        y = self.settings.value("ImgRead_y")
        if x and y:
            self.readSize = QSize(int(x), int(y))

        config.Encode = self.GetSettingV("Waifu2x/Encode", 0)
        self.encodeSelect.setCurrentIndex(config.Encode)

        config.LookModel = self.GetSettingV("Waifu2x/LookModel", config.LookModel)
        config.LookNoise = self.GetSettingV("Waifu2x/LookNoise", config.LookNoise)
        config.LookScale = self.GetSettingV("Waifu2x/LookScale", config.LookScale)
        self.readModel.setCurrentIndex(config.LookModel)
        self.readNoise.setCurrentIndex(config.LookNoise+1)
        self.readScale.setValue(config.LookScale)

        config.DownloadModel = self.GetSettingV("Waifu2x/DownloadModel", config.DownloadModel)
        config.DownloadNoise = self.GetSettingV("Waifu2x/DownloadNoise", config.DownloadNoise)
        config.DownloadScale = self.GetSettingV("Waifu2x/DownloadScale", config.DownloadScale)
        config.DonwloadAuto = self.GetSettingV("Waifu2x/DonwloadAuto", config.DownloadAuto)
        self.downModel.setCurrentIndex(config.DownloadModel)
        self.downNoise.setCurrentIndex(config.DownloadNoise+1)
        self.downScale.setValue(config.DownloadScale)
        self.downAuto.setChecked(config.DownloadAuto)

        config.LogIndex = self.GetSettingV("Waifu2x/LogIndex", config.LogIndex)
        self.logBox.setCurrentIndex(config.LogIndex)
        Log.UpdateLoggingLevel()

        config.IsTips = self.GetSettingV("Waifu2x/IsTips", config.IsTips)
        config.IsOpenWaifu = self.GetSettingV("Waifu2x/IsOpen2", config.IsOpenWaifu)
        self.checkBox.setChecked(config.IsOpenWaifu)

        self.userId = self.settings.value("UserId")
        self.passwd = self.settings.value("Passwd2")
        self.passwd = base64.b64decode(self.passwd).decode("utf-8") if self.passwd else self.passwd
        themId = self.GetSettingV("ThemeId", 0)
        self.themeBox.setCurrentIndex(themId)
        self.SetTheme()
        return

    def GetSettingV(self, key, defV=None):
        v = self.settings.value(key)
        if v:
            if isinstance(defV, int):
                if v == "true" or v == "True":
                    return 1
                elif v == "false" or v == "False":
                    return 0
                return int(v)
            elif isinstance(defV, float):
                return float(v)
            else:
                return v
        return defV

    def SetSettingV(self, key, val):
        self.settings.setValue(key, val)
        return

    def ExitSaveSetting(self, mainQsize, bookQsize, imgQsize, userId, passwd):
        self.settings.setValue("MainSize_x", mainQsize.width())
        self.settings.setValue("MainSize_y", mainQsize.height())
        self.settings.setValue("BookSize_x", bookQsize.width())
        self.settings.setValue("BookSize_y", bookQsize.height())
        self.settings.setValue("ImgRead_x", imgQsize.width())
        self.settings.setValue("ImgRead_y", imgQsize.height())
        self.settings.setValue("UserId", userId)
        self.settings.setValue("Passwd", base64.b64encode(passwd.encode("utf-8")))
        self.settings.setValue("Passwd2", base64.b64encode(passwd.encode("utf-8")))
        self.settings.setValue("Waifu2x/IsOpen2", int(config.IsOpenWaifu))
        self.settings.setValue("Waifu2x/IsTips", int(config.IsTips))

    def SetTheme(self):
        index = self.themeBox.currentIndex()
        if index == 0:
            QtOwner().owner.app.setPalette(QPalette())
            QtOwner().owner.app.setStyleSheet("")
            return
        elif index == 1:
            text = "flatblack"
        else:
            text = "flatwhite"
        data = QssDataMgr().GetData(text)
        QtOwner().owner.app.setPalette(QPalette(QColor(data[20:27])))
        QtOwner().owner.app.setStyleSheet(data)

    def SaveSetting(self):

        config.DownloadThreadNum = int(self.comboBox.currentText())
        config.HttpProxy = self.httpEdit.text()
        config.SavePath = self.saveEdit.text()
        config.IsHttpProxy = 1 if self.httpProxy.isChecked() else 0
        config.PreLoading = self.preDownNum.value()

        self.settings.setValue("DownloadThreadNum", config.DownloadThreadNum)
        self.settings.setValue("Proxy/Http", config.HttpProxy)
        self.settings.setValue("Proxy/IsHttp", config.IsHttpProxy)
        self.settings.setValue("SavePath", config.SavePath)
        self.settings.setValue("PreLoading", config.PreLoading)

        config.Encode = self.encodeSelect.currentIndex()
        config.Waifu2xThread = int(self.threadSelect.currentIndex()) + 1
        config.IsOpenWaifu = int(self.checkBox.isChecked())
        config.DownloadModel = int(self.downModel.currentIndex())
        config.LogIndex = int(self.logBox.currentIndex())

        self.settings.setValue("Waifu2x/DownloadModel", config.DownloadModel)
        self.settings.setValue("Waifu2x/LogIndex", config.LogIndex)
        self.settings.setValue("Waifu2x/Encode", config.Encode)
        self.settings.setValue("Waifu2x/IsOpen2", config.IsOpenWaifu)

        config.LookModel = self.readModel.currentIndex()
        config.LookNoise = self.readNoise.currentIndex()-1
        config.LookScale = self.readScale.value()
        self.SetSettingV("Waifu2x/LookModel", config.LookModel)
        self.SetSettingV("Waifu2x/LookNoise", config.LookNoise)
        self.SetSettingV("Waifu2x/LookScale", config.LookScale)

        config.DownloadModel = self.downModel.currentIndex()
        config.DownloadNoise = self.downNoise.currentIndex()-1
        config.DownloadScale = self.downScale.value()
        config.DownloadAuto = int(self.downAuto.isChecked())
        self.SetSettingV("Waifu2x/DownloadModel", config.DownloadModel)
        self.SetSettingV("Waifu2x/DownloadNoise", config.DownloadNoise)
        self.SetSettingV("Waifu2x/DownloadScale", config.DownloadScale)
        self.SetSettingV("Waifu2x/DownloadAuto", config.DownloadAuto)

        self.SetSettingV("ThemeId", self.themeBox.currentIndex())

        Log.UpdateLoggingLevel()
        # QtWidgets.QMessageBox.information(self, '保存成功', "成功", QtWidgets.QMessageBox.Yes)
        QtBubbleLabel.ShowMsgEx(self, "保存成功")
        self.LoadSetting()

    def SelectSavePath(self):
        url = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if url:
            self.saveEdit.setText(url)

    def SetGpuInfos(self, gpuInfo):
        self.gpuInfos = gpuInfo
        if config.Encode >= len(self.gpuInfos):
            config.Encode = 0

        if not self.gpuInfos:
            return
        for info in self.gpuInfos:
            self.encodeSelect.addItem(info)
        self.encodeSelect.setCurrentIndex(config.Encode)
        Log.Info("waifu2x GPU: " + str(self.gpuInfos))
        return

    def GetGpuName(self):
        index = config.Encode
        if index >= len(self.gpuInfos) or index < 0:
            return "GPU"
        return self.gpuInfos[index]
