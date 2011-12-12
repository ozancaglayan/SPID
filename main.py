#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyKDE4.phonon import Phonon

from ui.ui_mainwindow import Ui_SPIDMainWindow

from spidprogresswindow import SPIDProgressWindow
from spidrecordwindow import SPIDRecordWindow

from Marf import Marf

class SPID(QtGui.QDialog, Ui_SPIDMainWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        # Create Phonon Music Player
        self.phonon = Phonon.createPlayer(Phonon.MusicCategory)

        # Connect signals for buttons
        self.comboBoxUsers.currentIndexChanged.connect(self.reflectUserProperties)
        self.pushButtonAddSample.clicked.connect(self.slotShowRecordWindow)

        # Enable button when item clicked
        self.listWidgetEnrollments.itemClicked.connect(lambda: self.pushButtonPlay.setEnabled(True))

        # Play sample if double-clicked
        self.listWidgetEnrollments.itemDoubleClicked.connect(self.slotStartPlayback)

        # Start/Stop Playback
        self.pushButtonPlay.clicked.connect(self.slotStartPlayback)
        self.pushButtonStop.clicked.connect(self.slotStopPlayback)
        self.pushButtonTrain.clicked.connect(self.slotStartTraining)

        # Create Marf instance
        self.marf = Marf()

        # Fill user list with trained speakers
        for speaker in self.marf.get_trained_speakers():
            self.comboBoxUsers.addItem(speaker.s_name, QtCore.QVariant(speaker.s_id))

    def slotStartTraining(self):
        progressWindow = SPIDProgressWindow(self)
        progressWindow.show()
        progressWindow.labelMessage.setText(self.marf.train())
        progressWindow.hide()
        del progressWindow

    def slotStartPlayback(self, item):
        if item:
            file_path = item.text()
        else:
            file_path = self.listWidgetEnrollments.currentItem().text()

        file_path = self.marf.get_training_sample_path(unicode(file_path))

        # Set file path and start playing
        self.phonon.setCurrentSource(Phonon.MediaSource(file_path))
        self.pushButtonStop.setEnabled(True)
        self.phonon.play()

    def slotStopPlayback(self):
        self.phonon.stop()
        self.pushButtonStop.setEnabled(False)

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
