#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyKDE4.phonon import Phonon

from ui.ui_mainwindow import Ui_SPIDMainWindow
from spidrecordwindow import SPIDRecordWindow
from spididentifywindow import SPIDIdentifyWindow

from Marf import Marf

import os

class SPID(QtGui.QDialog, Ui_SPIDMainWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        # Create Phonon Music Player
        self.phonon = Phonon.createPlayer(Phonon.MusicCategory)
        self.phonon.stateChanged.connect(self.slotPhononStateChanged)
        self.phonon.finished.connect(self.slotPhononPlaybackFinished)

        # Connect signals for buttons
        self.comboBoxUsers.currentIndexChanged.connect(self.reflectUserProperties)
        self.pushButtonRecordSample.clicked.connect(self.slotShowRecordWindow)

        # Enable button when item clicked
        self.listWidgetEnrollments.itemClicked.connect(lambda: self.pushButtonPlay.setEnabled(True))

        # Play sample if double-clicked
        self.listWidgetEnrollments.itemDoubleClicked.connect(self.slotStartPlayback)

        # Start/Stop Playback
        self.pushButtonPlay.clicked.connect(self.slotStartPlayback)
        self.pushButtonStop.clicked.connect(self.slotStopPlayback)
        self.pushButtonTrain.clicked.connect(self.slotShowTrainingDialog)
        self.pushButtonIdentify.clicked.connect(self.slotShowIdentifyDialog)
        self.pushButtonAddSpeaker.clicked.connect(self.slotAddSpeaker)
        self.pushButtonPlayTestingSample.clicked.connect(self.slotPlayTestingSample)
        self.lineEditNewSpeaker.textEdited.connect(self.slotCheckNewSpeaker)

        # Create Marf instance
        self.marf = Marf()

        # Fill speaker list
        self.fill_speaker_list()

    def fill_speaker_list(self):
        # Fill user list with speakers
        self.comboBoxUsers.clear()
        for speaker in self.marf.get_all_speakers():
            self.comboBoxUsers.addItem(speaker.s_name, QtCore.QVariant(speaker.s_id))

    def slotCheckNewSpeaker(self, text):
        # Enable/Disable button according to the available text
        self.pushButtonAddSpeaker.setEnabled(bool(text))

    def slotAddSpeaker(self):
        s_name = self.lineEditNewSpeaker.text()
        self.lineEditNewSpeaker.clear()

        # Add speaker to marf DB
        self.marf.add_speaker(unicode(s_name), [], [])

        # Refresh the list
        self.fill_speaker_list()
        self.comboBoxUsers.setCurrentIndex(self.comboBoxUsers.findText(s_name))

    def slotShowTrainingDialog(self):
        self.groupBox.setEnabled(False)
        QtGui.qApp.processEvents()
        self.setWindowTitle("Training...")
        QtGui.qApp.processEvents()
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        # Train
        self.marf.write_speakers()
        ret = self.marf.train()

        # Restore cursor
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QApplication.restoreOverrideCursor()
        self.setWindowTitle("Speaker Identification")
        self.groupBox.setEnabled(True)

    def slotPhononPlaybackFinished(self):
        self.pushButtonStop.setEnabled(False)

    def slotPhononStateChanged(self, state):
        if state == Phonon.StoppedState:
            self.pushButtonStop.setEnabled(False)
        elif state == Phonon.PlayingState:
            self.pushButtonStop.setEnabled(True)

    def slotPlayTestingSample(self):
        s_id, ok = self.comboBoxUsers.itemData(self.comboBoxUsers.currentIndex()).toInt()
        # Take the first one, not so important
        file_path = self.marf.get_testing_samples(s_id)[0]
        file_path = self.marf.get_testing_sample_path(file_path)
        self.phonon.setCurrentSource(Phonon.MediaSource(file_path))
        self.phonon.play()

    def slotStartPlayback(self, item):
        if item:
            file_path = item.text()
        else:
            file_path = self.listWidgetEnrollments.currentItem().text()

        file_path = self.marf.get_training_sample_path(unicode(file_path))

        # Set file path and start playing
        self.phonon.setCurrentSource(Phonon.MediaSource(file_path))
        self.phonon.play()

    def slotStopPlayback(self):
        self.phonon.stop()

    def slotShowRecordWindow(self):
        self._last_id, ok = self.comboBoxUsers.itemData(self.comboBoxUsers.currentIndex()).toInt()
        recordWindow = SPIDRecordWindow(self, self._last_id)
        recordWindow.show()

    def slotIdentifyFinished(self):
        self.groupBox.setEnabled(False)
        QtGui.qApp.processEvents()
        self.setWindowTitle("Identifying...")
        QtGui.qApp.processEvents()
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        #self.marf.write_speakers()
        ret = self.marf.identify(os.path.basename(self._last_testing_filename))
        print ret

        # Restore cursor
        QtGui.QApplication.restoreOverrideCursor()
        QtGui.QApplication.restoreOverrideCursor()
        self.setWindowTitle("Speaker Identification")
        self.groupBox.setEnabled(True)


    def slotShowIdentifyDialog(self):
        identifyWindow = SPIDIdentifyWindow(self)
        identifyWindow.show()

    def slotSampleRecordingFinished(self):
        self.marf.update_speaker(self._last_id, s_training=self._fileName)

        # Refresh the list
        self.reflectUserProperties(self.comboBoxUsers.currentIndex())

    def reflectUserProperties(self, index):
        s_id, ok = self.comboBoxUsers.itemData(index).toInt()
        training_samples = self.marf.get_training_samples(s_id)
        self.listWidgetEnrollments.clear()
        testing_sample = bool(self.marf.get_testing_samples(s_id))
        self.pushButtonPlayTestingSample.setEnabled(bool(testing_sample))
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
