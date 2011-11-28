#!/usr/bin/python
# -*- coding: utf-8 -*-

import pwd

class SystemUsers(object):
    def __init__(self):
        self.users = {}

        # Fill in regular users
        for entry in pwd.getpwall():
            if entry.pw_uid >= 1000 and entry.pw_uid < 2000:
                # Regular user
                self.users[pw_name] = entry
