#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from AudioRecorder import AudioRecorderThread

from ui.ui_recordwindow import Ui_SPIDRecordWindow

class SPIDRecordWindow(QtGui.QDialog, Ui_SPIDRecordWindow):
    def __init__(self, parent=None, s_id=None):
        QtGui.QDialog.__init__(self, parent)

        self.s_id = s_id

        self.setupUi(self)

        self.pushButtonStartRecording.clicked.connect(self.slotStartRecording)
        self.pushButtonStopRecording.clicked.connect(self.slotStopRecording)

        self.thread = AudioRecorderThread(self)
        self.thread.finished.connect(self.slotRecordingFinished)
        self.thread.finished.connect(self.parent().slotSampleRecordingFinished)

    def slotStopRecording(self):
        self.thread.exiting = True
        self.hide()

    def slotStartRecording(self):
        if self.checkBoxTestingSample.isChecked():
            # Testing
            self.thread.setOutputFileName(self.parent().marf.get_next_testing_sample_path())
        else:
            # Training
            self.thread.setOutputFileName(self.parent().marf.get_next_training_sample_path(self.s_id))

        self.parent()._fileName = self.thread.outputFileName
        print self.parent()._fileName

        self.thread.start()
        self.pushButtonStartRecording.setEnabled(False)
        self.pushButtonStopRecording.setEnabled(True)

    def slotRecordingFinished(self):
        self.pushButtonStopRecording.setEnabled(False)
        self.pushButtonStartRecording.setEnabled(True)
