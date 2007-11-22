"""
    sleekmotion_complexs.py - A port of the bmotion simple stuffs.
    Copyright (C) 2007 Kevin Smith.
    Original logic copyright of bMotion project.

    SleekBot is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    SleekBot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this software; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import logging
import random
import re

class sleekmotion_complexs(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        
        self.about = "'sleekmotion_complexs' Simple ports of lots of the bmotion complex plugins. \nBased on the bMotion plugin.\nWritten by Kevin Smith"
        
        t = self.bot.botplugin['sleekmotion'].registerTrigger
        v = self.bot.botplugin['sleekmotion'].addValues
        
        t("xmas", "(merry|happy|have a good) (xmas|christmas|chrismas|newyear|new year) %botnicks", 100, self.xmas)
        t("asl", "^([a-zA-Z]+(:|,| )*)?a/?s/?l\??$", 100, self.asl)
        
    def xmas(self, nick, jid, handle, body, message):
        self.bot.botplugin['sleekmotion'].makeHappy()
        self.bot.botplugin['sleekmotion'].makeUnLonely()
        self.bot.botplugin['sleekmotion'].driftFriendship(handle,3)
        name = self.bot.botplugin['sleekmotion'].getRealName(handle, nick)
        return "merry christmas and happy new year "+name+" %VAR{smiles}"
    
    def asl(self, nick, jid, handle, body, message):
        return "%s: %d/%s/%s" % (nick, random.randint(12,65), self.bot.botplugin['sleekmotion'].getGender(), "%VAR{locations}")
