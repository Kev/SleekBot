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
from store import store
from optparse import OptionParser
from xml.etree import ElementTree as ET
import os
import time
import plugins
import sys

class sleekbot(sleekxmpp.sleekxmpp.xmppclient, basebot):
    def __init__(self, configFile, jid, password, ssl=False, plugin_config = {}):
        self.configFile = configFile
        self.botconfig = self.loadConfig(configFile)
        sleekxmpp.sleekxmpp.xmppclient.__init__(self, jid, password, ssl, plugin_config)
        basebot.__init__(self)
        storageXml = self.botconfig.find('storage')
        if storageXml is not None:
            self.store = store(storageXml.attrib['file'])
        else:
            logging.warning("No storage element found in config file - proceeding with no persistent storage, plugin behaviour may be undefined.")
        self.rooms = {}
        self.botplugin = {}
        self.pluginModules = {}
        self.add_event_handler("session_start", self.start, threaded=True)
        #KIS: I saw the current like and thought it redundant, so am commenting
        #self.loadConfig(self.configFile)
        self.register_bot_plugins()
        self.registerCommands()
    
    def loadConfig(self, configFile):
        """ Loads the specified config. Does not attempt to make changes based upon config.
        """
        return ET.parse(configFile)
    
    def registerCommands(self):
        aboutform = self.plugin['xep_0004'].makeForm('form', "About SleekBot")
        aboutform.addField('about', 'fixed', value=
"""SleekBot was written by Nathan Fritz.
SleekBot uses SleekXMPP which was also written by Nathan Fritz.
-----------------------------------------------------------------
Special thanks to Kevin Smith and David Search.
Also, thank you Athena for putting up with me while I programmed.""")
        self.plugin['xep_0050'].addCommand('about', 'About Sleekbot', aboutform)
        pluginform = self.plugin['xep_0004'].makeForm('form', 'Plugins')
        plugins = pluginform.addField('plugin', 'list-single', 'Plugins')
        for key in self.botplugin:
            plugins.addOption(key, key)
        plugins = pluginform.addField('option', 'list-single', 'Commands')
        plugins.addOption('about', 'About')
        #plugins.addOption('config', 'Configure')
        self.plugin['xep_0050'].addCommand('plugins', 'Plugins', pluginform, self.form_plugin_command, True)
    
    
    def form_plugin_command(self, form):
        value = form.getValues()
        option = value['option']
        plugin = value['plugin']
        if option == 'about':
            aboutform = self.plugin['xep_0004'].makeForm('form', "About SleekBot")
            aboutform.addField('about', 'fixed', value=self.botplugin[plugin].about)
            return aboutform, None, False
        elif option == 'config':
            pass

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
    
    def deregister_bot_plugins(self):
        """ Unregister all loaded bot plugins.
        """
        for plugin in self.botplugin.keys():
            self.deregisterBotPlugin(plugin)
    
    def plugin_name_to_module(self, pluginname):
        """ Takes a plugin name, and returns a module name
        """
        #following taken from sleekxmpp.py
        # discover relative "path" to the plugins module from the main app, and import it.
        return "%s.%s" % (globals()['plugins'].__name__, pluginname)
    
    def deregisterBotPlugin(self, pluginname):
        """ Unregisters a bot plugin.
        """
        logging.info("Unloading plugin %s" % pluginname)
        if hasattr(self.botplugin[pluginname], 'shutDown'):
            logging.debug("Plugin has a shutDown() method, so calling that.")
            self.botplugin[pluginname].shutDown()
        del self.botplugin[pluginname]
    
    def registerBotPlugin(self, pluginname, config):
		""" Registers a bot plugin pluginname is the file and class name,
		and config is an xml element passed to the plugin. Will reload the plugin module,
		so previously loaded plugins can be updated.
		"""
		#f self.pluginModules.has_key(pluginname):
		#	del sys.modules[self.plugin_name_to_module(pluginname)]
		#	self.pluginModules[pluginname] = reload(self.pluginModules[pluginname])
		#else:
		#	self.pluginModules[pluginname] = __import__(self.plugin_name_to_module(pluginname))
