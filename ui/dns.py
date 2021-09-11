# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dns.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dns(object):
    def setupUi(self, Dns):
        if not Dns.objectName():
            Dns.setObjectName(u"Dns")
        Dns.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dns)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(Dns)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(Dns)

        QMetaObject.connectSlotsByName(Dns)
    # setupUi

    def retranslateUi(self, Dns):
        Dns.setWindowTitle(QCoreApplication.translate("Dns", u"Doh DNS", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dns", u"Host", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dns", u"IP", None));
    # retranslateUi

