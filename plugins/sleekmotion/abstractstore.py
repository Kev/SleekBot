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

class AbstractStore(object):
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