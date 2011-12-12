#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

from AudioRecorder import AudioRecorderThread

from ui.ui_recordwindow import Ui_SPIDRecordWindow

class SPIDRecordWindow(QtGui.QDialog, Ui_SPIDRecordWindow):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.setupUi(self)

        self.pushButtonStartRecording.clicked.connect(self.slotStartRecording)
        self.pushButtonStopRecording.clicked.connect(self.slotStopRecording)

        self.thread = AudioRecorderThread(self)
        self.thread.finished.connect(self.slotRecordingFinished)
        self.thread.finished.connect(self.parent().slotSampleRecordingFinished)

    def setFileName(self, file_name):
        self.labelFileName.setText(file_name)
        self.thread.setOutputFileName(file_name)

    def slotStopRecording(self):
        self.thread.exiting = True
        self.hide()

    def slotStartRecording(self):
        self.thread.start()
        self.pushButtonStartRecording.setEnabled(False)
        self.pushButtonStopRecording.setEnabled(True)

    def slotRecordingFinished(self):
        self.pushButtonStopRecording.setEnabled(False)
        self.pushButtonStartRecording.setEnabled(True)
