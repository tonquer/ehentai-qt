# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'favorite_info.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Favorite_Info(object):
    def setupUi(self, Favorite_Info):
        if not Favorite_Info.objectName():
            Favorite_Info.setObjectName(u"Favorite_Info")
        Favorite_Info.resize(542, 423)
        self.gridLayout_2 = QGridLayout(Favorite_Info)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineEdit = QLineEdit(Favorite_Info)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 200))

        self.gridLayout_2.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.comboBox = QComboBox(Favorite_Info)
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

        self.gridLayout_2.addWidget(self.comboBox, 2, 0, 1, 1)

        self.pushButton = QPushButton(Favorite_Info)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 3, 0, 1, 1)

        self.nameLabel = QLabel(Favorite_Info)
        self.nameLabel.setObjectName(u"nameLabel")

        self.gridLayout_2.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 4, 0, 1, 1)


        self.retranslateUi(Favorite_Info)
        self.pushButton.clicked.connect(Favorite_Info.SaveFavorite)

        QMetaObject.connectSlotsByName(Favorite_Info)
    # setupUi

    def retranslateUi(self, Favorite_Info):
        Favorite_Info.setWindowTitle(QCoreApplication.translate("Favorite_Info", u"Form", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59390", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59391", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59392", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59393", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59394", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59395", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59396", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59397", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59398", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Favorite_Info", u"\u6536\u85cf\u59399", None))

        self.pushButton.setText(QCoreApplication.translate("Favorite_Info", u"\u4fdd\u5b58", None))
        self.nameLabel.setText(QCoreApplication.translate("Favorite_Info", u"TextLabel", None))
    # retranslateUi

