# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login.ui'
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
        Login.resize(400, 444)
        Login.setMaximumSize(QSize(400, 599))
        Login.setStyleSheet(u"*{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QDialog#Login\n"
"{\n"
"	border-radius: 5px\n"
"}\n"
"QLineEdit {\n"
"    border: none;\n"
"    padding: 5px 2px 5px 10px;\n"
"    font: 15px 'Microsoft YaHei Light';\n"
"    selection-background-color: rgb(0, 153, 188);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    background: rgb(250,250,250);\n"
"}\n"
"\n"
"QLineEdit:!focus {\n"
"    background: rgb(230,230,230);\n"
"}\n"
"\n"
"QLineEdit:hover:!focus {\n"
"    background: rgb(215,215,215);\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(Login)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(25, 25, 25, 25)
        self.label = QLabel(Login)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color:rgb(27,27,27);\n"
"font: 16pt \"Microsoft YaHei UI\";")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Login)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color:rgb(96,96,96);")
        self.label_2.setWordWrap(True)

        self.horizontalLayout.addWidget(self.label_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.switchButton = QPushButton(Login)
        self.switchButton.setObjectName(u"switchButton")
        self.switchButton.setFocusPolicy(Qt.NoFocus)
        self.switchButton.setStyleSheet(u"background-color: transparent;\n"
"color:rgb(0,66,177);\n"
"font: 9pt \"Microsoft YaHei UI\";\n"
"text-decoration: underline;")

        self.verticalLayout_3.addWidget(self.switchButton)

        self.protyButton = QPushButton(Login)
        self.protyButton.setObjectName(u"protyButton")
        self.protyButton.setFocusPolicy(Qt.NoFocus)
        self.protyButton.setStyleSheet(u"background-color: transparent;\n"
"color:rgb(0,66,177);\n"
"font: 9pt \"Microsoft YaHei UI\";\n"
"text-decoration: underline;")

        self.verticalLayout_3.addWidget(self.protyButton)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.errLabel = QLabel(Login)
        self.errLabel.setObjectName(u"errLabel")
        self.errLabel.setStyleSheet(u"color: rgb(197,5,0);")

        self.verticalLayout.addWidget(self.errLabel)

        self.stackedWidget = QStackedWidget(Login)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_5 = QVBoxLayout(self.page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.label_3 = QLabel(self.page)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_5.addWidget(self.label_3)

        self.userEdit = QLineEdit(self.page)
        self.userEdit.setObjectName(u"userEdit")

        self.verticalLayout_5.addWidget(self.userEdit)

        self.label_4 = QLabel(self.page)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_5.addWidget(self.label_4)

        self.passwdEdit = QLineEdit(self.page)
        self.passwdEdit.setObjectName(u"passwdEdit")

        self.verticalLayout_5.addWidget(self.passwdEdit)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_6 = QVBoxLayout(self.page_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, -1, 0, -1)
        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_6.addWidget(self.label_5)

        self.memberLabel = QLineEdit(self.page_2)
        self.memberLabel.setObjectName(u"memberLabel")

        self.verticalLayout_6.addWidget(self.memberLabel)

        self.label_6 = QLabel(self.page_2)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_6.addWidget(self.label_6)

        self.hashLabel = QLineEdit(self.page_2)
        self.hashLabel.setObjectName(u"hashLabel")

        self.verticalLayout_6.addWidget(self.hashLabel)

        self.label_7 = QLabel(self.page_2)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_6.addWidget(self.label_7)

        self.igneousLabel = QLineEdit(self.page_2)
        self.igneousLabel.setObjectName(u"igneousLabel")

        self.verticalLayout_6.addWidget(self.igneousLabel)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.downWidget = QWidget(Login)
        self.downWidget.setObjectName(u"downWidget")
        self.downWidget.setMinimumSize(QSize(0, 80))
        self.downWidget.setMaximumSize(QSize(16777215, 80))
        self.downWidget.setStyleSheet(u"QWidget#downWidget{\n"
"background-color: rgb(243,243,243);\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(self.downWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(25, 9, 25, -1)
        self.loginButton = QPushButton(self.downWidget)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setMaximumSize(QSize(150, 30))
        self.loginButton.setFocusPolicy(Qt.NoFocus)
        self.loginButton.setStyleSheet(u"background-color: rgb(0, 90, 158);\n"
"border-radius: 10px;\n"
"border:2px solid rgb(251,251,251);\n"
"color: rgb(251,251,251);")

        self.horizontalLayout_2.addWidget(self.loginButton)

        self.closeButton = QPushButton(self.downWidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMaximumSize(QSize(150, 30))
        self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.closeButton.setStyleSheet(u"background-color: rgb(251, 251, 251);\n"
"border-radius: 10px;\n"
"border:2px solid rgb(251,251,251);")

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.verticalLayout_2.addWidget(self.downWidget)


        self.retranslateUi(Login)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Login", u"\u7528\u6237\u767b\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("Login", u"\u8bf7\u5728\u4e0b\u65b9\u8f93\u5165\u4f60\u7684\u7528\u6237\u540d\u548c\u5bc6\u7801,\u4e5f\u53ef\u4f7f\u7528Cookie\u767b\u5f55", None))
        self.switchButton.setText(QCoreApplication.translate("Login", u"\u4f7f\u7528Cookie\u767b\u5f55", None))
        self.protyButton.setText(QCoreApplication.translate("Login", u"\u4ee3\u7406\u8bbe\u7f6e", None))
        self.errLabel.setText(QCoreApplication.translate("Login", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("Login", u"\u7528\u6237\u540d", None))
        self.label_4.setText(QCoreApplication.translate("Login", u"\u5bc6\u7801", None))
        self.label_5.setText(QCoreApplication.translate("Login", u"ipb_member_id", None))
        self.label_6.setText(QCoreApplication.translate("Login", u"ipb_pass_hash", None))
        self.label_7.setText(QCoreApplication.translate("Login", u"igneous", None))
        self.igneousLabel.setPlaceholderText(QCoreApplication.translate("Login", u"\u9009\u586b", None))
        self.loginButton.setText(QCoreApplication.translate("Login", u"\u767b\u5f55", None))
#if QT_CONFIG(shortcut)
        self.loginButton.setShortcut(QCoreApplication.translate("Login", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.closeButton.setText(QCoreApplication.translate("Login", u"\u53d6\u6d88", None))
    # retranslateUi

