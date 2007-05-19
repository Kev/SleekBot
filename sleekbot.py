#!/usr/bin/env python2.5
"""
    This file is part of SleekXMPP.

    SleekXMPP is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    SleekXMPP is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SleekXMPP; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import logging
import sleekxmpp.sleekxmpp
from basebot import basebot
from optparse import OptionParser
from xml.etree import ElementTree as ET
import os
import time
import plugins

class sleekbot(sleekxmpp.sleekxmpp.xmppclient, basebot):
	def __init__(self, botconfig, jid, password, ssl=False, plugin_config = {}):
		sleekxmpp.sleekxmpp.xmppclient.__init__(self, jid, password, ssl, plugin_config)
		basebot.__init__(self)
		self.botplugin = {}
		self.add_event_handler("session_start", self.start, threaded=True)
		self.botconfig = botconfig
		self.register_bot_plugins()
	
	def register_bot_plugins(self):
		""" Registers all bot plugins required by botconfig.
		"""
		plugins = self.botconfig.findall('plugins/bot/plugin')
		if plugins:
			for plugin in plugins:
				logging.info("Loading plugin %s." % (plugin.attrib['name']))
				loaded = self.registerBotPlugin(plugin.attrib['name'], plugin.find('config'))
				if not loaded:
					logging.info("Loading plugin %s FAILED." % (plugin.attrib['name']))
					
	
	def registerBotPlugin(self, pluginname, config):
		""" Registers a bot plugin pluginname is the file and class name,
		and config is an xml element passed to the plugin.
		"""
		#following taken from sleekxmpp.py
		# discover relative "path" to the plugins module from the main app, and import it.
		__import__("%s.%s" % (globals()['plugins'].__name__, pluginname))
		# init the plugin class
		self.botplugin[pluginname] = getattr(getattr(plugins, pluginname), pluginname)(self, config)
		return True
		
	def start(self, event):
		#TODO: make this configurable
		self.requestRoster()
		self.sendPresence(ppriority=10)
		self.joinRooms()
	
	def joinRooms(self):
		rooms = self.botconfig.findall('rooms/muc')
		if rooms:
			for room in rooms:
				logging.info("Joining room %s as %s." % (room.attrib['room'], room.attrib['nick']))
				self.plugin['xep_0045'].joinMUC(room.attrib['room'], room.attrib['nick'])

if __name__ == '__main__':
	#parse command line arguements
	optp = OptionParser()
	optp.add_option('-q','--quiet', help='set logging to ERROR', action='store_const', dest='loglevel', const=logging.ERROR, default=logging.INFO)
	optp.add_option('-d','--debug', help='set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
	optp.add_option('-v','--verbose', help='set logging to COMM', action='store_const', dest='loglevel', const=5, default=logging.INFO)
	optp.add_option("-c","--config", dest="configfile", default="config.xml", help="set config file to use")
	opts,args = optp.parse_args()
	
	logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

	#load xml config
	logging.info("Loading config file: %s" % opts.configfile)
	config = ET.parse(os.path.expanduser(opts.configfile))
	auth = config.find('auth')
	
	#init
	logging.info("Logging in as %s" % auth.attrib['jid'])
	
	plugin_config = {}
	plugin_config['xep_0092'] = {'name': 'SleekBot', 'version': '0.1-dev'}
	
	con = sleekbot(config, auth.attrib['jid'], auth.attrib['pass'], plugin_config=plugin_config)
	if not auth.get('server', None):
		# we don't know the server, but the lib can probably figure it out
		con.connect() 
	else:
		con.connect((auth.attrib['server'], 5222))
	con.process()
	while con.connected:
		time.sleep(1)
