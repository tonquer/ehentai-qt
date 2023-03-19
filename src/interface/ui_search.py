# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_search.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLayout, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

from component.line_edit.search_line_edit import SearchLineEdit
from component.list.comic_list_widget import ComicListWidget

class Ui_Search(object):
    def setupUi(self, Search):
        if not Search.objectName():
            Search.setObjectName(u"Search")
        Search.resize(765, 551)
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

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(Search)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(60, 0))
        self.label_7.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.label_7)

        self.f_sh = QCheckBox(Search)
        self.f_sh.setObjectName(u"f_sh")

        self.horizontalLayout_3.addWidget(self.f_sh)

        self.line = QFrame(Search)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.label_3 = QLabel(Search)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.f_spf = QSpinBox(Search)
        self.f_spf.setObjectName(u"f_spf")
        self.f_spf.setMaximum(9999)

        self.horizontalLayout_3.addWidget(self.f_spf)

        self.label_4 = QLabel(Search)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_3.addWidget(self.label_4)

        self.f_spt = QSpinBox(Search)
        self.f_spt.setObjectName(u"f_spt")
        self.f_spt.setMaximum(9999)

        self.horizontalLayout_3.addWidget(self.f_spt)

        self.line_2 = QFrame(Search)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_2)

        self.label_5 = QLabel(Search)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.f_srdd = QComboBox(Search)
        self.f_srdd.addItem("")
        self.f_srdd.addItem("")
        self.f_srdd.addItem("")
        self.f_srdd.addItem("")
        self.f_srdd.addItem("")
        self.f_srdd.setObjectName(u"f_srdd")

        self.horizontalLayout_3.addWidget(self.f_srdd)

        self.line_3 = QFrame(Search)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_3)

        self.label_6 = QLabel(Search)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.f_sfl = QCheckBox(Search)
        self.f_sfl.setObjectName(u"f_sfl")

        self.horizontalLayout_3.addWidget(self.f_sfl)

        self.f_sfu = QCheckBox(Search)
        self.f_sfu.setObjectName(u"f_sfu")

        self.horizontalLayout_3.addWidget(self.f_sfu)

        self.f_sft = QCheckBox(Search)
        self.f_sft.setObjectName(u"f_sft")

        self.horizontalLayout_3.addWidget(self.f_sft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(Search)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(60, 0))
        self.label_8.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_4.addWidget(self.label_8)

        self.tagList = QWidget(Search)
        self.tagList.setObjectName(u"tagList")
        self.tagList.setStyleSheet(u"\n"
"QPushButton {\n"
"    background-color:rgb(251, 239, 243);\n"
"    color: rgb(196, 95, 125);\n"
"	border:2px solid red;\n"
"    border-radius: 10px;\n"
"	border-color:rgb(196, 95, 125);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
" QPushButton:checked \n"
"{\n"
"    background-color:rgb(240, 240, 240);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"/* \u9f20\u6807\u5728\u6309\u94ae\u4e0a\u65f6\uff0c\u6309\u94ae\u989c\u8272 */\n"
"QPushButton:hover \n"
"{\n"
"    background-color:rgb(21, 85, 154);\n"
"    border-radius: 10px;\n"
"    color: rgb(0, 0, 0);\n"
"}")

        self.horizontalLayout_4.addWidget(self.tagList)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

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
        self.label_7.setText(QCoreApplication.translate("Search", u"\u9ad8\u7ea7\uff1a", None))
        self.f_sh.setText(QCoreApplication.translate("Search", u"\u663e\u793a\u5df2\u5220\u9664\u7684\u753b\u5eca", None))
        self.label_3.setText(QCoreApplication.translate("Search", u"\u9875\u6570\u8303\u56f4 \uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Search", u"-", None))
        self.label_5.setText(QCoreApplication.translate("Search", u"\u8bc4\u5206\uff1a", None))
        self.f_srdd.setItemText(0, QCoreApplication.translate("Search", u"\u65e0", None))
        self.f_srdd.setItemText(1, QCoreApplication.translate("Search", u"2\u661f", None))
        self.f_srdd.setItemText(2, QCoreApplication.translate("Search", u"3\u661f", None))
        self.f_srdd.setItemText(3, QCoreApplication.translate("Search", u"4\u661f", None))
        self.f_srdd.setItemText(4, QCoreApplication.translate("Search", u"5\u661f", None))

        self.label_6.setText(QCoreApplication.translate("Search", u"\u7981\u7528\u7b5b\u9009\uff1a", None))
        self.f_sfl.setText(QCoreApplication.translate("Search", u"\u8bed\u8a00", None))
        self.f_sfu.setText(QCoreApplication.translate("Search", u"\u4e0a\u4f20\u8005", None))
        self.f_sft.setText(QCoreApplication.translate("Search", u"\u6807\u7b7e", None))
        self.label_8.setText(QCoreApplication.translate("Search", u"\u5206\u7c7b\uff1a", None))
        self.label.setText(QCoreApplication.translate("Search", u"\u9875\uff1a0/0", None))
        self.jumpPage.setText(QCoreApplication.translate("Search", u"\u4e0b\u4e00\u9875", None))
    # retranslateUi

