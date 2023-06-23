import base64

from PySide6.QtCore import Signal, QTimer

from component.dialog.base_mask_dialog import BaseMaskDialog
from config.setting import Setting
from interface.ui_login import Ui_Login
from qt_owner import QtOwner
from task.qt_task import QtTaskBase
from tools.str import Str
from view.user.login_host_widget import LoginHostWidget


class LoginView(BaseMaskDialog, Ui_Login, QtTaskBase):
    CloseLogin = Signal()

    def __init__(self, parent=None, isAutoLogin=0):
        BaseMaskDialog.__init__(self, parent)
        Ui_Login.__init__(self)
        QtTaskBase.__init__(self)
        self.widget.adjustSize()
        self.setupUi(self.widget)
        self.tabWidget.currentChanged.connect(self._SwichWidget)
        self.loginButton.clicked.connect(self._ClickButton)

        self.loginWidget.passHash.setText(Setting.IpbPassHash.value)
        self.loginWidget.memberId.setText(Setting.IpbMemberId.value)
        self.loginWidget.igneous.setText(Setting.Igneous.value)

        self.closeButton.clicked.connect(self.close)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._AutoLogin)
        if isAutoLogin:
            self.timer.start()

    @property
    def loginWidget(self):
        return self.tab

    @property
    def loginProxyWidget(self):
        return self.tab_3

    @property
    def loginHostWidget(self):
        return self.tab_2

    def closeEvent(self, arg__1) -> None:
        self.timer.stop()
        return BaseMaskDialog.closeEvent(self, arg__1)

    def _AutoLogin(self):
        self.timer.stop()
        self.loginWidget.ClickButton()
        return

    def _SwichWidget(self, index):
        # self.tabWidget.widget(index).adjustSize()
        # print(self.tabWidget.widget(index).size())
        # self.tabWidget.resize(self.tabWidget.widget(index).size())
        if self.tabWidget.widget(index) == self.loginWidget:
            self.loginButton.setText(Str.GetStr(Str.Login))
        elif self.tabWidget.widget(index) == self.loginProxyWidget:
            self.loginButton.setText(Str.GetStr(Str.Save))
        elif self.tabWidget.widget(index) == self.loginHostWidget:
            self.loginButton.setText(Str.GetStr(Str.Save))
        self.tabWidget.widget(index).Init()

    def _ClickButton(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.widget(index).ClickButton()
        if self.tabWidget.widget(index) == self.loginHostWidget:
            self.loginProxyWidget.UpdateServer()

    # def event(self, event) -> bool:
    #     return BaseMaskDialog.event(event)