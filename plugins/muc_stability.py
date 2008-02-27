"""
    muc_stability.py - A plugin for keeping Sleek in muc channels it joins.
    Copyright (C) 2008 Kevin Smith

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
import thread

class muc_stability(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.about = "Attempts to keep Sleek in muc channels."
        self.shuttingDown = False
        thread.start_new(self.loop, ())
        self.bot.add_handler("<message xmlns='jabber:client' type='error'><error type='modify' code='406' ><not-acceptable xmlns='urn:ietf:params:xml:ns:xmpp-stanzas'/></error></message>", self.handle_message_error)
        
        
    def loop(self):
        """ Perform the muc checking.
        """
        while not self.shuttingDown:
            #print "looping on feed %s" % feedUrl
            if self.bot['xep_0045']:
                for muc in self.bot['xep_0045'].getJoinedRooms():
                    jid = self.bot['xep_0045'].getOurJidInRoom(muc)
                    self.bot.sendMessage(jid, None, mtype='chat')
            time.sleep(600)

    def handle_message_error(self, xml):
        """ On error messages, see if it's from a muc, and rejoin the muc if so.
            (Subtle as a flying mallet)
        """
        source = xml.attrib['from']
        room = self.bot.getjidbare(source)
        if room not in self.bot['xep_0045'].getJoinedRooms():
            return
        nick = self.bot.getjidresource(self.bot['xep_0045'].getOurJidInRoom(room))
        logging.debug("muc_stability: error from %s, rejoining as %s" %(room, nick))
        self.bot['xep_0045'].joinMUC(room, nick)

"""<message  to="jabber@conference.jabber.org/sleek" id="abbbb" />
"""

