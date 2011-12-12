#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from AudioRecorder import AudioRecorderThread

from ui.ui_identifywindow import Ui_SPIDIdentifyWindow

class SPIDIdentifyWindow(QtGui.QDialog, Ui_SPIDIdentifyWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.pushButtonStartIdentifyRecording.clicked.connect(self.slotStartRecording)
        self.pushButtonStopIdentifyRecording.clicked.connect(self.slotStopRecording)

        self.thread = AudioRecorderThread(self)
        self.thread.finished.connect(self.slotRecordingFinished)
        self.thread.finished.connect(self.parent().slotIdentifyFinished)

    def slotStopRecording(self):
        self.thread.exiting = True
        self.hide()

    def slotStartRecording(self):
        self.parent()._last_testing_filename = self.parent().marf.get_next_testing_sample_path()
        self.thread.setOutputFileName(self.parent()._last_testing_filename)
        self.thread.start()
        self.pushButtonStartIdentifyRecording.setEnabled(False)
        self.pushButtonStopIdentifyRecording.setEnabled(True)

    def slotRecordingFinished(self):
        self.pushButtonStopIdentifyRecording.setEnabled(False)
        self.pushButtonStartIdentifyRecording.setEnabled(True)
