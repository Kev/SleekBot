"""
    sleekmotion_complexs.py - A port of the bmotion simple stuffs.
    Copyright (C) 2007 Kevin Smith.
    Original logic copyright of bMotion project.

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
import re

class sleekmotion_complexs(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        
        self.about = "'sleekmotion_complexs' Simple ports of lots of the bmotion complex plugins. \nBased on the bMotion plugin.\nWritten by Kevin Smith"
        
        t = self.bot.botplugin['sleekmotion'].registerTrigger
        v = self.bot.botplugin['sleekmotion'].addValues
        
        t("xmas", "(merry|happy|have a good) (xmas|christmas|chrismas|newyear|new year) %botnicks", 100, self.xmas)
        t("asl", "^([a-zA-Z]+(:|,| )*)?a/?s/?l\??$", 100, self.asl)
        v("wins",["victory for %me%colen", "this victory strengthens the soul of %me!", "%VAR{harhars}", "%VAR{thanks}", "wh%REPEAT{2:6:e}! do I get %VAR{sillyThings} now?"])
        t("wins", "^%botnicks:? (wins|exactly|precisely|perfect|nice one|yes)[!1.]*$", 100, self.wins)
        t("wins2", "(nice one|well said|exactly|previsely|perfect|right one|yes|victory for),? %botnicks[!1.]*$", 100, self.wins)
        t("watchout", "^%botnicks,?:? (watchout|watch out|watch it|careful|run( for (it|the hills))?|hide|duck)!?", 100, self.watchout)
        v("woots", ["i like %%", "\\o/", "%REPEAT{3:7} %%", "\\o/ %%", "hurrah", "wh%REPEAT{3:7:e} %%", "%VAR{smiles}"])
        t("woot", "^[a-zA-Z0-9]+[!1~]+$", 5, self.woot)
        t("sorry1", "(i'm)?( )?(very)?( )?sorry(,)? %botnicks", 100, self.sorry)
        t("sorry2", "%botnicks:? sorry", 100, self.sorry)
        t("plusplus", "^[a-zA-Z0-9]+\+\++$", 50, self.plusplus)
        
    def xmas(self, nick, jid, handle, body, message):
        self.bot.botplugin['sleekmotion'].makeHappy()
        self.bot.botplugin['sleekmotion'].makeUnLonely()
        self.bot.botplugin['sleekmotion'].driftFriendship(handle,3)
        name = self.bot.botplugin['sleekmotion'].getRealName(handle, nick)
        return "merry christmas and happy new year "+name+" %VAR{smiles}"
    
    def asl(self, nick, jid, handle, body, message):
        return "%s: %d/%s/%s" % (nick, random.randint(12,65), self.bot.botplugin['sleekmotion'].getGender(), "%VAR{locations}")

    def wins(self, nick, jid, handle, body, message):
        self.bot.botplugin['sleekmotion'].makeHappy()
        self.bot.botplugin['sleekmotion'].makeUnLonely()
        self.bot.botplugin['sleekmotion'].driftFriendship(handle,1)
        return "%VAR{wins}"

    def watchout(self, nick, jid, handle, body, message):
        self.bot.botplugin['sleekmotion'].makeUnLonely()
        self.bot.botplugin['sleekmotion'].driftFriendship(handle,1)
        return "%VAR{hides}"
    
    def woot(self, nick, jid, handle, body, message):
        logging.debug("Wooting")
        response = self.bot.botplugin['sleekmotion'].variableValue("woots")
        item = re.compile('^(?P<item>[a-zA-Z0-9]+)[!1~]+$').search(body).group('item')
        r = re.compile('%%')
        while r.search(response):
            response = re.sub(r, item, response)
        return response
        
    def plusplus(self, nick, jid, handle, body, message):
        logging.debug("PlusPlussing")
        response = self.bot.botplugin['sleekmotion'].variableValue("woots")
        item = re.compile('^?P<item>[a-zA-Z0-9]+\+\++$').search(body).group('item')
        r = re.compile('%%')
        while r.search(response):
            response = re.sub(r, item, response)
        return response
        
    def sorry(self, nick, jid, handle, body, message):
        self.bot.botplugin['sleekmotion'].makeHappy()
        self.bot.botplugin['sleekmotion'].makeUnLonely()
        self.bot.botplugin['sleekmotion'].driftFriendship(handle,3)
        name = self.bot.botplugin['sleekmotion'].getRealName(handle, nick)
        return "%VAR{sorryok} %%"
