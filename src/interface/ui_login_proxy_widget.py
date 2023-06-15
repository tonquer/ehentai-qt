# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_login_proxy_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QVBoxLayout,
    QWidget)

from component.scroll_area.smooth_scroll_area import SmoothScrollArea

class Ui_LoginProxyWidget(object):
    def setupUi(self, LoginProxyWidget):
        if not LoginProxyWidget.objectName():
            LoginProxyWidget.setObjectName(u"LoginProxyWidget")
        LoginProxyWidget.resize(495, 483)
        LoginProxyWidget.setMinimumSize(QSize(450, 0))
        self.gridLayout = QGridLayout(LoginProxyWidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = SmoothScrollArea(LoginProxyWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -187, 458, 650))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.proxy_0 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup = QButtonGroup(LoginProxyWidget)
        self.radioProxyGroup.setObjectName(u"radioProxyGroup")
        self.radioProxyGroup.addButton(self.proxy_0)
        self.proxy_0.setObjectName(u"proxy_0")

        self.horizontalLayout_11.addWidget(self.proxy_0)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.proxy_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_1)
        self.proxy_1.setObjectName(u"proxy_1")
        self.proxy_1.setMinimumSize(QSize(90, 0))

        self.horizontalLayout.addWidget(self.proxy_1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.httpLine = QLineEdit(self.scrollAreaWidgetContents)
        self.httpLine.setObjectName(u"httpLine")

        self.horizontalLayout.addWidget(self.httpLine)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.proxy_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_2)
        self.proxy_2.setObjectName(u"proxy_2")
        self.proxy_2.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_10.addWidget(self.proxy_2)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_10.addWidget(self.line_2)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.sockEdit = QLineEdit(self.scrollAreaWidgetContents)
        self.sockEdit.setObjectName(u"sockEdit")

        self.horizontalLayout_10.addWidget(self.sockEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.proxy_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.radioProxyGroup.addButton(self.proxy_3)
        self.proxy_3.setObjectName(u"proxy_3")

        self.horizontalLayout_12.addWidget(self.proxy_3)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.httpsBox = QCheckBox(self.scrollAreaWidgetContents)
        self.httpsBox.setObjectName(u"httpsBox")
        self.httpsBox.setChecked(True)

        self.horizontalLayout_9.addWidget(self.httpsBox)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ipDirect = QCheckBox(self.scrollAreaWidgetContents)
        self.ipDirect.setObjectName(u"ipDirect")

        self.horizontalLayout_2.addWidget(self.ipDirect)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.testSpeedButton = QPushButton(self.scrollAreaWidgetContents)
        self.testSpeedButton.setObjectName(u"testSpeedButton")

        self.verticalLayout.addWidget(self.testSpeedButton)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.radio_ex_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.exGroup = QButtonGroup(LoginProxyWidget)
        self.exGroup.setObjectName(u"exGroup")
        self.exGroup.addButton(self.radio_ex_3)
        self.radio_ex_3.setObjectName(u"radio_ex_3")

        self.gridLayout_2.addWidget(self.radio_ex_3, 10, 1, 1, 1)

        self.radio_eh_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.ehGroup = QButtonGroup(LoginProxyWidget)
        self.ehGroup.setObjectName(u"ehGroup")
        self.ehGroup.addButton(self.radio_eh_3)
        self.radio_eh_3.setObjectName(u"radio_eh_3")

        self.gridLayout_2.addWidget(self.radio_eh_3, 13, 1, 1, 1)

        self.label_eh_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_eh_2.setObjectName(u"label_eh_2")

        self.gridLayout_2.addWidget(self.label_eh_2, 12, 2, 1, 1)

        self.radio_e_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.eGroup = QButtonGroup(LoginProxyWidget)
        self.eGroup.setObjectName(u"eGroup")
        self.eGroup.addButton(self.radio_e_2)
        self.radio_e_2.setObjectName(u"radio_e_2")

        self.gridLayout_2.addWidget(self.radio_e_2, 3, 1, 1, 1)

        self.label_api = QLabel(self.scrollAreaWidgetContents)
        self.label_api.setObjectName(u"label_api")

        self.gridLayout_2.addWidget(self.label_api, 5, 0, 1, 1)

        self.label_e = QLabel(self.scrollAreaWidgetContents)
        self.label_e.setObjectName(u"label_e")

        self.gridLayout_2.addWidget(self.label_e, 2, 0, 1, 1)

        self.label_exa_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_exa_1.setObjectName(u"label_exa_1")

        self.gridLayout_2.addWidget(self.label_exa_1, 14, 2, 1, 1)

        self.radio_ex_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.exGroup.addButton(self.radio_ex_1)
        self.radio_ex_1.setObjectName(u"radio_ex_1")

        self.gridLayout_2.addWidget(self.radio_ex_1, 8, 1, 1, 1)

        self.radio_api_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.apiGroup = QButtonGroup(LoginProxyWidget)
        self.apiGroup.setObjectName(u"apiGroup")
        self.apiGroup.addButton(self.radio_api_1)
        self.radio_api_1.setObjectName(u"radio_api_1")

        self.gridLayout_2.addWidget(self.radio_api_1, 5, 1, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)

        self.label_api_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_1.setObjectName(u"label_api_1")

        self.gridLayout_2.addWidget(self.label_api_1, 5, 2, 1, 1)

        self.label_exa = QLabel(self.scrollAreaWidgetContents)
        self.label_exa.setObjectName(u"label_exa")

        self.gridLayout_2.addWidget(self.label_exa, 14, 0, 1, 1)

        self.label_api_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_2.setObjectName(u"label_api_2")

        self.gridLayout_2.addWidget(self.label_api_2, 6, 2, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.radio_eh_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.ehGroup.addButton(self.radio_eh_1)
        self.radio_eh_1.setObjectName(u"radio_eh_1")

        self.gridLayout_2.addWidget(self.radio_eh_1, 11, 1, 1, 1)

        self.radio_e_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.eGroup.addButton(self.radio_e_3)
        self.radio_e_3.setObjectName(u"radio_e_3")

        self.gridLayout_2.addWidget(self.radio_e_3, 4, 1, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_6, 1, 2, 1, 1)

        self.label_eh_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_eh_1.setObjectName(u"label_eh_1")

        self.gridLayout_2.addWidget(self.label_eh_1, 11, 2, 1, 1)

        self.label_eh_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_eh_3.setObjectName(u"label_eh_3")

        self.gridLayout_2.addWidget(self.label_eh_3, 13, 2, 1, 1)

        self.radio_api_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.apiGroup.addButton(self.radio_api_2)
        self.radio_api_2.setObjectName(u"radio_api_2")

        self.gridLayout_2.addWidget(self.radio_api_2, 6, 1, 1, 1)

        self.label_e_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_e_2.setObjectName(u"label_e_2")

        self.gridLayout_2.addWidget(self.label_e_2, 3, 2, 1, 1)

        self.radio_ex_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.exGroup.addButton(self.radio_ex_2)
        self.radio_ex_2.setObjectName(u"radio_ex_2")

        self.gridLayout_2.addWidget(self.radio_ex_2, 9, 1, 1, 1)

        self.label_api_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_api_3.setObjectName(u"label_api_3")

        self.gridLayout_2.addWidget(self.label_api_3, 7, 2, 1, 1)

        self.label_eh = QLabel(self.scrollAreaWidgetContents)
        self.label_eh.setObjectName(u"label_eh")

        self.gridLayout_2.addWidget(self.label_eh, 11, 0, 1, 1)

        self.label_ex_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_ex_1.setObjectName(u"label_ex_1")

        self.gridLayout_2.addWidget(self.label_ex_1, 8, 2, 1, 1)

        self.label_e_1 = QLabel(self.scrollAreaWidgetContents)
        self.label_e_1.setObjectName(u"label_e_1")

        self.gridLayout_2.addWidget(self.label_e_1, 2, 2, 1, 1)

        self.label_e_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_e_3.setObjectName(u"label_e_3")

        self.gridLayout_2.addWidget(self.label_e_3, 4, 2, 1, 1)

        self.label_ex_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_ex_2.setObjectName(u"label_ex_2")

        self.gridLayout_2.addWidget(self.label_ex_2, 9, 2, 1, 1)

        self.label_ex = QLabel(self.scrollAreaWidgetContents)
        self.label_ex.setObjectName(u"label_ex")

        self.gridLayout_2.addWidget(self.label_ex, 8, 0, 1, 1)

        self.radio_e_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.eGroup.addButton(self.radio_e_1)
        self.radio_e_1.setObjectName(u"radio_e_1")
        self.radio_e_1.setChecked(True)

        self.gridLayout_2.addWidget(self.radio_e_1, 2, 1, 1, 1)

        self.radio_api_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.apiGroup.addButton(self.radio_api_3)
        self.radio_api_3.setObjectName(u"radio_api_3")

        self.gridLayout_2.addWidget(self.radio_api_3, 7, 1, 1, 1)

        self.radio_eh_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.ehGroup.addButton(self.radio_eh_2)
        self.radio_eh_2.setObjectName(u"radio_eh_2")

        self.gridLayout_2.addWidget(self.radio_eh_2, 12, 1, 1, 1)

        self.label_exa_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_exa_3.setObjectName(u"label_exa_3")

        self.gridLayout_2.addWidget(self.label_exa_3, 16, 2, 1, 1)

        self.label_ex_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_ex_3.setObjectName(u"label_ex_3")

        self.gridLayout_2.addWidget(self.label_ex_3, 10, 2, 1, 1)

        self.label_exa_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_exa_2.setObjectName(u"label_exa_2")

        self.gridLayout_2.addWidget(self.label_exa_2, 15, 2, 1, 1)

        self.radio_exa_1 = QRadioButton(self.scrollAreaWidgetContents)
        self.exaGroup = QButtonGroup(LoginProxyWidget)
        self.exaGroup.setObjectName(u"exaGroup")
        self.exaGroup.addButton(self.radio_exa_1)
        self.radio_exa_1.setObjectName(u"radio_exa_1")

        self.gridLayout_2.addWidget(self.radio_exa_1, 14, 1, 1, 1)

        self.radio_exa_2 = QRadioButton(self.scrollAreaWidgetContents)
        self.exaGroup.addButton(self.radio_exa_2)
        self.radio_exa_2.setObjectName(u"radio_exa_2")

        self.gridLayout_2.addWidget(self.radio_exa_2, 15, 1, 1, 1)

        self.radio_exa_3 = QRadioButton(self.scrollAreaWidgetContents)
        self.exaGroup.addButton(self.radio_exa_3)
        self.radio_exa_3.setObjectName(u"radio_exa_3")

        self.gridLayout_2.addWidget(self.radio_exa_3, 16, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")

        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(LoginProxyWidget)
        self.testSpeedButton.clicked.connect(LoginProxyWidget.SpeedTest)

        QMetaObject.connectSlotsByName(LoginProxyWidget)
    # setupUi

    def retranslateUi(self, LoginProxyWidget):
        LoginProxyWidget.setWindowTitle(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u8bbe\u7f6e", None))
        self.proxy_0.setText(QCoreApplication.translate("LoginProxyWidget", u"\u65e0\u4ee3\u7406", None))
        self.proxy_1.setText(QCoreApplication.translate("LoginProxyWidget", u"HTTP\u4ee3\u7406", None))
        self.label.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.httpLine.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"http://127.0.0.1:10809", None))
#endif // QT_CONFIG(tooltip)
        self.httpLine.setPlaceholderText("")
        self.proxy_2.setText(QCoreApplication.translate("LoginProxyWidget", u"Sock5\u4ee3\u7406", None))
        self.label_5.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4ee3\u7406\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.sockEdit.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"127.0.0.1:10808", None))
