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

import random
import re

def pinkytransform(oldstring):
    output = oldstring
    if re.compile('[.!?]$').search(oldstring):
      output += "."
    output += " %VAR{narfs}"
    return output

def gollumtransform(oldstring):
    output = oldstring
    if re.compile('[.!?]$').search(oldstring):
      output += "."
    output += " %VAR{preciouses}"
    return output

def typostransform( oldstring):
    corrections = []
    wordpairs = {'the':'teh','is':'si','I':'i'}
    charpairs = {
        'z':{'new':'z\\','correct':"-\\"},
        ')':{'new':')_','correct':"-_"},
        'd':{'new':'df','correct':"-f"},
        'e':{'new':'re','correct':"-r"},
        's':{'new':'sd','correct':"-d"},
        'l':{'new':';l','correct':"-;"}
                }
    flips = [['is', 'si'], ['ome', 'oem'], ['ame', 'aem'], ['oe', 'eo'], ['aid', 'iad'], ['ers', 'ars'], ['ade', 'aed'], ['ite', 'eit'], ['hi', 'ih'], ['or', 'ro'], ['ip', 'pi'], ['ho', 'oh'], ['he', 'eh'], ['re', 'er'], ['in', 'ni'], ['lv', 'vl'], ['sec', 'sex'], ['ir', 'ri'], ['ou', 'uo'], ['ha', 'ah'], ['ui', 'iu'], ['ig', 'gi'], ['nd', 'dn']]
    outputwords = oldstring.split()
    
    typochance = 10
    
    for i in range(len(outputwords)):
        if outputwords[i] in wordpairs.keys() and random.randint(0,100) < typochance:
            corrections.append("s/%s/%s/" % (wordpairs[outputwords[i]],outputwords[i]))
            outputwords[i] = wordpairs[outputwords[i]]
            typochance *= 0.6
            continue
        for j in range(len(outputwords[i])):
            if outputwords[i][j] in charpairs.keys() and random.randint(0,100) < typochance:
                corrections.append(charpairs[outputwords[i][j]]['correct'])
                outputwords[i] = outputwords[i][:j] + charpairs[outputwords[i][j]]['new'] + outputwords[i][j+1:]
                typochance *= 0.6
    
    for i in range(len(outputwords) - 1):
        if random.randint(0,100) < typochance:
            outputwords[i] = "".join(outputwords[i:i+2])
            del outputwords[i+1]
            corrections.append('+space')
            typochance *= 0.6
            break
    output = " ".join(outputwords)

    for flip in flips:
        r = re.compile(flip[0])
        if r.search(output) and random.randint(0,100) < typochance:
            modified = re.sub(r, flip[1], output)
            corrections.append("s/%s/%s/" %(flip[1],flip[0]))
            typochance *= 0.6

    if len(corrections) > 0:
        output = output + "|" + " ".join(corrections)
    return output

class sleekmotion_outputplugins(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        plugins = []
        plugins.append({'name':'typos','function':typostransform,'probability':10})
        plugins.append({'name':'pinky','function':pinkytransform,'probability':10})
        plugins.append({'name':'gollum','function':gollumtransform,'probability':10})
        for plugin in plugins:
            self.bot.botplugin['sleekmotion'].registerOutputPlugin(plugin)