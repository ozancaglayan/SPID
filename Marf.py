#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess

class MarfSpeaker(object):
    def __init__(self, s_id, s_name, s_training, s_testing):
        self.s_id = s_id
        self.s_name = s_name
        self.s_training = s_training
        self.s_testing = s_testing


class Marf(object):
    def __init__(self, marf_path="marf"):
        self.marf_path = marf_path
        self.speaker_db = os.path.join(self.marf_path, "speakers.txt")

        # Should always be run in the marf directory
        self.cmd = ["java", "-ea", "-Xmx512m", "-jar", "SpeakerIdentApp.jar"]

        self.speakers = {}

        # Fill speaker list
        for line in open(self.speaker_db, "r").readlines():
            data = line.strip().split(",")

            s_training = []
            s_testing = ""

            s_id = int(data.pop(0))
            s_name = data.pop(0)
            try:
                s_training = data.pop(0).split("|")
                s_testing = data.pop(0)
            except IndexError:
                pass

            self.speakers[s_id] = MarfSpeaker(s_id, s_name, s_training, s_testing)

        # Hold the next id
        self.next_id = max(self.speakers.keys()) + 1

    def get_all_speakers(self):
        return self.speakers

    def get_trained_speakers(self):
        d =  {}
        for key, value in self.speakers.items():
            if value.s_training:
                d[key] = value

        return d

    def train(self):
        train_cmd = self.cmd[:]
        train_cmd.extend(["--train", "training-samples",
                          "-endp", "-lpc", "-cheb"])
        process = subprocess.Popen(train_cmd,
                                   cwd=self.marf_path,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process.communicate()[0].startswith("Done training on folder \"training-samples\".")


    def identify(self, sample):
        # sample is the temporarily recorded wave file
        ident_cmd = self.cmd[:]
        ident_cmd.extend(["--ident", "testing-samples/%s" % sample,
                          "-endp", "-lpc", "-cheb"])
        process = subprocess.Popen(ident_cmd,
                                   cwd=self.marf_path,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout = process.communicate()[0]
        for line in stdout.split("\n"):
            if "Expected Speaker's ID:" in line.strip():
                return line.split("Expected Speaker's ID:")[1].strip()

    def write_speakers(self):
        speaker_file = open(self.speaker_db, "w")

        for s_id in sorted(self.speakers.keys()):
            speaker = self.speakers[s_id]
            speaker_file.write("%s,%s" % (speaker.s_id, speaker.s_name))
            if speaker.s_training:
                speaker_file.write(",%s" % ("|".join(speaker.s_training)))
                if speaker.s_testing:
                    speaker_file.write(",%s" % speaker.s_testing)
            speaker_file.write("\n")

    def add_speaker(self, s_name, s_training, s_testing):
        self.speakers[self.next_id] = MarfSpeaker(self.next_id,
                                                  s_name,
                                                  s_training,
                                                  s_testing)

        self.write_speakers()
        self.next_id += 1



if __name__ == "__main__":

    m = Marf()
    #m.add_speaker("Ozan", ["ozan1.wav", "ozan2.wav"], "ozan-test.wav")
    """
    print "Training: %s" % m.train()

    # Random identify
    import math
    import time
    import random

    random.seed(time.time())

    trained_speakers = m.get_trained_speakers()
    random_id = int(math.floor(random.random()*len(trained_speakers)))
    speaker = trained_speakers[random_id]
    print "Identifying (%d) %s" % (speaker.s_id, speaker.s_name)
    print "ID Identified: %s" % m.identify(speaker.s_testing)
    """