#endif // QT_CONFIG(tooltip)
        self.sockEdit.setPlaceholderText("")
        self.proxy_3.setText(QCoreApplication.translate("LoginProxyWidget", u"\u4f7f\u7528\u7cfb\u7edf\u4ee3\u7406", None))
        self.httpsBox.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528Https\uff08\u5982\u679c\u51fa\u73b0\u8fde\u63a5\u88ab\u91cd\u7f6e\uff0c\u5efa\u8bae\u5173\u95ed\u8bd5\u8bd5\uff09", None))
        self.ipDirect.setText(QCoreApplication.translate("LoginProxyWidget", u"\u542f\u7528IP\u76f4\u8fde\uff08\u6709\u4ee3\u7406\u53ef\u5173\u95ed\u6b64\u529f\u80fd\uff09", None))
        self.testSpeedButton.setText(QCoreApplication.translate("LoginProxyWidget", u"\u6d4b\u901f", None))
        self.radio_ex_3.setText(QCoreApplication.translate("LoginProxyWidget", u"178.175.128.252", None))
        self.radio_eh_3.setText(QCoreApplication.translate("LoginProxyWidget", u"178.162.139.24", None))
        self.label_eh_2.setText("")
        self.radio_e_2.setText(QCoreApplication.translate("LoginProxyWidget", u"104.20.135.21", None))
        self.label_api.setText(QCoreApplication.translate("LoginProxyWidget", u"api.e-hentai.org", None))
        self.label_e.setText(QCoreApplication.translate("LoginProxyWidget", u"e-hentai.org", None))
        self.label_exa_1.setText("")
        self.radio_ex_1.setText(QCoreApplication.translate("LoginProxyWidget", u"178.175.129.252", None))
