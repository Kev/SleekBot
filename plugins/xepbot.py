"""
	xepbot.py - A XEP information plugin
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
from urllib import urlopen
from xml.etree import ElementTree as ET
import time
import math

class xepbot(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.bot.addIMCommand('xep', self.handle_xep)
		self.bot.addMUCCommand('xep', self.handle_xep)
		self.bot.addHelp('xep', 'Xep Command', "Returns details of the specified XEP.", 'xep [number]')
		self.lastCacheTime = 0
		self.xeps = None
		self.ensureCacheIsRecent()

	def ensureCacheIsRecent(self):
		""" Check if the xep list cache is older than the age limit in config and refreshes if so.
		"""
		now = math.floor(time.time())
		expirySeconds = int(self.config.find('cache').attrib['expiry']) * 60 * 60
		if self.lastCacheTime + expirySeconds < now:
			self.refreshCache()
	
	def refreshCache(self):
		""" Updates the xep list cache.
		"""
		url = self.config.find('xeps').attrib['url']
		try:
			urlObject = urlopen(url)
			self.xeps = ET.parse(urlObject).getroot()
			self.lastCacheTime = math.floor(time.time())
		except:
			logging.info("Loading XEP list file %s failed." % (url))

	def handle_xep(self, command, args, msg):
		self.ensureCacheIsRecent()
		try:
			xepnumber = '%04i' % int(args)
		except:
			xepnumber = ''
		if self.xeps == None:
			return 'I have suffered a tremendous error: I cannot reach the XEP list (and have never been able to)'
		response = ''
		for xep in self.xeps.findall('xep'):
			if xep.find('number').text == xepnumber or xep.find('name').text.lower().find(args.lower()) >= 0:
				if response != '':
					response = response + "\n\n"
				response = response + '%(type)s XEP-%(number)s, %(name)s, is %(status)s (last updated %(updated)s): http://www.xmpp.org/extensions/xep-%(number)s.html'
				texts = {}
				texts['type'] = xep.find('type').text 
				texts['number'] = xep.find('number').text 
				texts['name'] = xep.find('name').text 
				texts['status'] = xep.find('status').text 
				texts['updated'] = xep.find('updated').text
				response = response % texts
		if response == '':
			response = 'The XEP you specified ("%s") could not be found' % args
		return response
