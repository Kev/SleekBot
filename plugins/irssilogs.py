"""
	irssilogs.py - A plugin for logging muc traffic in an irssi style.
	Copyright (C) 2008 Kevin Smith

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

import datetime
import time
import logging

class irssilogfile(object):
    """ Handle writing to a single irssi log file.
    """
    def __init__(self, muc, fileName):
        """ Create a logfile handler for a given muc and file.
        """
        self.muc = muc
        self.fileName = fileName
        self.logfile = open(self.fileName, 'a')
    
    def datetimeToTimestamp(self, dt):
        """ Convert a datetime to hh:mm
        """
        return "00:00"
        
    def logPresence(self, presence):
        """ Log the presence to the file.
            Formats:
            join = '20:06 -!- Nick [userhost] has joined #room'
            quit = '19:07 -!- Nick [userhost] has quit [status]'
        """
        values = {}
        values['nick'] = presence['nick']
        values['reason'] = presence.get('status', "")
        values['userhost'] = presence['room']
        values['time'] = self.datetimeToTimestamp(presence['dateTime'])
        values['room'] = '#%s' % presence['room']
        if presence.get('type', None) == 'unavailable':
            line = '%(time)s -!- %(nick)s [%(userhost)s] has quit [%(reason)s]'
        else:
            line = '%(time)s -!- %(nick)s [%(userhost)s] has joined %(room)s'
        self.appendLogLine(line % values)
        
    def logMessage(self, message):
        """ Log the message to the file.
            Formats:
            message = '09:43 <+Nick> messagebody'
            action = '10:45  * Nick actionbodies'
            topic = '18:38 -!- Nick changed the topic of #room to: New Topic'
        """
        values = {}
        values['nick'] = message['name']
        values['userhost'] = message['room']
        values['time'] = self.datetimeToTimestamp(message['dateTime'])
        values['room'] = '#%s' % message['room']
        values['body'] = message['message']
        action = False
        topic = False
        if values['body'][:4] == '/me ':
            action = True
        if action:
            values['body'] = values['body'][4:]
            line = '%(time)s  * %(nick)s %(body)s'            
        elif topic:
            line = '%(time)s -!- %(nick)s changed the topic of %(room)s to: %(body)s'
        else:
            line = '%(time)s <%(nick)s> %(body)s'

        self.appendLogLine(line % values)
    
    def appendLogLine(self, line):
        """ Append the line to the log
        """
        self.logfile.write("%s\n" % line)
        self.logfile.flush()
        
class irssilogs(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.about = "Log muc events."
        self.bot.add_event_handler("groupchat_presence", self.handle_groupchat_presence, threaded=True)
        self.bot.add_event_handler("groupchat_message", self.handle_groupchat_message, threaded=True)
        self.roomLogFiles = {}
        self.roomMembers = {}
        logs = self.config.findall('log')
        if logs:
            for log in logs:
                room = log.attrib['room']
                fileName = log.attrib['file']
                self.roomLogFiles[room] = irssilogfile(room, fileName)
                self.roomMembers[room] = []
                logging.info("irssilogs.py script logging %s to %s." % (room, fileName))
                
    
    def handle_groupchat_presence(self, presence):
        """ Monitor MUC presences.
        """
        presence['dateTime'] = datetime.datetime.now()
        if presence['room'] in self.roomLogFiles.keys():
            if presence.get('type', None) == 'unavailable' or presence['nick'] not in self.roomMembers[presence['room']]:
                self.roomLogFiles[presence['room']].logPresence(presence)
                if presence.get('type', None) == 'unavailable':
                    for i in range(0,len(self.roomMembers[presence['room']])):
                        if self.roomMembers[presence['room']][i] == presence['nick']:
                           self.roomMembers[presence['room']].remove(i)
                           break 
                else:
                    self.roomMembers[presence['room']].append(presence['nick'])
        
    
    def handle_groupchat_message(self, message):
        """ Monitor MUC messages.
        """
        message['dateTime'] = datetime.datetime.now()
        if message['room'] in self.roomLogFiles.keys():
            self.roomLogFiles[message['room']].logMessage(message)

    
