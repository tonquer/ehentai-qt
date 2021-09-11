# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_proxy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LoginProxy(object):
    def setupUi(self, LoginProxy):
        if not LoginProxy.objectName():
            LoginProxy.setObjectName(u"LoginProxy")
        LoginProxy.resize(455, 315)
        self.gridLayout = QGridLayout(LoginProxy)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.saveButton = QPushButton(LoginProxy)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_8.addWidget(self.saveButton)


        self.gridLayout.addLayout(self.horizontalLayout_8, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.proxyBox = QCheckBox(LoginProxy)
        self.proxyBox.setObjectName(u"proxyBox")

        self.horizontalLayout.addWidget(self.proxyBox)

        self.line = QFrame(LoginProxy)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label = QLabel(LoginProxy)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.httpLine = QLineEdit(LoginProxy)
        self.httpLine.setObjectName(u"httpLine")

        self.horizontalLayout.addWidget(self.httpLine)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.host_1 = QLabel(LoginProxy)
        self.host_1.setObjectName(u"host_1")
        self.host_1.setIndent(20)

        self.gridLayout_2.addWidget(self.host_1, 2, 0, 1, 1)

        self.boxLabel_1 = QLabel(LoginProxy)
        self.boxLabel_1.setObjectName(u"boxLabel_1")

        self.gridLayout_2.addWidget(self.boxLabel_1, 2, 2, 1, 1)

        self.host_2 = QLabel(LoginProxy)
        self.host_2.setObjectName(u"host_2")
        self.host_2.setIndent(20)

        self.gridLayout_2.addWidget(self.host_2, 3, 0, 1, 1)

        self.radioButton_1 = QRadioButton(LoginProxy)
        self.buttonGroup = QButtonGroup(LoginProxy)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_1)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_1, 0, 0, 1, 1)

        self.host_3 = QLabel(LoginProxy)
        self.host_3.setObjectName(u"host_3")
        self.host_3.setIndent(20)

        self.gridLayout_2.addWidget(self.host_3, 4, 0, 1, 1)

        self.host_4 = QLabel(LoginProxy)
        self.host_4.setObjectName(u"host_4")
        self.host_4.setIndent(20)

        self.gridLayout_2.addWidget(self.host_4, 5, 0, 1, 1)

        self.radioButton_2 = QRadioButton(LoginProxy)
        self.buttonGroup.addButton(self.radioButton_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_2.addWidget(self.radioButton_2, 1, 0, 1, 1)

        self.comboBox_1 = QComboBox(LoginProxy)
        self.comboBox_1.setObjectName(u"comboBox_1")
        self.comboBox_1.setEditable(True)

        self.gridLayout_2.addWidget(self.comboBox_1, 2, 1, 1, 1)

        self.host_5 = QLabel(LoginProxy)
        self.host_5.setObjectName(u"host_5")
        self.host_5.setIndent(20)

        self.gridLayout_2.addWidget(self.host_5, 6, 0, 1, 1)

        self.comboBox_2 = QComboBox(LoginProxy)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setEditable(True)

        self.gridLayout_2.addWidget(self.comboBox_2, 3, 1, 1, 1)

        self.comboBox_3 = QComboBox(LoginProxy)
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setEditable(True)

        self.gridLayout_2.addWidget(self.comboBox_3, 4, 1, 1, 1)

        self.comboBox_4 = QComboBox(LoginProxy)
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setEditable(True)

        self.gridLayout_2.addWidget(self.comboBox_4, 5, 1, 1, 1)

        self.comboBox_5 = QComboBox(LoginProxy)
        self.comboBox_5.setObjectName(u"comboBox_5")
        self.comboBox_5.setEditable(True)

        self.gridLayout_2.addWidget(self.comboBox_5, 6, 1, 1, 1)

        self.boxLabel_2 = QLabel(LoginProxy)
        self.boxLabel_2.setObjectName(u"boxLabel_2")

        self.gridLayout_2.addWidget(self.boxLabel_2, 3, 2, 1, 1)

        self.boxLabel_3 = QLabel(LoginProxy)
        self.boxLabel_3.setObjectName(u"boxLabel_3")

        self.gridLayout_2.addWidget(self.boxLabel_3, 4, 2, 1, 1)

        self.boxLabel_4 = QLabel(LoginProxy)
        self.boxLabel_4.setObjectName(u"boxLabel_4")

        self.gridLayout_2.addWidget(self.boxLabel_4, 5, 2, 1, 1)

        self.boxLabel_5 = QLabel(LoginProxy)
        self.boxLabel_5.setObjectName(u"boxLabel_5")

        self.gridLayout_2.addWidget(self.boxLabel_5, 6, 2, 1, 1)

        self.testDoHButton = QPushButton(LoginProxy)
        self.testDoHButton.setObjectName(u"testDoHButton")

        self.gridLayout_2.addWidget(self.testDoHButton, 1, 1, 1, 1)

        self.pushButton = QPushButton(LoginProxy)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 1, 2, 1, 1)

        self.boxLabel_0 = QLabel(LoginProxy)
        self.boxLabel_0.setObjectName(u"boxLabel_0")

        self.gridLayout_2.addWidget(self.boxLabel_0, 0, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)


        self.retranslateUi(LoginProxy)
        self.saveButton.clicked.connect(LoginProxy.SaveSetting)
        self.pushButton.clicked.connect(LoginProxy.SpeedTest)
        self.testDoHButton.clicked.connect(LoginProxy.StartDoh)

        QMetaObject.connectSlotsByName(LoginProxy)
    # setupUi

    def retranslateUi(self, LoginProxy):
        LoginProxy.setWindowTitle(QCoreApplication.translate("LoginProxy", u"\u4ee3\u7406\u8bbe\u7f6e", None))
        self.saveButton.setText(QCoreApplication.translate("LoginProxy", u"\u4fdd\u5b58", None))
        self.proxyBox.setText(QCoreApplication.translate("LoginProxy", u"\u542f\u7528\u4ee3\u7406", None))
        self.label.setText(QCoreApplication.translate("LoginProxy", u"\u4ee3\u7406\u5730\u5740", None))
        self.host_1.setText(QCoreApplication.translate("LoginProxy", u"e-hentai.org", None))
        self.boxLabel_1.setText("")
        self.host_2.setText(QCoreApplication.translate("LoginProxy", u"ehgt.org", None))
        self.radioButton_1.setText(QCoreApplication.translate("LoginProxy", u"\u9ed8\u8ba4", None))
        self.host_3.setText(QCoreApplication.translate("LoginProxy", u"api.e-hentai.org", None))
        self.host_4.setText(QCoreApplication.translate("LoginProxy", u"exhentai.org", None))
        self.radioButton_2.setText(QCoreApplication.translate("LoginProxy", u"\u81ea\u5b9a\u4e49HOST", None))
        self.host_5.setText(QCoreApplication.translate("LoginProxy", u"api.exhentai.org", None))
        self.boxLabel_2.setText("")
        self.boxLabel_3.setText("")
        self.boxLabel_4.setText("")
        self.boxLabel_5.setText("")
        self.testDoHButton.setText(QCoreApplication.translate("LoginProxy", u"\u4f7f\u7528DoH\u83b7\u53d6Host", None))
        self.pushButton.setText(QCoreApplication.translate("LoginProxy", u"Ping", None))
        self.boxLabel_0.setText("")
    # retranslateUi

