#!/usr/bin/python
# -*- coding: utf-8 -*-

import pwd

class User(object):
    def __init__(self, pw):
        self.loginName = pw.pw_name
        self.userID = pw.pw_uid
        self.realName = pw.pw_gecos

class SystemUsers(object):
    def __init__(self):
        self.users = {}

        # Fill in regular users
        for entry in pwd.getpwall():
            if entry.pw_uid >= 1000 and entry.pw_uid < 2000:
                # Regular user
                self.users[entry.pw_name] = entry

    def getUsers(self):
        return self.users

    def getUser(self, user):
        try:
            return User(self.users[user])
        except KeyError, ke:
            print "User %s not found!" % user
