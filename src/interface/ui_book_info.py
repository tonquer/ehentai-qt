# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_book_info.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from component.scroll_area.smooth_scroll_area import SmoothScrollArea
from component.list.tag_list_widget import TagListWidget
from component.button.icon_tool_button import IconToolButton

import images_rc

class Ui_BookInfo(object):
    def setupUi(self, BookInfo):
        if not BookInfo.objectName():
            BookInfo.setObjectName(u"BookInfo")
        BookInfo.resize(838, 724)
        BookInfo.setStyleSheet(u"QToolButton\n"
"{\n"
"background-color:transparent;\n"
"  border: 0px;\n"
"  height: 0px;\n"
"  margin: 0px;\n"
"  padding: 0px;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"QToolButton:hover  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"\n"
"QToolButton:pressed  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"\n"
"QToolButton:checked  {\n"
"background-color:transparent;\n"
"  border-right: 0px;\n"
"  border-left: 0px;\n"
"}\n"
"QListWidget {background-color:transparent;}\n"
"QScrollArea {background-color:transparent;}")
        self.gridLayout_2 = QGridLayout(BookInfo)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = SmoothScrollArea(BookInfo)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 818, 704))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.picture = QLabel(self.scrollAreaWidgetContents)
        self.picture.setObjectName(u"picture")
        self.picture.setMinimumSize(QSize(300, 400))

        self.horizontalLayout.addWidget(self.picture)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(60, 0))
        self.label_4.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_4.addWidget(self.label_4)

        self.idLabel = QLabel(self.scrollAreaWidgetContents)
        self.idLabel.setObjectName(u"idLabel")
        self.idLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.horizontalLayout_4.addWidget(self.idLabel)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 0))
        self.label.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_3.addWidget(self.label)

        self.title = QLabel(self.scrollAreaWidgetContents)
        self.title.setObjectName(u"title")
        self.title.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.horizontalLayout_3.addWidget(self.title)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(60, 0))
        self.label_3.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_7.addWidget(self.label_3)

        self.categoryList = TagListWidget(self.scrollAreaWidgetContents)
        self.categoryList.setObjectName(u"categoryList")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoryList.sizePolicy().hasHeightForWidth())
        self.categoryList.setSizePolicy(sizePolicy)
        self.categoryList.setMaximumSize(QSize(16777215, 40))
        self.categoryList.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
