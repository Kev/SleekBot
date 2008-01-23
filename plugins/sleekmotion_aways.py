"""
    sleekmotion_aways.py - A script to learn and use status messages.
    Copyright (C) 2007 Kevin Smith.

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
import thread
import time
import pickle


class statusstore(object):
    def __init__(self):
        self.null = None
        self.statuses = []
        self.loaddefault()
        

    def add(self, statusType, statusMessage):
        if statusMessage is None:
            return
        for (oldType, oldMessage) in self.statuses:
            if oldType == statusType and oldMessage == statusMessage:
                return
        self.statuses.append((statusType, statusMessage))
        self.savedefault()
        
    def getRandom(self):
        if len(self.statuses) == 0:
            return (None, None)
        return self.statuses[random.randint(0,len(self.statuses)-1)]
        
    def loaddefault(self):
        self.load("statuses.dat")
        
    def savedefault(self):
        self.save("statuses.dat")
        
    def load(self, filename):
        try:
            f = open(filename, 'rb')
        except:
            logging.warning("Error loading statuses")
            return
        self.statuses = pickle.load(f)
        f.close()

    def save(self, filename):
        try:
            f = open(filename, 'wb')
        except IOError:
            logging.warning("Error saving statuses")
            return
        pickle.dump(self.statuses, f)
        f.close()

class sleekmotion_aways(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.statuses = statusstore()
        self.about = "'sleekmotion_aways' Learn status messages from people, and use them.\nWritten by Kevin Smith"
        self.bot.add_handler("<presence />", self.handle_presence)
        thread.start_new(self.loop,())
        
    def loop(self):
        while 1:
            if random.randint(0,100) < 5:
                self.setRandomStatus()
            time.sleep(60)
            
    def setRandomStatus(self):
        if not self.bot.connected:
            return
        (statusMessage, statusType) = self.statuses.getRandom()
        logging.debug("sleekmotion_aways: trying to set a random status")
        if statusMessage is None:
            logging.debug("sleekmotion_aways: no random status available")
            return
        logging.debug("sleekmotion_aways: setting random status '%s' '%s'" % (str(statusType), str(statusMessage)))
        if statusMessage is None or statusMessage == "":
            return
        if statusType in ["dnd", "away", "xa", "ffc"]:
            self.bot.sendPresence(pshow=statusType, pstatus=statusMessage)
        else:
            self.bot.sendPresence(pstatus=statusMessage)
        
    def handle_presence(self, presence):
        source = presence.attrib['from']
        if not self.bot.shouldAnswerToJid(source):
            return
        entry = {}
        for tag in ['status','show']:
            if presence.find('{jabber:client}' + tag) != None:
                entry[tag] = presence.find('{jabber:client}' + tag).text
            else:
                entry[tag] = None
        logging.debug("Learning new '%s' status, '%s'" % (str(entry['show']),str(entry['status'])))
        self.statuses.add(entry['status'],entry['show'])