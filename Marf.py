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

class MarfSample(object):
    def __init__(self, sample_path):
        pass

class Marf(object):
    def __init__(self, marf_path="marf"):
        self.marf_path = marf_path
        self.speaker_db = os.path.join(self.marf_path, "speakers.txt")
        self.training_samples_dir = "training-samples"
        self.testing_samples_dir = "testing-samples"

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

    def get_training_sample_path(self, training_sample):
        return os.path.join(os.getcwd(), self.marf_path,
                            self.training_samples_dir,
                            training_sample)

    def get_testing_sample_path(self, testing_sample):
        return os.path.join(os.getcwd(), self.marf_path,
                            self.testing_samples_dir,
                            testing_sample)

    def get_all_speakers(self):
        return sorted(self.speakers.values(), key=lambda spkr: spkr.s_name)

    def get_training_samples(self, s_id):
        return sorted(self.speakers[s_id].s_training)

    def get_testing_sample(self, s_id):
        return self.speakers[s_id].s_testing

    def get_next_training_sample_path(self, s_id):
        import time
        file_name = "%s-%s.wav" % (self.speakers[s_id].s_name.lower(),
                                   time.strftime("%Y%m%d_%H%M%S"))
        return os.path.join(os.getcwd(), self.marf_path,
                            self.training_samples_dir, file_name)


    def get_next_testing_sample_path(self):
        import time
        file_name = "testing-%s.wav" % time.strftime("%Y%m%d_%H%M%S")
        return os.path.join(os.getcwd(), self.marf_path,
                            self.testing_samples_dir, file_name)

    def train(self):
        train_cmd = self.cmd[:]
        train_cmd.extend(["--train", self.training_samples_dir,
                          "-endp", "-lpc", "-cheb"])
        process = subprocess.Popen(train_cmd,
                                   cwd=self.marf_path,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process.communicate()[0]

    def identify(self, sample):
        # sample is the temporarily recorded wave file
        ident_cmd = self.cmd[:]
        ident_cmd.extend(["--ident", "%s/%s" % (self.testing_samples_dir, sample),
                          "-endp", "-lpc", "-cheb"])
        process = subprocess.Popen(ident_cmd,
                                   cwd=self.marf_path,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout = process.communicate()[0]
        print stdout
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
        self.next_id += 1
        self.write_speakers()

    def update_speaker(self, s_id, s_name=None, s_training=None, s_testing=None):
        try:
            speaker = self.speakers[s_id]
            if s_name:
                speaker.s_name = s_name
            if s_training:
                speaker.s_training.append(os.path.basename(s_training))
            if s_testing:
                speaker.s_testing = s_testing
        except KeyError, e:
            print "No speaker with id %s!" % s_id

        self.write_speakers()