#if QT_CONFIG(tooltip)
        self.radio_api_1.setToolTip(QCoreApplication.translate("LoginProxyWidget", u"\u6240\u4ee5\u5206\u6d41\u4e0d\u53ef\u4f7f\u7528\u65f6\uff0c\u81ea\u52a8\u89e3\u9501", None))
#endif // QT_CONFIG(tooltip)
        self.radio_api_1.setText(QCoreApplication.translate("LoginProxyWidget", u"37.48.89.16", None))
        self.label_2.setText(QCoreApplication.translate("LoginProxyWidget", u"IP", None))
        self.label_api_1.setText("")
        self.label_exa.setText(QCoreApplication.translate("LoginProxyWidget", u"s.exhentai.org", None))
        self.label_api_2.setText("")
        self.label_3.setText(QCoreApplication.translate("LoginProxyWidget", u"IP\u76f4\u8fde\u914d\u7f6e", None))
        self.radio_eh_1.setText(QCoreApplication.translate("LoginProxyWidget", u"37.48.89.44", None))
        self.radio_e_3.setText(QCoreApplication.translate("LoginProxyWidget", u"172.67.0.127", None))
        self.label_6.setText(QCoreApplication.translate("LoginProxyWidget", u"\u5ef6\u8fdf", None))
        self.label_eh_1.setText("")
        self.label_eh_3.setText("")
        self.radio_api_2.setText(QCoreApplication.translate("LoginProxyWidget", u"178.162.147.246", None))
        self.label_e_2.setText("")
        self.radio_ex_2.setText(QCoreApplication.translate("LoginProxyWidget", u"178.175.132.20", None))
        self.label_api_3.setText("")
        self.label_eh.setText(QCoreApplication.translate("LoginProxyWidget", u"ehgt.org", None))
        self.label_ex_1.setText("")
        self.label_e_1.setText("")
        self.label_e_3.setText("")
        self.label_ex_2.setText("")
        self.label_ex.setText(QCoreApplication.translate("LoginProxyWidget", u"exhentai.org", None))
        self.radio_e_1.setText(QCoreApplication.translate("LoginProxyWidget", u"104.20.134.21", None))
        self.radio_api_3.setText(QCoreApplication.translate("LoginProxyWidget", u"81.171.10.55", None))
        self.radio_eh_2.setText(QCoreApplication.translate("LoginProxyWidget", u"81.171.10.48", None))
        self.label_exa_3.setText("")
        self.label_ex_3.setText("")
        self.label_exa_2.setText("")
        self.radio_exa_1.setText(QCoreApplication.translate("LoginProxyWidget", u"178.175.129.254", None))
        self.radio_exa_2.setText(QCoreApplication.translate("LoginProxyWidget", u"178.175.132.22", None))
        self.radio_exa_3.setText(QCoreApplication.translate("LoginProxyWidget", u"178.175.128.254", None))
    # retranslateUi

