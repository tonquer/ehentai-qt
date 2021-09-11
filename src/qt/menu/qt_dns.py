from PySide2 import QtWidgets

from src.qt.util.qt_domain import QtDomainMgr
from ui.dns import Ui_Dns, Qt, QTableWidgetItem


class QtDns(QtWidgets.QWidget, Ui_Dns):
    def __init__(self, owner):
        super(self.__class__, self).__init__()
        Ui_Dns.__init__(self)
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

    def show(self):
        self.LoadDns()
        return super(self.__class__, self).show()

    def LoadDns(self):
        for row in range(0, self.tableWidget.rowCount()):
            row = self.tableWidget.rowCount()
            self.tableWidget.removeRow(row-1)

        row = 0
        for host, ip in QtDomainMgr().cache_dns.items():
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(host))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(ip))
            row += 1

        for host in QtDomainMgr().fail_dns:
            if host in QtDomainMgr().cache_dns:
                continue
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(host))
            self.tableWidget.setItem(row, 1, QTableWidgetItem("Fail"))
            row += 1
        return