#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui.ui_mainwindow import Ui_SPIDMainWindow

from systemuserhelper import SystemUsers

from spidrecordwindow import SPIDRecordWindow

class SPID(QtGui.QDialog, Ui_SPIDMainWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        # Connect signals for buttons
        self.comboBoxUsers.currentIndexChanged[str].connect(self.reflectUserProperties)
        self.pushButtonRecord.clicked.connect(self.slotShowRecordWindow)

        # Create SystemUsers instance
        self.systemUsers = SystemUsers()

        # Fill user list
        for user in sorted(self.systemUsers.getUsers().keys()):
            self.comboBoxUsers.addItem(user)

    def slotShowRecordWindow(self):
        recordWindow = SPIDRecordWindow(self)
        recordWindow.show()

    def reflectUserProperties(self, text):
        userEntry = self.systemUsers.getUser(unicode(text))
        if userEntry:
            self.labelLoginName.setText(unicode(userEntry.loginName))
            self.labelRealName.setText(unicode(userEntry.realName))
            self.labelUserID.setText(unicode("%s" % userEntry.userID))

            # Enable record button
            self.pushButtonRecord.setEnabled(True)
        else:
            self.labelLoginName.clear()
            self.labelRealName.clear()
            self.labelUserID.clear()

            # Disable record button
            self.pushButtonRecord.setEnabled(False)



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