# init the plugin class
		#self.botplugin[pluginname] = getattr(getattr(self.pluginModules[pluginname], pluginname), pluginname)(self, config)
		try:
			reload(globals()['plugins'].__dict__[pluginname])
		except:
			__import__(self.plugin_name_to_module(pluginname))
		self.botplugin[pluginname] = getattr(globals()['plugins'].__dict__[pluginname], pluginname)(self, config)
			
		return True
        
    def getOwners(self):
        """ Returns a list of all the jids belonging to bot owners
        """
        return self.getMemberClassJids('owner')
        
    def getAdmins(self):
        """ Returns a list of all the jids belonging to bot admins
        """
        return self.getMemberClassJids('admin')

    def getMembers(self):
        """ Returns a list of all the jids belonging to bot members
        """
        return self.getMemberClassJids('member')

    def getBannedUsers(self):
        """ Returns a list of all the jids belonging to banned users
        """
        return self.getMemberClassJids('banned')

    def getMemberClassJids(self, userClass):
        """ Returns a list of all jids belonging to users of a given class
        """
        jids = []
        users = self.botconfig.findall('users/' + userClass)
        if users:
            for user in users:
                userJids = user.findall('jid')
                if userJids:
                    for jid in userJids:
                        logging.debug("appending %s to %s list" % (jid.text, userClass))
                        jids.append(jid.text)
        return jids

    def getRealJid(self, jid):
        """ Returns the 'real' jid.
            If the jid isn't in a muc, it is returned.
            If the jid is in a muc and the true jid is known, that is returned.
            If it's in muc and the true jid isn't known, None is returned.
        """
        bareJid = self.getjidbare(jid)
        nick = self.getjidresource(jid)
        if bareJid in self.plugin['xep_0045'].getJoinedRooms():
            logging.debug("Checking real jid for %s %s (%s)" %(bareJid, nick, jid))
            realJid = self.plugin['xep_0045'].getJidProperty(bareJid, nick, 'jid')
            if realJid:
                return realJid
            else:
                return None
        return jid

    def getRealJidFromMessage(self, msg):
        jid = None
        if msg['type'] == 'groupchat':
            if msg['name'] == "":
                #system message
                jid = None
            else:
                jid = self.getRealJid("%s/%s" % (msg['room'], msg['name']))
                if jid:
                    jid = self.getjidbare(jid)
        else:
            if msg['jid'] in self['xep_0045'].getJoinedRooms():
                jid = self.getRealJid("%s/%s" % (msg['jid'], msg['resource']))
                if jid:
                    jid = self.getjidbare(jid)
            else:
                jid = self.getjidbare(msg.get('jid', ''))
        return jid

    def shouldAnswerToMessage(self, msg):
        """ Checks whether the bot is configured to respond to the sender of a message.
        """     
        if msg['type'] == 'groupchat':
            if msg['name'] == "":
                #system message
                return False
            return self.shouldAnswerToJid("%s/%s" % (msg['room'], msg['name']))
        else:
            if msg['jid'] in self['xep_0045'].getJoinedRooms():
                return self.shouldAnswerToJid("%s/%s" % (msg['jid'], msg['resource']))
            return self.shouldAnswerToJid(msg.get('jid', ''))
    
    def shouldAnswerToJid(self, passedJid):
        """ Checks whether the bot is configured to respond to the specified jid.
            Pass in a muc jid if you want, it'll be converted to a real jid if possible
            Accepts 'None' jids (acts as an unknown user).
        """     
        jid = self.getRealJid(passedJid)
        if jid:
            jid = self.getjidbare(jid)
        if jid in self.getBannedUsers():
            return False
        if not self.botconfig.find('require-membership'):
            return True
        if jid in self.getMembers() or jid in self.getAdmins() or jid in self.getOwners():
            return True
        return False

    def start(self, event):
        #TODO: make this configurable
        self.requestRoster()
        self.sendPresence(ppriority = self.botconfig.find('auth').attrib['priority'])
        self.joinRooms()
    
    def rehash(self):
        """ Re-reads the config file, making appropriate runtime changes.
            Causes all plugins to be reloaded (or unloaded). The XMPP stream, and
            channels will not be disconnected.
        """
        logging.info("Deregistering bot plugins for rehash")
        del globals()['plugins']
        globals()['plugins'] = __import__('plugins')
        self.clearCommands()
        self.deregister_bot_plugins()
        logging.info("Reloading config file")
        self.botconfig = self.loadConfig(self.configFile)
        self.register_bot_plugins()
        self.joinRooms()
    
    
    def joinRooms(self):
        logging.info("Re-syncing with required channels")
        newRoomXml = self.botconfig.findall('rooms/muc')
        newRooms = {}
        if newRoomXml:
            for room in newRoomXml:
                newRooms[room.attrib['room']] = room.attrib['nick']
        for room in self.rooms.keys():
            if room not in newRooms.keys():
                logging.info("Parting room %s." % room)
                self.plugin['xep_0045'].leaveMUC(room, self.rooms[room])
                del self.rooms[room]
        for room in newRooms.keys():
            if room not in self.rooms.keys():
                self.rooms[room] = newRooms[room]
                logging.info("Joining room %s as %s." % (room, newRooms[room]))
                self.plugin['xep_0045'].joinMUC(room, newRooms[room])

    def die(self):
        """ Kills the bot.
        """
        self.deregister_bot_plugins()
        self.rooms = {}
        logging.info("Disconnecting bot")
        self.disconnect()

    def restart(self):
        """ Cause the bot to be completely restarted (will reconnect etc.)
        """
        global shouldRestart
        shouldRestart = True
        logging.info("Restarting bot")
        self.die()

if __name__ == '__main__':
    #parse command line arguements
    optp = OptionParser()
    optp.add_option('-q','--quiet', help='set logging to ERROR', action='store_const', dest='loglevel', const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d','--debug', help='set logging to DEBUG', action='store_const', dest='loglevel', const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v','--verbose', help='set logging to COMM', action='store_const', dest='loglevel', const=5, default=logging.INFO)
    optp.add_option("-c","--config", dest="configfile", default="config.xml", help="set config file to use")
    opts,args = optp.parse_args()
    
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')

    global shouldRestart
    shouldRestart = True
    while shouldRestart:
        shouldRestart = False
        #load xml config
        logging.info("Loading config file: %s" % opts.configfile)
        configFile = os.path.expanduser(opts.configfile)
        config = ET.parse(configFile)
        auth = config.find('auth')
    
        #init
        logging.info("Logging in as %s" % auth.attrib['jid'])
    
        plugin_config = {}
        plugin_config['xep_0092'] = {'name': 'SleekBot', 'version': '0.1-dev'}
    
        bot = sleekbot(configFile, auth.attrib['jid'], auth.attrib['pass'], plugin_config=plugin_config)
        if not auth.get('server', None):
            # we don't know the server, but the lib can probably figure it out
            bot.connect() 
        else:
            bot.connect((auth.attrib['server'], 5222))
        bot.process()
        while bot.connected:
            time.sleep(1)
