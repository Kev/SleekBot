"""
    pingbot.py - A plugin for pinging Jids.
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

class pingbot(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "Pingbot allows users to ping other jids.\nWritten By: Kevin Smith"
		self.bot.addIMCommand('ping', self.handle_ping)
		self.bot.addMUCCommand('ping', self.handle_ping)
		self.bot.addHelp('ping', 'Ping Command', "Discover latency to a jid.", 'ping jid')
			
	def handle_ping(self, command, args, msg):
		latency = self.bot['xep_0199'].sendPing(args, 10)
		if latency == False:
			response = "No response when pinging " + args
		else:
			response = "Ping response received from %s in %d seconds." % (args, latency)
		return response
