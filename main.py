#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.phonon import Phonon

from ui.ui_mainwindow import Ui_SPIDMainWindow
from spidrecordwindow import SPIDRecordWindow

from Marf import Marf
from pthread import PThread

class SPID(QtGui.QDialog, Ui_SPIDMainWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        # Create thread
        # self.playerThread = PThread(self, self.slotPlaySample)

        # Create Phonon Music Player
        self.phonon = Phonon.createPlayer(Phonon.MusicCategory)

        # Connect signals for buttons
        self.comboBoxUsers.currentIndexChanged.connect(self.reflectUserProperties)
        self.pushButtonAddSample.clicked.connect(self.slotShowRecordWindow)

        # Enable button when item clicked
        self.listWidgetEnrollments.itemClicked.connect(lambda: self.pushButtonPlay.setEnabled(True))

        # Play sample if double-clicked
        self.listWidgetEnrollments.itemDoubleClicked.connect(self.slotStartPlayback)

        #
        self.pushButtonPlay.clicked.connect(self.slotStartPlayback)
        self.pushButtonStop.clicked.connect(self.slotStopPlayback)

        # Create Marf instance
        self.marf = Marf()

        # Fill user list with trained speakers
        for speaker in self.marf.get_trained_speakers():
            self.comboBoxUsers.addItem(speaker.s_name, QtCore.QVariant(speaker.s_id))

    def slotStartPlayback(self, item):
        if item:
            file_path = item.text()
        else:
            file_path = self.listWidgetEnrollments.currentItem().text()

        self.phonon.setCurrentSource(Phonon.MediaSource(file_path))
        self.phonon.play()

    def slotStopPlayback(self):
        print "stop"

    def slotShowRecordWindow(self):
        recordWindow = SPIDRecordWindow(self)
        recordWindow.show()

    def reflectUserProperties(self, index):
        s_id, ok = self.comboBoxUsers.itemData(index).toInt()
        training_samples = self.marf.get_training_samples(s_id)
        self.listWidgetEnrollments.clear()
        self.pushButtonPlay.setEnabled(False)
        for sample in training_samples:
            item = QtGui.QListWidgetItem(QtGui.QIcon(":/audio-ac3.png"),
                                         sample,
                                         self.listWidgetEnrollments)

if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    QtGui.QApplication.setApplicationName("SPID")

    spid = SPID()
    spid.show()

    app.exec_()
