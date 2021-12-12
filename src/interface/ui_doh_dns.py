# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_doh_dns.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DohDns(object):
    def setupUi(self, DohDns):
        if not DohDns.objectName():
            DohDns.setObjectName(u"DohDns")
        DohDns.resize(400, 300)
        self.verticalLayout = QVBoxLayout(DohDns)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(DohDns)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(DohDns)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(DohDns)

        QMetaObject.connectSlotsByName(DohDns)
    # setupUi

    def retranslateUi(self, DohDns):
        DohDns.setWindowTitle(QCoreApplication.translate("DohDns", u"Doh DNS", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DohDns", u"Host", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DohDns", u"IP", None));
        self.pushButton.setText(QCoreApplication.translate("DohDns", u"\u5173\u95ed", None))
    # retranslateUi

