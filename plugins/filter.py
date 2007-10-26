"""
    filter.py - A SleekBot plugin to filter text.
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
from xml.etree import ElementTree as ET

class leetFilter():
    def __init__(self):
        self.mappings = {
            'a':['4','/\\','@','/-\\','^'],
            'b':['8','6','13','!3'],
            'c':['[','<','(','{'],
            'd':[')','|)','[)','0','T)'],
            'e':['3','&','£','[-'],
            'f':['|=','|#','/='],
            'g':['6','&','9','C-'],
            'h':['#','/_/','[-]','|-|','}{'],
            'i':['1','!','|',']'],
            'j':['_|','_/','(/'],
            'k':['X','|<','|(','|{'],
            'l':['1','£','|','|_'],
            'm':['|v|','|\\//|'],
            'n':['^/','/\\/','[]\\'],
            'o':['0','()','[]'],
            'p':["|*","|>","9","|7"],
            'q':['(_,)','()_','0_','<|'],
            'r':['2','|?','/2','|^','12','l2'],
            's':['5','$','z'],
            't':['7','+','-|-','1','\'][\''],
            'u':['(_)','|_|','v','L|'],
            'v':['\\/'],
            'w':['\\/\\/','vv','\\^/','\\|/'],
            'x':['%','><','}{',')('],
            'y':['j','`/'],
            'z':['2','~/_','%','>_','7_']
        }
        pass
    
    def filter(self, text):
        for i in range(len(text)):
            leets = self.mappings.get(text[i], [])
            if len(leets) == 0:
                continue
            text = text[:i] + leets[random.randint(0, len(leets) - 1)] + text[i+1:]
        return text
            

class filter(object):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.bot.addIMCommand('filter', self.handle_filter)
        self.bot.addMUCCommand('filter', self.handle_filter)
        self.bot.addHelp('filter', 'Text filter command', "Parses the text through a filter.", 'filter filtertype text')
        self.availableFilters = {}
        self.availableFilters['leet'] = leetFilter()

    def handle_filter(self, command, args, msg):
        if args == None or args == "" or len(args.split(" ")) < 2:
            return "Insufficient information, please check help."
        language = args.split(" ")[0].lower()
        text = " ".join(args.split(" ")[1:])
        if language not in self.availableFilters.keys():
            return "Language %s not available" % language
        return self.availableFilters[language].filter(text)
