"""
    sleekmotion.py - An approximate port of bMotion to Sleek.
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
import re
import random

class sleekmotionstore(object):
    def __init__(self):
        self.chatiness = 1
        self.store = {}

    def loaddefault(self):
        self.load("sleekmotion.dat")

    def savedefault(self):
        self.save("sleekmotion.dat")

    def load(self, filename):
        try:
            f = open(filename, 'rb')
        except:
            logging.warning("Error loading sleekmotion config")
            return
        self = pickle.load(f)
        f.close()

    def save(self, filename):
        try:
            f = open(filename, 'wb')
        except IOError:
            logging.warning("Error saving sleekmotion config")
            return
        pickle.dump(self, f)
        f.close()
    

class sleekmotion(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.store = sleekmotionstore()
        self.store.loaddefault()
        self.about = "'sleekmotion' is an approximate port of bMotion to SleekBot.\nWritten By: Kevin Smith"
        #self.bot.addIMCommand('chatiness', self.handle_chatiness)
        #self.bot.addMUCCommand('chatiness', self.handle_chatiness)
        #self.bot.addHelp('chatiness', 'Chatiness command', "Multiplier for the chatiness of a bot.", 'chatiness 0-100')
        self.commands = {}
        self.outputPlugins = {}
        self.botNicks = ['sleek']
        nicks = self.config.findall('botNick')
        if nicks:
            self.botNicks = []
            for nick in nicks:
                self.botNicks.append(nick.text)
        
        self.bot.add_event_handler("groupchat_message", self.handle_message, threaded=True)
        import sleekmotion_abstracts
        sleekmotion_abstracts.importInto(self)
        
    def registerTrigger(self, name, regexp, frequency, response):
        """ Add a trigger, with id 'name', triggered when text matches 'regexp', 
            with a frequency%, and where the response is either a var name or function.
        """
        responses = None
        function = None
        responseList = None
        if type(response) == type(self.registerTrigger):
            function = response
        elif type(response) == type([]):
            responseList = response
        else:
            responses = response
        command = {'name':name, 'regexp':regexp, 'frequency':frequency, 'function':function, 'responseVar':responses, 'responseList':responseList}
        self.commands[name] = command
        logging.debug("Registering trigger '%s' (%s) " %(name,regexp))
    
    def addValues(self, varName, values):
        """ Adds the list of values to the variable in the store.
        """
        for value in values:
            if varName not in self.store.store.keys():
                self.store.store[varName] = []
            if value not in self.store.store[varName]:
                self.store.store[varName].append(value)
        
    def ruser(self):
        """ Returns a random nickname that the bot knows about.
        """
        self.store.store['names'] = ["Kev",'albert','remko','textshell','hal','infiniti','psidekick','xepbot']
        return self.store.store['names'][random.randint(0,len(self.store.store['names'])-1)]
    
    def variableValue(self, varname):
        """ Return a random value from a variable.
        """
        logging.debug("sleekmotion getting value for '%s'" %varname)
        
        if varname not in self.store.store.keys():
            return "funny thing from an amusing list I've not defined yet (%s)" % varname
        
        return self.store.store[varname][random.randint(0,len(self.store.store[varname])-1)]
    
    def getColenChars(self):
        """ Return 'Colen characters'.
        """
        response = ""
        colen = ["!","$","%","^","&","*","(",")","@","#"]
        for i in random.randint(4,12):
            response = response + colen[random.randint(0,len(colen)-1)]
        return response
    
    def registerOutputPlugin(self, plugin):
        """ Adds the specified output plugin.
        """
        self.outputPlugins[plugin['name']] = plugin
    
    def applyOutputPlugins(self, response, message):
        """ For each registered output plugin, possibly apply it.
        """
        modified = response
        for plugin in self.outputPlugins.values():
            if random.randint(0, 99) < plugin['probability']:
                logging.debug("Applying output plugin '%s'" % plugin['name'])
                modified = plugin['function'](modified)
                modified = self.parseResponse(modified, message, False)
        return modified
        
    def parseResponse(self, response, message, allowOutputPlugins = True):
        """ Parses special strings out of the response.
        """
        logging.debug("Parsing response '%s' (outputplugins = %s)" % (response, str(allowOutputPlugins)))
        r = re.compile('%ruser')
        
        modified = response
        
        while r.search(modified):
            user = self.ruser()
            modified = re.sub(r, user, modified)
        
        r = re.compile('%%')
        while r.search(modified):
            if message['type'] == 'groupchat':
                nick = message['name']
            else:
                nick = message['name']
            modified = re.sub(r, nick, modified)
        
        r = re.compile('%colen')
        while r.search(modified):
            colen = self.getColenChars()
            modified = re.sub(r, colen, modified)
            
        r = re.compile('%VAR\\{(?P<varname>.+)\\}')
        while not r.search(modified) == None:
            varname = r.search(modified).group('varname')
            modified = re.sub(r, self.variableValue(varname), modified)
        
        r = re.compile('%REPEAT\\{(?P<min>.+),(?P<max>.+),(?P<string>.+)\\}')
        while not r.search(modified) == None:
            string = r.search(modified).group('string')
            min = int(r.search(modified).group('min'))
            max = int(r.search(modified).group('max'))
            replacement = ""
            for i in random.randint(min,max):
                replacement = replacement + string
            modified = re.sub(r, replacement, modified)
        
        ready = (response == modified)
        
        while not ready:
            newModified = self.parseResponse(modified, message, False)
            ready = (newModified == modified)
            modified = newModified
        
        if allowOutputPlugins:
            modified = self.applyOutputPlugins(modified, message)    
        
        return modified
    
    def botNickRegexp(self):
        """ Returns a regexp string matching bot nicks.
        """
        return "(%s)" % "|".join(self.botNicks)
    
    def parseTrigger(self, trigger):
        """ Parse special strings from a trigger regexp.
        """
        r = re.compile('%botnicks')
        modified = trigger
        while not r.search(modified) == None:
            modified = re.sub(r, self.botNickRegexp(), modified)
        
        logging.debug("trigger transformed to '%s'" % modified)
        return modified
    
    def parseMultiline(self, response):
        """ Parses | out into multiple strings.
        """
        return response.split('|')
        
        
    def handle_message(self, message):
        body = message.get('message', '')
        logging.debug("sleekmotion handling message body '%s'" % body)
        for trigger in self.commands.values():
            logging.debug("Comparing for trigger '%s'" % trigger['regexp'])
            if re.compile(self.parseTrigger(trigger['regexp'])).search(body):
                if random.randint(0,100) < trigger['frequency'] * self.store.chatiness:
                    logging.debug("Deciding not to respond to match")
                    continue
                if not trigger['function'] == None:
                    response = trigger.function(body, message)
                elif not trigger['responseList'] == None:
                        response = trigger['responseList'][random.randint(0,len(trigger['responseList'])-1)]
                else:
                    response = self.variableValue(trigger['responseVar'])
                response = self.parseResponse(response, message)
                logging.debug("Responding with '%s'" % response)
                for responseLine in self.parseMultiline(response):
                    if message['type'] == 'groupchat':
                        self.bot.sendMessage("%s" % message.get('room', ''), responseLine, mtype=message.get('type', 'groupchat'))
                    else:
                        self.bot.sendMessage("%s/%s" % (message.get('jid', ''), message.get('resource', '')), responseLine, mtype=message.get('type', 'chat'))
        
    