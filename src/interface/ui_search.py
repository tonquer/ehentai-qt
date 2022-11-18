# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from component.list.comic_list_widget import ComicListWidget
from component.line_edit.search_line_edit import SearchLineEdit
from component.list.tag_list_widget import TagListWidget


class Ui_Search(object):
    def setupUi(self, Search):
        if not Search.objectName():
            Search.setObjectName(u"Search")
        Search.resize(740, 551)
        Search.setMinimumSize(QSize(80, 0))
        self.verticalLayout = QVBoxLayout(Search)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.searchTab = QLabel(Search)
        self.searchTab.setObjectName(u"searchTab")
        self.searchTab.setEnabled(True)
        self.searchTab.setTextInteractionFlags(Qt.TextBrowserInteraction)

        self.verticalLayout.addWidget(self.searchTab)

        self.searchWidget = QWidget(Search)
        self.searchWidget.setObjectName(u"searchWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchWidget.sizePolicy().hasHeightForWidth())
        self.searchWidget.setSizePolicy(sizePolicy)
        self.searchWidget.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.searchWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_2 = QLabel(self.searchWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(60, 0))
        self.label_2.setMaximumSize(QSize(60, 40))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit = SearchLineEdit(self.searchWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy2)
        self.lineEdit.setMinimumSize(QSize(40, 40))
        self.lineEdit.setMaximumSize(QSize(16777215, 40))
        self.lineEdit.setClearButtonEnabled(True)

        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.searchButton = QPushButton(self.searchWidget)
        self.searchButton.setObjectName(u"searchButton")
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMaximumSize(QSize(16777215, 40))

        self.horizontalLayout_2.addWidget(self.searchButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.searchWidget)

        self.tagWidget = TagListWidget(Search)
        self.tagWidget.setObjectName(u"tagWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tagWidget.sizePolicy().hasHeightForWidth())
        self.tagWidget.setSizePolicy(sizePolicy3)
        self.tagWidget.setMinimumSize(QSize(0, 40))
        self.tagWidget.setMaximumSize(QSize(16777215, 60))
        self.tagWidget.setStyleSheet(u"QListWidget {background-color:transparent;}\n"
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
        self.tagWidget.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.tagWidget)

        self.bookList = ComicListWidget(Search)
        self.bookList.setObjectName(u"bookList")

        self.verticalLayout.addWidget(self.bookList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.line_4 = QFrame(Search)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.label = QLabel(Search)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 30))
        self.label.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.label)

        self.line_5 = QFrame(Search)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.VLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_5)

        self.line_6 = QFrame(Search)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_6)

        self.jumpPage = QPushButton(Search)
        self.jumpPage.setObjectName(u"jumpPage")
        self.jumpPage.setMinimumSize(QSize(60, 30))
        self.jumpPage.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout.addWidget(self.jumpPage)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Search)

        QMetaObject.connectSlotsByName(Search)
    # setupUi

    def retranslateUi(self, Search):
        Search.setWindowTitle(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.searchTab.setText("")
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("Search", u"<html><head/><body><p>\u641c\u5bfb\u7684\u6700\u4f73\u59ff\u52bf?</p><p>\u3010\u5305\u542b\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][+]\u4eba\u59bb,\u4ec5\u663e\u793a\u5168\u5f69\u4e14\u662f\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 +\u4eba\u59bb<br/></p><p>\u3010\u6392\u9664\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c][]\u4eba\u59bb,\u663e\u793a\u5168\u5f69\u5e76\u6392\u9664\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 -\u4eba\u59bb<br/></p><p>\u3010\u6211\u90fd\u8981\u641c\u5bfb\u3011</p><p>\u641c\u5bfb\u5168\u5f69[\u7a7a\u683c]\u4eba\u59bb,\u4f1a\u663e\u793a\u6240\u6709\u5305\u542b\u5168\u5f69\u53ca\u4eba\u59bb\u7684\u672c\u672c</p><p>\u8303\u4f8b:\u5168\u5f69 \u4eba\u59bb</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("Search", u"\u641c\u7d22\uff1a", None))
        self.searchButton.setText(QCoreApplication.translate("Search", u"\u641c\u7d22", None))
        self.label.setText(QCoreApplication.translate("Search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Search", u"\u4e0b\u4e00\u9875", None))
    # retranslateUi

