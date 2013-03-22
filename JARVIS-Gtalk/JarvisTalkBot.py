#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time

from PyGtalkRobot import GtalkRobot

############################################################################################################################

class JarvisBot(GtalkRobot):
    def command_001_TalkToJarvis(self, user, message, args):
        '''.*?(?s)(?m)'''
        self.replyMessage(user, time.strftime("%Y-%m-%d %a %H:%M:%S", time.gmtime()))

############################################################################################################################
if __name__ == "__main__":
    bot = JarvisBot()
    bot.setState('available', "J.A.R.V.I.S")
    bot.start("jarvis.systeme@gmail.com", "jarvispowered")