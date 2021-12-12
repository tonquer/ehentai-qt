# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_line_edit_help_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LineEditHelp(object):
    def setupUi(self, LineEditHelp):
        if not LineEditHelp.objectName():
            LineEditHelp.setObjectName(u"LineEditHelp")
        LineEditHelp.resize(400, 440)
        self.verticalLayout_2 = QVBoxLayout(LineEditHelp)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(LineEditHelp)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.listView = QListView(LineEditHelp)
        self.listView.setObjectName(u"listView")
        self.listView.setMinimumSize(QSize(0, 120))

        self.verticalLayout_2.addWidget(self.listView)


        self.retranslateUi(LineEditHelp)

        QMetaObject.connectSlotsByName(LineEditHelp)
    # setupUi

    def retranslateUi(self, LineEditHelp):
        LineEditHelp.setWindowTitle(QCoreApplication.translate("LineEditHelp", u"Form", None))
        self.label.setText(QCoreApplication.translate("LineEditHelp", u"\u8054\u60f3\u8bcd", None))
    # retranslateUi