"QListWidget::item {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"    border-radius: 10px;\n"
"	border-color:rgb(196, 95, 125);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QListWidget::item:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"")
        self.categoryList.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_7.addWidget(self.categoryList)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(60, 0))
        self.label_2.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_5.addWidget(self.label_2)

        self.lanLabel = QLabel(self.scrollAreaWidgetContents)
        self.lanLabel.setObjectName(u"lanLabel")
        self.lanLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.horizontalLayout_5.addWidget(self.lanLabel)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(60, 0))
        self.label_6.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_8.addWidget(self.label_6)

        self.pageLabel = QLabel(self.scrollAreaWidgetContents)
        self.pageLabel.setObjectName(u"pageLabel")
        self.pageLabel.setMaximumSize(QSize(16777215, 20))
        self.pageLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.horizontalLayout_8.addWidget(self.pageLabel)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_13 = QLabel(self.scrollAreaWidgetContents)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(60, 0))
        self.label_13.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_11.addWidget(self.label_13)

        self.favoriteLabel = QLabel(self.scrollAreaWidgetContents)
        self.favoriteLabel.setObjectName(u"favoriteLabel")
        self.favoriteLabel.setMaximumSize(QSize(16777215, 20))
        self.favoriteLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.horizontalLayout_11.addWidget(self.favoriteLabel)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)


        self.horizontalLayout.addLayout(self.verticalLayout_6)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.updateTick = QLabel(self.scrollAreaWidgetContents)
        self.updateTick.setObjectName(u"updateTick")
        self.updateTick.setEnabled(True)
        self.updateTick.setMinimumSize(QSize(80, 0))
        self.updateTick.setMaximumSize(QSize(160, 20))

        self.horizontalLayout_2.addWidget(self.updateTick)

        self.favoriteButton = IconToolButton(self.scrollAreaWidgetContents)
        self.favoriteButton.setObjectName(u"favoriteButton")
        self.favoriteButton.setMinimumSize(QSize(40, 40))
        self.favoriteButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.favoriteButton.setStyleSheet(u"background-color:transparent;")
        icon = QIcon()
        icon.addFile(u":/png/icon/icon_like_off.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/png/icon/icon_bookmark_on.png", QSize(), QIcon.Selected, QIcon.On)
        self.favoriteButton.setIcon(icon)
        self.favoriteButton.setIconSize(QSize(50, 50))
        self.favoriteButton.setCheckable(False)

        self.horizontalLayout_2.addWidget(self.favoriteButton)

        self.commentButton = IconToolButton(self.scrollAreaWidgetContents)
        self.commentButton.setObjectName(u"commentButton")
        self.commentButton.setMinimumSize(QSize(40, 40))
        self.commentButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.commentButton.setStyleSheet(u"background-color:transparent;")
        icon1 = QIcon()
        icon1.addFile(u":/png/icon/icon_comment.png", QSize(), QIcon.Normal, QIcon.Off)
        self.commentButton.setIcon(icon1)
        self.commentButton.setIconSize(QSize(50, 50))
        self.commentButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.commentButton)

        self.downloadButton = IconToolButton(self.scrollAreaWidgetContents)
        self.downloadButton.setObjectName(u"downloadButton")
        self.downloadButton.setMinimumSize(QSize(40, 40))
        self.downloadButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.downloadButton.setStyleSheet(u"background-color:transparent;")
        icon2 = QIcon()
        icon2.addFile(u":/png/icon/ic_get_app_black_36dp.png", QSize(), QIcon.Normal, QIcon.Off)
        self.downloadButton.setIcon(icon2)
        self.downloadButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_2.addWidget(self.downloadButton)

        self.startRead = QPushButton(self.scrollAreaWidgetContents)
        self.startRead.setObjectName(u"startRead")
        self.startRead.setMinimumSize(QSize(0, 40))
        self.startRead.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.startRead)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_2)


        self.gridLayout_3.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.tagScrollArea = QScrollArea(self.scrollAreaWidgetContents)
        self.tagScrollArea.setObjectName(u"tagScrollArea")
        self.tagScrollArea.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"    border-radius: 10px;\n"
"	border-color:rgb(196, 95, 125);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QPushButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}")
        self.tagScrollArea.setWidgetResizable(True)
        self.tagWidgetContents = QWidget()
        self.tagWidgetContents.setObjectName(u"tagWidgetContents")
        self.tagWidgetContents.setGeometry(QRect(0, 0, 798, 224))
        self.verticalLayout = QVBoxLayout(self.tagWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tagScrollArea.setWidget(self.tagWidgetContents)

        self.verticalLayout_3.addWidget(self.tagScrollArea)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(BookInfo)
        self.favoriteButton.clicked.connect(BookInfo.AddFavorite)
        self.downloadButton.clicked.connect(BookInfo.AddDownload)
        self.startRead.clicked.connect(BookInfo.StartRead)
        self.commentButton.clicked.connect(BookInfo.OpenComment)

        QMetaObject.connectSlotsByName(BookInfo)
    # setupUi

    def retranslateUi(self, BookInfo):
        BookInfo.setWindowTitle(QCoreApplication.translate("BookInfo", u"\u6f2b\u753b\u8be6\u60c5", None))
        self.picture.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("BookInfo", u"ID:", None))
        self.idLabel.setText("")
        self.label.setText(QCoreApplication.translate("BookInfo", u"\u6807\u9898\uff1a", None))
        self.title.setText(QCoreApplication.translate("BookInfo", u"\u6807\u9898", None))
        self.label_3.setText(QCoreApplication.translate("BookInfo", u"\u5206\u7c7b\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("BookInfo", u"\u8bed\u8a00\uff1a", None))
        self.lanLabel.setText("")
        self.label_6.setText(QCoreApplication.translate("BookInfo", u"\u9875\u6570\uff1a", None))
        self.pageLabel.setText("")
        self.label_13.setText(QCoreApplication.translate("BookInfo", u"\u6536\u85cf\u6570\uff1a", None))
        self.favoriteLabel.setText("")
        self.updateTick.setText(QCoreApplication.translate("BookInfo", u"TextLabel", None))
        self.favoriteButton.setText("")
        self.commentButton.setText("")
        self.downloadButton.setText("")
        self.startRead.setText(QCoreApplication.translate("BookInfo", u"\u5f00\u59cb\u9605\u8bfb", None))
    # retranslateUi

