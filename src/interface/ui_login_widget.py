# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QHBoxLayout,
    QLabel, QLineEdit, QRadioButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_LoginWidget(object):
    def setupUi(self, LoginWidget):
        if not LoginWidget.objectName():
            LoginWidget.setObjectName(u"LoginWidget")
        LoginWidget.resize(403, 334)
        self.verticalLayout_2 = QVBoxLayout(LoginWidget)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label_2 = QLabel(LoginWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_5 = QLabel(LoginWidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_2.addWidget(self.label_5)

        self.passHash = QLineEdit(LoginWidget)
        self.passHash.setObjectName(u"passHash")

        self.verticalLayout_2.addWidget(self.passHash)

        self.label_6 = QLabel(LoginWidget)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.memberId = QLineEdit(LoginWidget)
        self.memberId.setObjectName(u"memberId")
        self.memberId.setEchoMode(QLineEdit.Normal)

        self.verticalLayout_2.addWidget(self.memberId)

        self.label = QLabel(LoginWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.igneous = QLineEdit(LoginWidget)
        self.igneous.setObjectName(u"igneous")

        self.verticalLayout_2.addWidget(self.igneous)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.loginOpen = QCheckBox(LoginWidget)
        self.loginOpen.setObjectName(u"loginOpen")

        self.horizontalLayout.addWidget(self.loginOpen)

        self.autoBox = QCheckBox(LoginWidget)
        self.autoBox.setObjectName(u"autoBox")

        self.horizontalLayout.addWidget(self.autoBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label_3 = QLabel(LoginWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.eRadio = QRadioButton(LoginWidget)
        self.buttonGroup = QButtonGroup(LoginWidget)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.eRadio)
        self.eRadio.setObjectName(u"eRadio")
        self.eRadio.setChecked(True)

        self.horizontalLayout_2.addWidget(self.eRadio)

        self.exRadio = QRadioButton(LoginWidget)
        self.buttonGroup.addButton(self.exRadio)
        self.exRadio.setObjectName(u"exRadio")

        self.horizontalLayout_2.addWidget(self.exRadio)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.retranslateUi(LoginWidget)

        QMetaObject.connectSlotsByName(LoginWidget)
    # setupUi

    def retranslateUi(self, LoginWidget):
        LoginWidget.setWindowTitle(QCoreApplication.translate("LoginWidget", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("LoginWidget", u"\u8bf7\u81ea\u884c\u83b7\u53d6cookie", None))
        self.label_5.setText(QCoreApplication.translate("LoginWidget", u"ipb_pass_hash:", None))
        self.label_6.setText(QCoreApplication.translate("LoginWidget", u"ipb_member_id :", None))
        self.label.setText(QCoreApplication.translate("LoginWidget", u"igneous:", None))
        self.igneous.setPlaceholderText(QCoreApplication.translate("LoginWidget", u"\u53ef\u9009", None))
        self.loginOpen.setText(QCoreApplication.translate("LoginWidget", u"\u542f\u52a8\u540e\u6253\u5f00\u767b\u5f55", None))
        self.autoBox.setText(QCoreApplication.translate("LoginWidget", u"\u81ea\u52a8\u767b\u5f55", None))
        self.label_3.setText(QCoreApplication.translate("LoginWidget", u"\u9ed8\u8ba4\u7ad9\u70b9\u9009\u62e9:", None))
        self.eRadio.setText(QCoreApplication.translate("LoginWidget", u"e-hentai", None))
        self.exRadio.setText(QCoreApplication.translate("LoginWidget", u"exhentai", None))
    # retranslateUi

