import weakref

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel

from conf import config
from src.qt.util.qttask import QtTask
from src.server import Server, req
from src.util.status import Status
from ui.login import Ui_Login
from PySide2 import QtWidgets


class QtLogin(QtWidgets.QWidget, Ui_Login):
    def __init__(self, owner):
        super(self.__class__, self).__init__(owner)
        Ui_Login.__init__(self)
        self.setupUi(self)
        self.owner = weakref.ref(owner)
        self.setWindowTitle("登陆")
        self.speedTest = []
        self.speedIndex = 0

    def Login(self):
        userId = self.userIdEdit.text()
        passwd = self.passwdEdit.text()
        QtTask().AddHttpTask(req.LoginReq(userId, passwd), self.LoginBack)

        self.owner().loadingForm.show()
        # self.close()
        # self.owner().show()

    def LoginBack(self, msg):
        self.owner().loadingForm.close()
        if msg == Status.Ok:
            # self.close()
            QtTask().AddHttpTask(req.HomeReq(), self.UpdateUserBack)
            self.SkipLogin()
        else:
            # QtWidgets.QMessageBox.information(self, '登陆失败', msg, QtWidgets.QMessageBox.Yes)
            self.owner().msgForm.ShowError("登陆失败, " + msg)

    def UpdateUserBack(self, msg):
        return

    def ShowUserImg(self, data, st):
        if st == Status.Ok:
            self.owner().userForm.SetPicture(data)

    def SkipLogin(self):
        self.owner().stackedWidget.setCurrentIndex(1)
        self.owner().userForm.Switch(1)
        return

    def Init(self):
        return

