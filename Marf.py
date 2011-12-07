#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class MarfSpeaker(object):
    def __init__(self, marf_path, s_id, s_name, s_training, s_testing):
        self.s_id = s_id
        self.s_name = s_name
        self.s_training = s_training
        self.s_testing = s_testing



class Marf(object):
    def __init__(self, marf_path="/opt/marf"):
        self.marf_path = marf_path
        self.speaker_db = os.path.join(self.marf_path, "speakers.txt")

        self.speakers = {}

        # Fill speaker list
        for line in open(self.speaker_db, "r").readlines():
            data = line.strip().split(",")

            s_id = int(data[0].strip())
            s_name = data[1].strip()
            s_training = []
            s_testing = ""
            try:
                # s_training is a list of wav files joined with '|'
                s_training = data[2].split("|")
            except IndexError:
                pass

            try:
                s_testing = data[3].strip()
            except IndexError:
                pass

            self.speakers[s_id] = [s_name, s_training, s_testing]

    def dump_speakers(self):
        for sp_id in sorted(self.speakers.keys()):
            sp_data = self.speakers[sp_id]
            sp = "%s,%s" % (sp_id, sp_data[0])
            try:
                data = "%s" % "|".join(sp_data[1])
            except IndexError:
                pass
            else:
                sp += ",%s" % data

            try:
                data = sp_data[2]
            except IndexError:
                pass
            else:
                sp += ",%s" % data

            print sp

    def add_speaker(self, s_id, s_name, s_training, s_testing):
        pass



if __name__ == "__main__":

    m = Marf()
    m.dump_speakers()

