# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_index.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidgetItem, QSizePolicy,
    QVBoxLayout, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Index(object):
    def setupUi(self, Index):
        if not Index.objectName():
            Index.setObjectName(u"Index")
        Index.resize(400, 300)
        Index.setStyleSheet(u"QWidget#Index{\n"
"border: 3px solid rgb(229, 229, 229);\n"
"border-radius: 15px;\n"
"}\n"
"QLabel#titleLabel {\n"
"    font: 14px 'Microsoft YaHei Light';\n"
"   border: 0px;\n"
"    /* padding: 10px 15px 10px 15px; */\n"
"}\n"
"QListWidget {\n"
"	border: 0px;\n"
"}\n"
"*{\n"
"background-color: rgb(249,249,249);\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(Index)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.titleLabel = QLabel(Index)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout_2.addWidget(self.titleLabel)

        self.bookList = ComicListWidget(Index)
        self.bookList.setObjectName(u"bookList")

        self.verticalLayout_2.addWidget(self.bookList)


        self.retranslateUi(Index)

        QMetaObject.connectSlotsByName(Index)
    # setupUi

    def retranslateUi(self, Index):
        Index.setWindowTitle(QCoreApplication.translate("Index", u"Form", None))
        self.titleLabel.setText(QCoreApplication.translate("Index", u"\u9996\u9875", None))
    # retranslateUi

