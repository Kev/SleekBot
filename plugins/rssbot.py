"""
    rssbot.py - A plugin for streaming RSS entries into a channel.
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
import feedparser
import thread
import time
import re

class rssbot(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        #self.bot.addIMCommand('xep', self.handle_xep)
        #self.bot.addMUCCommand('xep', self.handle_xep)
        #self.bot.addHelp('xep', 'Xep Command', "Returns details of the specified XEP.", 'xep [number]')
        self.rssCache = {}
        feeds = self.config.findall('feed')
        if feeds:
            for feed in feeds:
                logging.info("rssbot.py script starting with feed %s." % feed.attrib['url'])
                roomsXml = feed.findall('muc')
                if not roomsXml:
                    continue
                rooms = []
                for roomXml in roomsXml:
                    rooms.append(roomXml.attrib['room'])
                thread.start_new(self.loop,(feed.attrib['url'], feed.attrib['refresh'], rooms))

    def loop(self, feedUrl, refresh, rooms):
        """ The main thread loop that polls an rss feed with a specified frequency
        """
        self.loadCache(feedUrl)
        while True:
            #print "looping on feed %s" % feedUrl
            if self.bot['xep_0045']:
                feed = feedparser.parse(feedUrl)
                for item in feed['entries']:
                    if feedUrl not in self.rssCache.keys():
                        self.rssCache[feedUrl] = []
                    if item['title'] in self.rssCache[feedUrl]:
                        continue
                    #print u"found new item %s" % item['title']
                    for muc in rooms:
                        if muc in self.bot['xep_0045'].getJoinedRooms():
                            #print u"sending to room %s" %muc
                            self.sendItem(item, muc, feed['channel']['title'])
                    self.rssCache[feedUrl].append(item['title'])
                    #print u"remembering new item %s" % item['title']
            time.sleep(float(refresh)*60)
            
    def sendItem(self, item, muc, feedName):
        """ Sends a summary of an rss item to a specified muc.
        """
        #for contentKey in ['summary','value', '']:
        #    if item.has_key(contentKey):
        #        break
        #if contentKey == '':
        #    print "No content found for item"
        #    return
        #print u"found content in key %s" % contentKey
        content = self.bot.xmlesc(item['content'][0].value)
        text = u"Update from feed %s\n%s\n%s" % (feedName, self.bot.xmlesc(item['title']), content)
        self.bot.sendMessage(muc, text, mtype='groupchat')
    
    def cacheFilename(self, feedUrl):
        """ Returns the filename used to store the cache for a feedUrl
        """
        rep = re.compile('s/\W//g')
        return "rsscache-%s.dat" % rep.sub('', feedUrl)
    
    def loadCache(self, feed):
        """ Loads the cache of entries
        """
        try:
            f = open(self.cacheFilename(feed), 'rb')
        except:
            print "Error loading rss data %s" % self.cacheFilename(feed)
            return
        self.rssCache[feed] = pickle.load(f)
        f.close()
        
    def saveCache(self):
        """ Saves the cache of entries
        """
        try:
            f = open(self.cacheFilename(feed), 'wb')
        except IOError:
            print "Error saving rss data %s" % cacheFilename(food)
            return
        pickle.dump(self.rssCache[feed], f)
        f.close()