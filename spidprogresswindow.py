#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from ui.ui_progresswindow import Ui_SPIDProgressWindow

class SPIDProgressWindow(QtGui.QDialog, Ui_SPIDProgressWindow):
    def __init__(self, parent=None, id_=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)
        self.labelMessage.setText("Training...")
