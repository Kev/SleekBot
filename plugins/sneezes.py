"""
    sneezes.py - A plugin which reacts to sneezes.
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

class sneezes(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.bot.botplugin['sleekmotion'].addValues('blessyous', [
            "gesuntheit",
            "bless you",
            "Bless you",
            "/me hands %% a tissue",
            "e%REPEAT{2:5:w}%|*wipe*",
            "hehe, someone must be talking about you %VAR{smiles}",
            "good thing I bought this haz-mat suit",
            "Rogue bogey!",
            "/ducks",
            '/hides behind %ruser',
            "Great. Now I'm gonna get a cold %VAR{unsmiles}",
            "Eek. Don't give it to me",
            "%% - I recommend %VAR{sillyThings}"])
        self.about = "'sneezes' Says thing when people sneeze. \nBased on the bMotion plugin.\nWritten by Kevin Smith"
        self.bot.botplugin['sleekmotion'].registerTrigger('sneeze', '^\*?(/me sneezes|.hatsjoe|wachoo|sneezes|.a+tchoo+)', 60, 'blessyous')
        
            

