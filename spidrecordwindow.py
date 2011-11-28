#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui.ui_recordwindow import Ui_SPIDRecordWindow

class SPIDRecordWindow(QtGui.QDialog, Ui_SPIDRecordWindow):
    def __init__(self, parent=None, id_=None):
        QtGui.QDialog.__init__(self, parent)

        self.timeLeft = 5

        self.setupUi(self)

        self.labelRecordCountdown.setText("Recording will start in %d seconds" % self.timeLeft)
