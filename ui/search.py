# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .qtlistwidget import QtBookList
from .qtlistwidget import QtCategoryList
from .completelineedit import CompleteLineEdit


class Ui_search(object):
    def setupUi(self, search):
        if not search.objectName():
            search.setObjectName(u"search")
        search.resize(827, 585)
        self.gridLayout_2 = QGridLayout(search)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.searchEdit = CompleteLineEdit(search)
        self.searchEdit.setObjectName(u"searchEdit")
        self.searchEdit.setMinimumSize(QSize(0, 30))
        self.searchEdit.setMaximumSize(QSize(16777215, 30))
        self.searchEdit.setStyleSheet(u"QLineEdit {background-color:transparent;}")

        self.horizontalLayout.addWidget(self.searchEdit)

        self.searchButton = QPushButton(search)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setMinimumSize(QSize(0, 30))
        self.searchButton.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.searchButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.line_4 = QFrame(search)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.label = QLabel(search)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.label)

        self.line_5 = QFrame(search)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.spinBox = QSpinBox(search)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 0))
        self.spinBox.setStyleSheet(u"background-color:transparent;")
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_6 = QFrame(search)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_6)

        self.jumpPage = QPushButton(search)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(60, 30))
        self.jumpPage.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.bookLayout = QGridLayout()
        self.bookLayout.setObjectName(u"bookLayout")
        self.bookList = QtBookList(search)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.bookLayout.addWidget(self.bookList, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(search)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.categoryList = QtCategoryList(search)
        self.categoryList.setObjectName(u"categoryList")
        self.categoryList.setMaximumSize(QSize(16777215, 50))
        self.categoryList.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"	border-color:rgb(196, 95, 125);\n"
"	border-radius: 15px;\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QListWidget::item:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 15px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.categoryList)


        self.bookLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.bookLayout, 0, 0, 1, 1)


        self.retranslateUi(search)
        self.searchButton.clicked.connect(search.Search)
        self.jumpPage.clicked.connect(search.JumpPage)

        QMetaObject.connectSlotsByName(search)
    # setupUi

    def retranslateUi(self, search):
        search.setWindowTitle(QCoreApplication.translate("search", u"Form", None))
        self.searchButton.setText(QCoreApplication.translate("search", u"\u641c\u7d22", None))
#if QT_CONFIG(shortcut)
        self.searchButton.setShortcut(QCoreApplication.translate("search", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("search", u"\u8df3\u8f6c", None))
        self.label_2.setText(QCoreApplication.translate("search", u"\u5206\u7c7b\uff1a", None))
    # retranslateUi

