# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_host.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPlainTextEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_LoginHostWidget(object):
    def setupUi(self, LoginHostWidget):
        if not LoginHostWidget.objectName():
            LoginHostWidget.setObjectName(u"LoginHostWidget")
        LoginHostWidget.resize(400, 272)
        self.verticalLayout = QVBoxLayout(LoginHostWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(LoginHostWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.plainTextEdit = QPlainTextEdit(LoginHostWidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout.addWidget(self.plainTextEdit)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(LoginHostWidget)

        QMetaObject.connectSlotsByName(LoginHostWidget)
    # setupUi

    def retranslateUi(self, LoginHostWidget):
        LoginHostWidget.setWindowTitle(QCoreApplication.translate("LoginHostWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("LoginHostWidget", u"\u81ea\u5b9a\u4e49IP\uff1a\u8bf7\u4f7f\u7528\u57df\u540d:IP\u7684\u683c\u5f0f", None))
    # retranslateUi

