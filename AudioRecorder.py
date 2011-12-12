#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import QThread
import pyaudio
import wave

class AudioRecorderThread(QThread):
    def __init__(self, parent=None,
                       format_=pyaudio.paInt16,
                       channels=1,
                       rate=8000,
                       framesPerBuffer=1024):

        QThread.__init__(self, parent)

        self.format_ = format_
        self.channels = channels
        self.rate = rate
        self.framesPerBuffer = framesPerBuffer
        self.pyAudio = pyaudio.PyAudio()
        self.exiting = False

    def setOutputFileName(self, fileName):
        self.outputFileName = fileName

    def run(self):
        result = []
        stream = self.pyAudio.open(format=self.format_,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.framesPerBuffer)

        while not self.exiting:
            data = stream.read(self.framesPerBuffer)
            result.append(data)

        stream.close()

        waveFile = wave.open(self.outputFileName, "wb")
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.pyAudio.get_sample_size(self.format_))
        waveFile.setframerate(self.rate)
        waveFile.writeframes("".join(result))
        waveFile.close()

    def close(self):
        self.pyAudio.terminate()
