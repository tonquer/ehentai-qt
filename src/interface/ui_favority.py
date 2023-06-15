# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_favority.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

from component.list.comic_list_widget import ComicListWidget

class Ui_Favority(object):
    def setupUi(self, Favority):
        if not Favority.objectName():
            Favority.setObjectName(u"Favority")
        Favority.resize(628, 335)
        self.gridLayout_2 = QGridLayout(Favority)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.msgLabel = QLabel(Favority)
        self.msgLabel.setObjectName(u"msgLabel")

        self.horizontalLayout.addWidget(self.msgLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.comboBox = QComboBox(Favority)
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
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.comboBox)

        self.line_2 = QFrame(Favority)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.nums = QLabel(Favority)
        self.nums.setObjectName(u"nums")
        self.nums.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.nums)

        self.line_3 = QFrame(Favority)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.jumpButton = QPushButton(Favority)
        self.jumpButton.setObjectName(u"jumpButton")
        self.jumpButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.jumpButton)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.bookList = ComicListWidget(Favority)
        self.bookList.setObjectName(u"bookList")
        self.bookList.setStyleSheet(u"QListWidget {background-color:transparent;}")

        self.gridLayout_3.addWidget(self.bookList, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Favority)
        self.jumpButton.clicked.connect(Favority.JumpPage)
        self.comboBox.currentIndexChanged.connect(Favority.JumpFavcat)

        QMetaObject.connectSlotsByName(Favority)
    # setupUi

    def retranslateUi(self, Favority):
        Favority.setWindowTitle(QCoreApplication.translate("Favority", u"\u6536\u85cf", None))
        self.msgLabel.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("Favority", u"\u5168\u90e8", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Favority", u"\u6536\u85cf0", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Favority", u"\u6536\u85cf1", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Favority", u"\u6536\u85cf2", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Favority", u"\u6536\u85cf3", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Favority", u"\u6536\u85cf4", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Favority", u"\u6536\u85cf5", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Favority", u"\u6536\u85cf6", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Favority", u"\u6536\u85cf7", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Favority", u"\u6536\u85cf8", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("Favority", u"\u6536\u85cf9", None))

        self.nums.setText(QCoreApplication.translate("Favority", u"\u6536\u85cf\u6570\uff1a", None))
        self.jumpButton.setText(QCoreApplication.translate("Favority", u"\u4e0b\u4e00\u9875", None))
#if QT_CONFIG(shortcut)
        self.jumpButton.setShortcut(QCoreApplication.translate("Favority", u"Return", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

