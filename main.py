#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui.ui_mainwindow import Ui_SPIDMainWindow

#from ehrnewrecordwindow import SPIDNewRecordWindow
#from ehrsearchrecordwindow import SPIDSearchRecordWindow

class SPID(QtGui.QDialog, Ui_SPIDMainWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        # Connect signals for buttons
        #self.pushButtonNewRecord.clicked.connect(self.createNewRecordWindow)
        #self.pushButtonSearchRecord.clicked.connect(self.createNewSearchWindow)
        #self.pushButtonExit.clicked.connect(QtGui.qApp.quit)

    """
    def createNewRecordWindow(self):
        self.newRecordWindow = SPIDNewRecordWindow(self)

        self.newRecordWindow.kactionselectorDrugs.availableListWidget().addItems(self.drugs)
        self.newRecordWindow.kactionselectorICD.availableListWidget().addItems(sorted(self.icd10))

        self.newRecordWindow.show()

    def createNewSearchWindow(self):
        self.searchRecordWindow = SPIDSearchRecordWindow(self)
        self.searchRecordWindow.show()
    """


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)

    spid = SPID()
    spid.show()

    app.exec_()
