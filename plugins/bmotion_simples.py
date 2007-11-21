"""
    bmotion_simples.py - A port of the bmotion simple stuffs.
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

class bmotion_simples(object):
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
            "/me ducks",
            '/me hides behind %ruser',
            "Great. Now I'm gonna get a cold %VAR{unsmiles}",
            "Eek. Don't give it to me",
            "%% - I recommend %VAR{sillyThings}"])
        
        self.bot.botplugin['sleekmotion'].addValues('goonthens', ["sssh sekrit",  "go on then", "oh go on then", "ok then, but don't tell anyone"])
        
        self.bot.botplugin['sleekmotion'].addValues('here_responses',[        "%VAR{nos}"])
        
        self.bot.botplugin['sleekmotion'].addValues('notbots', ["no I'm not",
          "am not %VAR{unsmiles}",
          "am not",
          "LIES.",
          "SILENCE%FUNC{colen}",
          "LIES, ALL LIES%|(unless a witness steps forward)",
          "/me smothers %%%|shh, someone will hear",
          "shh%|sekrit"])
            
        self.about = "'bmotion_simples' Simple ports of all the bmotion simple plugins. \nBased on the bMotion plugin.\nWritten by Kevin Smith"
        
        self.bot.botplugin['sleekmotion'].registerTrigger('sneeze', '^\*?(/me sneezes|.hatsjoe|wachoo|sneezes|.a+tchoo+)', 60, 'blessyous')
        self.bot.botplugin['sleekmotion'].registerTrigger("zzz","^zzz+",50, 'handcoffees')
        self.bot.botplugin['sleekmotion'].registerTrigger("takethat","^take that!",60, ["and party!","and party"])
        self.bot.botplugin['sleekmotion'].registerTrigger("wrongsmiley",'{^L\($}', 60, ["taunt","fail","WORST. SMILEY. EVER.","try realigning your fingers for that one","E_SMILEY"])
        self.bot.botplugin['sleekmotion'].registerTrigger("bisto","^ahh+$",10, "Bisto!")
        self.bot.botplugin['sleekmotion'].registerTrigger("thinkso","^(no, )?(i|I) do(n't| not) think so",10, ["Mr Negative","I DO think so.", "and what would you know?"])
        self.bot.botplugin['sleekmotion'].registerTrigger("littlebit", "(what, )?not even a little bit", 40, "goonthens")

        self.bot.botplugin['sleekmotion'].registerTrigger("here","^any ?(one|body) (here|alive|talking)", 40, "here_responses")

        self.bot.botplugin['sleekmotion'].registerTrigger("notbot", "%botnicks('s| is) a bot", 60, "notbots")

        self.bot.botplugin['sleekmotion'].registerTrigger("arebot", "((is %botnicks a bot)|(are you a bot,? %botnicks)|(^%botnicks%:? are you a bot))", 60, "%VAR{nos}")
 

