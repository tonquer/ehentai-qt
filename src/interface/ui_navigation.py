# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_navigation.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

from component.button.switch_button import SwitchButton
from component.label.head_label import HeadLabel
from component.scroll_area.smooth_scroll_area import SmoothScrollArea
import images_rc

class Ui_Navigation(object):
    def setupUi(self, Navigation):
        if not Navigation.objectName():
            Navigation.setObjectName(u"Navigation")
        Navigation.resize(248, 473)
        Navigation.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(Navigation)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Navigation)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.picLabel = HeadLabel(self.widget)
        self.picLabel.setObjectName(u"picLabel")
        self.picLabel.setMinimumSize(QSize(100, 100))
        self.picLabel.setMaximumSize(QSize(100, 100))
        self.picLabel.setPixmap(QPixmap(u":/png/icon/placeholder_avatar.png"))
        self.picLabel.setScaledContents(True)

        self.verticalLayout.addWidget(self.picLabel, 0, Qt.AlignHCenter)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout.addWidget(self.pushButton, 0, Qt.AlignHCenter)

        self.swichButton = QPushButton(self.widget)
        self.swichButton.setObjectName(u"swichButton")
        sizePolicy.setHeightForWidth(self.swichButton.sizePolicy().hasHeightForWidth())
        self.swichButton.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.swichButton, 0, Qt.AlignHCenter)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.nameLabel = QLabel(self.widget)
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.nameLabel, 0, 1, 1, 1)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.limitLabel = QLabel(self.widget)
        self.limitLabel.setObjectName(u"limitLabel")
        self.limitLabel.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.limitLabel, 2, 1, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.siteLabel = QLabel(self.widget)
        self.siteLabel.setObjectName(u"siteLabel")

        self.gridLayout.addWidget(self.siteLabel, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.line_4 = QFrame(self.widget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_4.addWidget(self.label_7)

        self.offlineButton = SwitchButton(self.widget)
        self.offlineButton.setObjectName(u"offlineButton")

        self.horizontalLayout_4.addWidget(self.offlineButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.scrollArea = SmoothScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -164, 211, 424))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 9, 0, 9)
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.collectButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup = QButtonGroup(Navigation)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.collectButton)
        self.collectButton.setObjectName(u"collectButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.collectButton.sizePolicy().hasHeightForWidth())
        self.collectButton.setSizePolicy(sizePolicy1)
        self.collectButton.setMinimumSize(QSize(150, 40))
        self.collectButton.setFocusPolicy(Qt.NoFocus)
        icon = QIcon()
        icon.addFile(u":/images/menu/Contact.png", QSize(), QIcon.Normal, QIcon.Off)
        self.collectButton.setIcon(icon)
        self.collectButton.setIconSize(QSize(32, 32))
        self.collectButton.setCheckable(True)
        self.collectButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.collectButton)

        self.historyButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.historyButton)
        self.historyButton.setObjectName(u"historyButton")
        sizePolicy1.setHeightForWidth(self.historyButton.sizePolicy().hasHeightForWidth())
        self.historyButton.setSizePolicy(sizePolicy1)
        self.historyButton.setMinimumSize(QSize(150, 40))
        self.historyButton.setFocusPolicy(Qt.NoFocus)
        self.historyButton.setIcon(icon)
        self.historyButton.setIconSize(QSize(32, 32))
        self.historyButton.setCheckable(True)
        self.historyButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.historyButton)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.searchButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.searchButton)
        self.searchButton.setObjectName(u"searchButton")
        sizePolicy1.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy1)
        self.searchButton.setMinimumSize(QSize(150, 40))
        self.searchButton.setFocusPolicy(Qt.NoFocus)
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QSize(32, 32))
        self.searchButton.setCheckable(True)
        self.searchButton.setChecked(True)
        self.searchButton.setPopupMode(QToolButton.DelayedPopup)
        self.searchButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.searchButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.searchButton)

        self.rankButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.rankButton)
        self.rankButton.setObjectName(u"rankButton")
        sizePolicy1.setHeightForWidth(self.rankButton.sizePolicy().hasHeightForWidth())
        self.rankButton.setSizePolicy(sizePolicy1)
        self.rankButton.setMinimumSize(QSize(150, 40))
        self.rankButton.setFocusPolicy(Qt.NoFocus)
        self.rankButton.setIcon(icon)
        self.rankButton.setIconSize(QSize(32, 32))
        self.rankButton.setCheckable(True)
        self.rankButton.setChecked(False)
        self.rankButton.setPopupMode(QToolButton.DelayedPopup)
        self.rankButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.rankButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_3.addWidget(self.rankButton)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.downloadButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.downloadButton)
        self.downloadButton.setObjectName(u"downloadButton")
        sizePolicy1.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy1)
        self.downloadButton.setMinimumSize(QSize(150, 40))
        self.downloadButton.setFocusPolicy(Qt.NoFocus)
        self.downloadButton.setIcon(icon)
        self.downloadButton.setIconSize(QSize(32, 32))
        self.downloadButton.setCheckable(True)
        self.downloadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.downloadButton)

        self.localReadButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.localReadButton)
        self.localReadButton.setObjectName(u"localReadButton")
        sizePolicy1.setHeightForWidth(self.localReadButton.sizePolicy().hasHeightForWidth())
        self.localReadButton.setSizePolicy(sizePolicy1)
        self.localReadButton.setMinimumSize(QSize(0, 40))
        self.localReadButton.setFocusPolicy(Qt.NoFocus)
        self.localReadButton.setIcon(icon)
        self.localReadButton.setIconSize(QSize(32, 32))
        self.localReadButton.setCheckable(True)
        self.localReadButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.localReadButton)

        self.waifu2xButton = QToolButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.waifu2xButton)
        self.waifu2xButton.setObjectName(u"waifu2xButton")
        sizePolicy1.setHeightForWidth(self.waifu2xButton.sizePolicy().hasHeightForWidth())
        self.waifu2xButton.setSizePolicy(sizePolicy1)
        self.waifu2xButton.setMinimumSize(QSize(150, 40))
        self.waifu2xButton.setFocusPolicy(Qt.NoFocus)
        self.waifu2xButton.setIcon(icon)
        self.waifu2xButton.setIconSize(QSize(32, 32))
        self.waifu2xButton.setCheckable(True)
        self.waifu2xButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout_3.addWidget(self.waifu2xButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.line_3 = QFrame(self.widget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.helpButton = QToolButton(self.widget)
        self.buttonGroup.addButton(self.helpButton)
        self.helpButton.setObjectName(u"helpButton")
        sizePolicy1.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.helpButton.setSizePolicy(sizePolicy1)
        self.helpButton.setMinimumSize(QSize(0, 40))
        self.helpButton.setFocusPolicy(Qt.NoFocus)
        self.helpButton.setIcon(icon)
        self.helpButton.setIconSize(QSize(32, 32))
        self.helpButton.setCheckable(True)
        self.helpButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.verticalLayout.addWidget(self.helpButton)

        self.settingButton = QToolButton(self.widget)
        self.buttonGroup.addButton(self.settingButton)
        self.settingButton.setObjectName(u"settingButton")
        sizePolicy1.setHeightForWidth(self.settingButton.sizePolicy().hasHeightForWidth())
        self.settingButton.setSizePolicy(sizePolicy1)
        self.settingButton.setMinimumSize(QSize(150, 40))
        self.settingButton.setFocusPolicy(Qt.NoFocus)
        self.settingButton.setStyleSheet(u"")
        self.settingButton.setIcon(icon)
        self.settingButton.setIconSize(QSize(32, 32))
        self.settingButton.setCheckable(True)
        self.settingButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.settingButton.setAutoRaise(False)

        self.verticalLayout.addWidget(self.settingButton)


        self.verticalLayout_2.addWidget(self.widget)


        self.retranslateUi(Navigation)

        QMetaObject.connectSlotsByName(Navigation)
    # setupUi

    def retranslateUi(self, Navigation):
        Navigation.setWindowTitle(QCoreApplication.translate("Navigation", u"\u5bfc\u822a", None))
        self.picLabel.setText("")
        self.pushButton.setText(QCoreApplication.translate("Navigation", u"\u767b\u5f55", None))
        self.swichButton.setText(QCoreApplication.translate("Navigation", u"\u8868\u91cc\u5207\u6362", None))
        self.nameLabel.setText("")
        self.label_4.setText(QCoreApplication.translate("Navigation", u"\u8d26\u53f7\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Navigation", u"\u56fe\u7247\u9650\u5236\uff1a", None))
        self.limitLabel.setText("")
        self.label_6.setText(QCoreApplication.translate("Navigation", u"\u7ad9\u70b9\uff1a", None))
        self.siteLabel.setText(QCoreApplication.translate("Navigation", u"e-hentai", None))
        self.label_7.setText(QCoreApplication.translate("Navigation", u"\u79bb\u7ebf\u6a21\u5f0f\uff1a", None))
        self.label.setText(QCoreApplication.translate("Navigation", u"\u7528\u6237", None))
        self.collectButton.setText(QCoreApplication.translate("Navigation", u"\u6211\u7684\u6536\u85cf", None))
        self.historyButton.setText(QCoreApplication.translate("Navigation", u"\u672c\u5730\u8bb0\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("Navigation", u"\u5bfc\u822a", None))
        self.searchButton.setText(QCoreApplication.translate("Navigation", u"\u641c\u7d22", None))
        self.rankButton.setText(QCoreApplication.translate("Navigation", u"\u6392\u884c\u699c", None))
        self.label_3.setText(QCoreApplication.translate("Navigation", u"\u5176\u4ed6", None))
        self.downloadButton.setText(QCoreApplication.translate("Navigation", u"\u4e0b\u8f7d", None))
        self.localReadButton.setText(QCoreApplication.translate("Navigation", u"\u672c\u5730\u6f2b\u753b", None))
        self.waifu2xButton.setText(QCoreApplication.translate("Navigation", u"Waifu2x", None))
        self.helpButton.setText(QCoreApplication.translate("Navigation", u"\u5e2e\u52a9", None))
        self.settingButton.setText(QCoreApplication.translate("Navigation", u"\u8bbe\u7f6e", None))
    # retranslateUi

