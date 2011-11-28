#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyaudio
import wave

class AudioRecorder(object):
    def __init__(self, outputFileName, seconds,
                       format_=pyaudio.paInt16,
                       channels=1,
                       rate=8000,
                       framesPerBuffer=1024):
        self.outputFileName = outputFileName
        self.format_ = format_
        self.channels = channels
        self.rate = rate
        self.duration = seconds
        self.framesPerBuffer = framesPerBuffer

        self.pyAudio = pyaudio.PyAudio()

    def record(self):
        result = []
        stream = self.pyAudio.open(format=self.format_,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.framesPerBuffer)

        for i in range(0, self.rate / self.framesPerBuffer * self.duration):
            data = stream.read(self.framesPerBuffer)
            result.append(data)

        stream.close()
        return "".join(result)

    def writeRecordedData(self, data):
        waveFile = wave.open(self.outputFileName, "wb")
        waveFile.setnchannels(self.channels)
        waveFile.setsampwidth(self.pyAudio.get_sample_size(self.format_))
        waveFile.setframerate(self.rate)
        waveFile.writeframes(data)
        waveFile.close()

    def close(self):
        self.pyAudio.terminate()
