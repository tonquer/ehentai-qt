# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_favority.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from component.list.comic_list_widget import ComicListWidget


class Ui_Favority(object):
    def setupUi(self, Favority):
        if not Favority.objectName():
            Favority.setObjectName(u"Favority")
        Favority.resize(628, 335)
        self.gridLayout_2 = QGridLayout(Favority)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgLabel = QLabel(Favority)
        self.msgLabel.setObjectName(u"msgLabel")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboBox = QComboBox(Favority)
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

        self.line_2 = QFrame(Favority)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(Favority)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.pages = QLabel(Favority)
        self.pages.setObjectName(u"pages")

        self.horizontalLayout.addWidget(self.pages)

        self.line = QFrame(Favority)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.line_4 = QFrame(Favority)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.spinBox = QSpinBox(Favority)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(50, 30))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(1)

        self.horizontalLayout.addWidget(self.spinBox)

        self.line_3 = QFrame(Favority)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(Favority)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(Favority)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Favority)
        self.jumpButton.clicked.connect(Favority.JumpPage)
        self.comboBox.currentIndexChanged.connect(Favority.JumpFavcat)

        QMetaObject.connectSlotsByName(Favority)
    # setupUi

    def retranslateUi(self, Favority):
        Favority.setWindowTitle(QCoreApplication.translate("Favority", u"\u6536\u85cf", None))
        self.msgLabel.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("Favority", u"\u5168\u90e8", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Favority", u"\u6536\u85cf0", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Favority", u"\u6536\u85cf1", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Favority", u"\u6536\u85cf2", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Favority", u"\u6536\u85cf3", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Favority", u"\u6536\u85cf4", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Favority", u"\u6536\u85cf5", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Favority", u"\u6536\u85cf6", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Favority", u"\u6536\u85cf7", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Favority", u"\u6536\u85cf8", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("Favority", u"\u6536\u85cf9", None))

        self.nums.setText(QCoreApplication.translate("Favority", u"\u6536\u85cf\u6570\uff1a", None))
        self.pages.setText(QCoreApplication.translate("Favority", u"\u9875", None))
        self.jumpButton.setText(QCoreApplication.translate("Favority", u"\u8df3\u8f6c", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("Favority", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

