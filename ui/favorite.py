# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'favorite.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .qtlistwidget import QtBookList


class Ui_favorite(object):
    def setupUi(self, favorite):
        if not favorite.objectName():
            favorite.setObjectName(u"favorite")
        favorite.resize(628, 335)
        self.gridLayout_2 = QGridLayout(favorite)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgLabel = QLabel(favorite)
        self.msgLabel.setObjectName(u"msgLabel")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboBox = QComboBox(favorite)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.line_2 = QFrame(favorite)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(favorite)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(favorite)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.line = QFrame(favorite)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.line_4 = QFrame(favorite)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.spinBox = QSpinBox(favorite)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(favorite)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(favorite)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = QtBookList(favorite)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(favorite)
        self.jumpButton.clicked.connect(favorite.JumpPage)
        self.comboBox.currentIndexChanged.connect(favorite.JumpFavcat)

        QMetaObject.connectSlotsByName(favorite)
    # setupUi

    def retranslateUi(self, favorite):
        favorite.setWindowTitle(QCoreApplication.translate("favorite", u"Form", None))
        self.msgLabel.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("favorite", u"\u5168\u90e8", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("favorite", u"\u6536\u85cf0", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("favorite", u"\u6536\u85cf1", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("favorite", u"\u6536\u85cf2", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("favorite", u"\u6536\u85cf3", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("favorite", u"\u6536\u85cf4", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("favorite", u"\u6536\u85cf5", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("favorite", u"\u6536\u85cf6", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("favorite", u"\u6536\u85cf7", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("favorite", u"\u6536\u85cf8", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("favorite", u"\u6536\u85cf9", None))

        self.nums.setText(QCoreApplication.translate("favorite", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("favorite", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("favorite", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("favorite", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

