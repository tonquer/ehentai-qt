# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_rank.ui'
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
from PySide6.QtWidgets import (QApplication, QListWidgetItem, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Rank(object):
    def setupUi(self, Rank):
        if not Rank.objectName():
            Rank.setObjectName(u"Rank")
        Rank.resize(536, 379)
        self.verticalLayout = QVBoxLayout(Rank)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Rank)
        self.tabWidget.setObjectName(u"tabWidget")
        self.widget_1 = QWidget()
        self.widget_1.setObjectName(u"widget_1")
        self.verticalLayout_2 = QVBoxLayout(self.widget_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.dayBookList = ComicListWidget(self.widget_1)
        self.dayBookList.setObjectName(u"dayBookList")

        self.verticalLayout_2.addWidget(self.dayBookList)

        self.tabWidget.addTab(self.widget_1, "")
        self.widget_2 = QWidget()
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.monthBookList = ComicListWidget(self.widget_2)
        self.monthBookList.setObjectName(u"monthBookList")

        self.verticalLayout_3.addWidget(self.monthBookList)

        self.tabWidget.addTab(self.widget_2, "")
        self.widget_3 = QWidget()
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_4 = QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.yearBookList = ComicListWidget(self.widget_3)
        self.yearBookList.setObjectName(u"yearBookList")

        self.verticalLayout_4.addWidget(self.yearBookList)

        self.tabWidget.addTab(self.widget_3, "")
        self.widget_4 = QWidget()
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_5 = QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.allBookList = ComicListWidget(self.widget_4)
        self.allBookList.setObjectName(u"allBookList")

        self.verticalLayout_5.addWidget(self.allBookList)

        self.tabWidget.addTab(self.widget_4, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Rank)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Rank)
    # setupUi

    def retranslateUi(self, Rank):
        Rank.setWindowTitle(QCoreApplication.translate("Rank", u"\u6392\u884c\u699c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_1), QCoreApplication.translate("Rank", u"\u6628\u65e5", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_2), QCoreApplication.translate("Rank", u"\u4e0a\u6708", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_3), QCoreApplication.translate("Rank", u"\u53bb\u5e74", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget_4), QCoreApplication.translate("Rank", u"\u5168\u90e8", None))
    # retranslateUi

