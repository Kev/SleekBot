"""
    say.py - A plugin for making a bot parrot text.
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
import datetime, time

class say(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.about = "Parrots text to a muc."
        self.bot.addIMCommand('say', self.handle_say)
        self.bot.addMUCCommand('say', self.handle_say)
        self.bot.addHelp('say', 'Say Command', "Have the bot parrot some text in a channel", 'say muc text')
            
    def handle_say(self, command, args, msg):
        if self.bot.getRealJidFromMessage(msg) not in self.bot.getOwners():
            return "I'm not your monkey."
        if args.count(" ") >= 1:
            [muc, text] = args.split(" ",1)
        else:
            return "Insufficient parameters."
        self.bot.sendMessage(muc, text, mtype='groupchat')
        return "Sent."
