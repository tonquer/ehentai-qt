# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_favorite_info.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_FavoriteInfo(object):
    def setupUi(self, FavoriteInfo):
        if not FavoriteInfo.objectName():
            FavoriteInfo.setObjectName(u"FavoriteInfo")
        FavoriteInfo.resize(542, 500)
        FavoriteInfo.setMinimumSize(QSize(400, 500))
        self.gridLayout_2 = QGridLayout(FavoriteInfo)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.comboBox = QComboBox(FavoriteInfo)
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

        self.lineEdit = QLineEdit(FavoriteInfo)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(0, 350))

        self.gridLayout_2.addWidget(self.lineEdit, 1, 0, 1, 1)

        self.nameLabel = QLabel(FavoriteInfo)
        self.nameLabel.setObjectName(u"nameLabel")

        self.gridLayout_2.addWidget(self.nameLabel, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(FavoriteInfo)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(FavoriteInfo)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 0, 1, 1)


        self.retranslateUi(FavoriteInfo)
        self.pushButton.clicked.connect(FavoriteInfo.SaveFavorite)

        QMetaObject.connectSlotsByName(FavoriteInfo)
    # setupUi

    def retranslateUi(self, FavoriteInfo):
        FavoriteInfo.setWindowTitle(QCoreApplication.translate("FavoriteInfo", u"Form", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59390", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59391", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59392", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59393", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59394", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59395", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59396", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59397", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59398", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("FavoriteInfo", u"\u6536\u85cf\u59399", None))

        self.nameLabel.setText(QCoreApplication.translate("FavoriteInfo", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("FavoriteInfo", u"\u4fdd\u5b58", None))
        self.pushButton_2.setText(QCoreApplication.translate("FavoriteInfo", u"\u53d6\u6d88", None))
    # retranslateUi

