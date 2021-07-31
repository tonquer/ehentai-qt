# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'user.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .head_label import HeadLabel


class Ui_User(object):
    def setupUi(self, User):
        if not User.objectName():
            User.setObjectName(u"User")
        User.resize(1059, 677)
        User.setMinimumSize(QSize(0, 0))
        self.gridLayout_2 = QGridLayout(User)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.icon = HeadLabel(User)
        self.icon.setObjectName(u"icon")
        self.icon.setEnabled(True)
        self.icon.setMinimumSize(QSize(100, 100))
        self.icon.setMaximumSize(QSize(100, 100))
        self.icon.setStyleSheet(u"background: transparent;")
        self.icon.setScaledContents(True)

        self.verticalLayout.addWidget(self.icon)

        self.name = QLabel(User)
        self.name.setObjectName(u"name")
        self.name.setMaximumSize(QSize(100, 16777215))
        self.name.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.name)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.toolButton0 = QToolButton(User)
        self.buttonGroup = QButtonGroup(User)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.toolButton0)
        self.toolButton0.setObjectName(u"toolButton0")
        self.toolButton0.setMinimumSize(QSize(100, 40))
        self.toolButton0.setMaximumSize(QSize(100, 16777215))
        self.toolButton0.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover\n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton0.setCheckable(True)
        self.toolButton0.setChecked(True)

        self.verticalLayout_2.addWidget(self.toolButton0)

        self.toolButton1 = QToolButton(User)
        self.buttonGroup.addButton(self.toolButton1)
        self.toolButton1.setObjectName(u"toolButton1")
        self.toolButton1.setMinimumSize(QSize(100, 40))
        self.toolButton1.setMaximumSize(QSize(100, 16777215))
        self.toolButton1.setStyleSheet(u"/* \u6b63\u5e38\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton{\n"
"    background:transparent;\n"
"    color: rgb(0, 0, 2);\n"
"    border-style: outset;\n"
"    border-color: beige;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QToolButton:hover\n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"\n"
" /* \u6309\u94ae\u88ab\u5355\u51fb\u540e\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QToolButton:checked {\n"
"    background-color:rgb(42, 115, 175);\n"
"    border-radius: 10px;\n"
"    color: rgb(255, 255, 0);\n"
"}")
        self.toolButton1.setCheckable(True)

        self.verticalLayout_2.addWidget(self.toolButton1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.stackedWidget = QStackedWidget(User)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"#stackedWidget {border:1px solid #014F84;}")

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 1, 1, 1)


        self.retranslateUi(User)

        QMetaObject.connectSlotsByName(User)
    # setupUi

    def retranslateUi(self, User):
        User.setWindowTitle(QCoreApplication.translate("User", u"Form", None))
        self.icon.setText("")
        self.name.setText("")
        self.toolButton0.setText(QCoreApplication.translate("User", u"\u641c\u7d22", None))
        self.toolButton1.setText(QCoreApplication.translate("User", u"\u6536\u85cf", None))
    # retranslateUi

