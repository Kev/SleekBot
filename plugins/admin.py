"""
    admin.py - A plugin for administering the bot.
    Copyright (C) 2007 Kevin Smith

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

class admin(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.about = "'Admin' allows a bot owner to perform tasks such as rehashing a bot remotely.\nWritten By: Kevin Smith"
        self.bot.addIMCommand('rehash', self.handle_rehash)
        self.bot.addMUCCommand('rehash', self.handle_rehash)
        self.bot.addHelp('rehash', 'Rehash command', "Reload the bot config and plugins without dropping the XMPP stream.", 'rehash')
        self.bot.addIMCommand('die', self.handle_die)
        self.bot.addMUCCommand('die', self.handle_die)
        self.bot.addHelp('die', 'Die command', "Kill the bot.", 'kill')
        self.bot.addIMCommand('restart', self.handle_restart)
        self.bot.addMUCCommand('restart', self.handle_restart)
        self.bot.addHelp('restart', 'Restart command', "Restart the bot, reconnecting etc.", 'restart')

    def message_from_owner(self, msg):
        """ Was this message sent from a room owner?
        """
        jid = None
        if msg['type'] == 'groupchat':
            if msg['name'] == "":
                #system message
                jid = None
            else:
                jid = self.bot.getjidbare(self.bot.getRealJid("%s/%s" % (msg['room'], msg['name'])))
        else:
            if msg['jid'] in self.bot['xep_0045'].getJoinedRooms():
                jid = jid = self.bot.getjidbare(self.bot.getRealJid("%s/%s" % (msg['jid'], msg['resource'])))
            else:
                jid = self.bot.getjidbare(msg.get('jid', ''))
        logging.debug("admin.py checking for owner status on jid %s" % jid)
        return jid in self.bot.getOwners()
            
    def handle_rehash(self, command, args, msg):
        if self.message_from_owner(msg):
            self.bot.rehash()
            response = "Rehashed boss"
        else:
            response = "You are insufficiently cool, go away."
        return response
        
    def handle_restart(self, command, args, msg):
        if self.message_from_owner(msg):
            self.bot.restart()
            response = "Restarted boss"
        else:
            response = "You are insufficiently cool, go away."
        return response
        
    def handle_die(self, command, args, msg):
        if self.message_from_owner(msg):
            response = "Dying (you'll never see this message)"
            self.bot.die()
        else:
            response = "You are insufficiently cool, go away."
        return response    
