"""
    factoidbot.py - A plugin for remembering facts.
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
import pickle

class factstore(object):
    def __init__(self):
        self.null = None
        self.data = {}
        self.loaddefault()
        

    def list_terms(self):
        return self.data.keys()
    
    def add(self, term, fact):
        self.data[term.lower()] = fact
        self.savedefault()
        
    def get(self, term):
        if self.data.has_key(term.lower()):
            return self.data[term.lower()]
        return "No facts known about " + term
        
    def delete(self, term):
        if self.data.has_key(term.lower()):
            del self.data[term.lower()]
            self.savedefault()
    
    def loaddefault(self):
        self.load("factoids.dat")
        
    def savedefault(self):
        self.save("factoids.dat")
        
    def load(self, filename):
        try:
            f = open(filename, 'rb')
        except:
            logging.warning("Error loading factoids")
            return
        self.data = pickle.load(f)
        f.close()

    def save(self, filename):
        try:
            f = open(filename, 'wb')
        except IOError:
            logging.warning("Error saving factoids")
            return
        pickle.dump(self.data, f)
        f.close()

class factoidbot(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.factstore = factstore()
        self.bot.addIMCommand('fact', self.handle_fact)
        self.bot.addMUCCommand('fact', self.handle_fact)
        self.bot.addHelp('fact', 'Factoid Command', "Returns facts.", 'fact [topic]')
        self.bot.addIMCommand('factoid', self.handle_fact)
        self.bot.addMUCCommand('factoid', self.handle_fact)
            
    def handle_fact(self, command, args, msg):
        subcommand = None
        term = None
        fact = None
        if args.count(" ") > 1:
            [subcommand, term, fact] = args.split(" ",2)
        elif args.count(" ") > 0:
            [subcommand, term] = args.split(" ",1)
        else:
            subcommand = args
        admin_commands = ['list', 'add', 'delete']
        
        #non-admin commands
        if subcommand not in admin_commands:
            response = "facts for " + args + "\n" + args + ": " + self.factstore.get(args)
            return response
        
        #admin commands
            
        if "list" == subcommand:
            if self.bot.getRealJidFromMessage(msg) not in self.bot.getOwners() + self.bot.getAdmins():
                return "You do not have access to this function"
            terms = self.factstore.list_terms()
            response = "I know about the following topics:\n"
            for term in terms:
                response = response + "\t" + term
            response = response + "."
        elif "add" == subcommand:
            if self.bot.getRealJidFromMessage(msg) not in self.bot.getOwners() + self.bot.getAdmins():
                response = "You do not have access to this function"
            elif term != None and fact != None:
                self.factstore.add(term, fact)
                response = "Fact added"
            else:
                response = "To add a fact, both a topic and description are needed."
        elif "delete" == subcommand:
            if self.bot.getRealJidFromMessage(msg) not in self.bot.getOwners() + self.bot.getAdmins():
                response = "You do not have access to this function"
            else:
                self.factstore.delete(term)
                response = "Deleted (if found)"
        logging.debug("handle_fact done: %s" % response)
        return response


