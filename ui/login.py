# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(528, 347)
        self.gridLayout = QGridLayout(Login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.passLabel = QLabel(Login)
        self.passLabel.setObjectName(u"passLabel")
        self.passLabel.setEnabled(False)
        self.passLabel.setMinimumSize(QSize(110, 0))
        self.passLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.horizontalLayout_7.addWidget(self.passLabel)

        self.passLine = QLineEdit(Login)
        self.passLine.setObjectName(u"passLine")
        self.passLine.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.passLine)


        self.gridLayout_2.addLayout(self.horizontalLayout_7, 8, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.memberLabel = QLabel(Login)
        self.memberLabel.setObjectName(u"memberLabel")
        self.memberLabel.setEnabled(False)
        self.memberLabel.setMinimumSize(QSize(110, 0))
        self.memberLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.horizontalLayout_5.addWidget(self.memberLabel)

        self.memberLine = QLineEdit(Login)
        self.memberLine.setObjectName(u"memberLine")
        self.memberLine.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.memberLine)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 7, 0, 1, 1)

        self.line_2 = QFrame(Login)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_2, 12, 0, 1, 1)

        self.line_3 = QFrame(Login)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_3, 10, 0, 1, 1)

        self.cookieRadio = QRadioButton(Login)
        self.buttonGroup = QButtonGroup(Login)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.cookieRadio)
        self.cookieRadio.setObjectName(u"cookieRadio")

        self.gridLayout_2.addWidget(self.cookieRadio, 6, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.loginButton = QPushButton(Login)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMinimumSize(QSize(100, 30))
        self.loginButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.loginButton)

        self.skipButton = QPushButton(Login)
        self.skipButton.setObjectName(u"skipButton")
        self.skipButton.setMinimumSize(QSize(100, 30))
        self.skipButton.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.skipButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 11, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.userLabel = QLabel(Login)
        self.userLabel.setObjectName(u"userLabel")
        self.userLabel.setMinimumSize(QSize(50, 30))
        self.userLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.userLabel)

        self.userIdEdit = QLineEdit(Login)
        self.userIdEdit.setObjectName(u"userIdEdit")
        self.userIdEdit.setMinimumSize(QSize(300, 30))

        self.horizontalLayout.addWidget(self.userIdEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.userRadio = QRadioButton(Login)
        self.buttonGroup.addButton(self.userRadio)
        self.userRadio.setObjectName(u"userRadio")
        self.userRadio.setChecked(True)

        self.horizontalLayout_4.addWidget(self.userRadio)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)

        self.line = QFrame(Login)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.passwdLabel = QLabel(Login)
        self.passwdLabel.setObjectName(u"passwdLabel")
        self.passwdLabel.setMinimumSize(QSize(50, 30))
        self.passwdLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.passwdLabel)

        self.passwdEdit = QLineEdit(Login)
        self.passwdEdit.setObjectName(u"passwdEdit")
        self.passwdEdit.setMinimumSize(QSize(300, 30))
        self.passwdEdit.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.passwdEdit)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.igneousLabel = QLabel(Login)
        self.igneousLabel.setObjectName(u"igneousLabel")
        self.igneousLabel.setEnabled(False)
        self.igneousLabel.setMinimumSize(QSize(110, 0))
        self.igneousLabel.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.horizontalLayout_6.addWidget(self.igneousLabel)

        self.igneousLine = QLineEdit(Login)
        self.igneousLine.setObjectName(u"igneousLine")
        self.igneousLine.setEnabled(False)

        self.horizontalLayout_6.addWidget(self.igneousLine)


        self.gridLayout_2.addLayout(self.horizontalLayout_6, 9, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")

        self.gridLayout_2.addLayout(self.gridLayout_4, 13, 0, 1, 1)

        self.line_4 = QFrame(Login)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_4, 5, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        QWidget.setTabOrder(self.userIdEdit, self.passwdEdit)
        QWidget.setTabOrder(self.passwdEdit, self.loginButton)
        QWidget.setTabOrder(self.loginButton, self.skipButton)

        self.retranslateUi(Login)
        self.loginButton.clicked.connect(Login.Login)
        self.skipButton.clicked.connect(Login.SkipLogin)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Form", None))
        self.passLabel.setText(QCoreApplication.translate("Login", u"ipb_pass_hash", None))
        self.memberLabel.setText(QCoreApplication.translate("Login", u"ipb_member_id", None))
        self.cookieRadio.setText(QCoreApplication.translate("Login", u"Cookie\u767b\u9646", None))
        self.loginButton.setText(QCoreApplication.translate("Login", u"\u767b\u9646", None))
#if QT_CONFIG(shortcut)
        self.loginButton.setShortcut(QCoreApplication.translate("Login", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.skipButton.setText(QCoreApplication.translate("Login", u"\u8df3\u8fc7\u767b\u5f55", None))
        self.userLabel.setText(QCoreApplication.translate("Login", u"\u5e10\u53f7", None))
        self.userIdEdit.setText("")
        self.userRadio.setText(QCoreApplication.translate("Login", u"\u5e10\u53f7\u767b\u9646", None))
        self.passwdLabel.setText(QCoreApplication.translate("Login", u"\u5bc6\u7801", None))
        self.passwdEdit.setText("")
        self.igneousLabel.setText(QCoreApplication.translate("Login", u"igneous", None))
        self.igneousLine.setPlaceholderText(QCoreApplication.translate("Login", u"\u9009\u586b", None))
    # retranslateUi

