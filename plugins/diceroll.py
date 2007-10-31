import random
import time
import sys
import re
import traceback

class diceroll(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "A nerdy plugin for rolling complex or\nsimple dice formulas."
		self.bot.addIMCommand('roll', self.handle_roll)
		self.bot.addMUCCommand('roll', self.handle_roll)
		self.bot.addHelp('roll', 'Roll Dice Command', "Rolls dice for you.\nExample: !roll (1 + d6 + 2d10 + 5 + d4) * 2", 'roll [dice calculation]')
	
	def handle_roll(self, command, args, msg):
		try:
			d = diceCalc(args)
			return d.show()
		except:
			traceback.print_exc()
			return "Invalid dice calculation."
		
class Die(object):
	def __init__(self, sides):
		self.sides = sides
		self.value = 0
	
	def roll(self):
		self.value = random.randint(1,self.sides)
		return self.value
	
	def __mul__(self, other):
		dielist = [self]
		for x in range(1, other):
			dielist.append(Die(self.sides))
		return Dice(dielist)
	
	def __cmp__(self, other):
		if self.value > other.value:
			return 1
		if self.value < other.value:
			return -1;
		return 0
		
	def __retr__(self):
		return self.__str__()
	
	def __str__(self):
		if self.value == 0:
			self.roll()
		return "d%s: %s" % (self.sides, self.value)
		
			
class Dice(object):
	def __init__(self, dice_list):
		self.dice_list = dice_list
		self.total = 0
		self.base = 0
		self.calc = ''
		
	def roll(self):
		for ddie in self.dice_list:
			self.total += ddie.roll()
			time.sleep(random.randint(0,100) * .0001)
		self.base = self.total
		return self.total
	
	def dropLow(self, number):
		self.dice_list.sort()
		sum = 0
		for die in self.dice_list[number:] :
			sum += die.value
		return sum
	
	def dropHigh(self, number):
		self.dice_list.sort()
		sum = 0
		for die in self.dice_list[:(-1*number)] :
			sum += die.value
		return sum
		
	def __repr__(self):
		return self.show()
	
	def sort(self):
		self.dice_list.sort()
		return self
		
	def show(self):
		if self.total == 0:
			self.roll()
		output = ''
		if self.calc:
			output += "%s%s\n" % (self.base, self.calc)
		output += "Total: %s\n" % self.total
		output += ", ".join([str(x) for x in self.dice_list])
		return output
	
	def __mul__(self, other):
		if self.total == 0:
			self.roll()
		self.total = self.total * other
		self.calc += ' * %s' % other
		return self
	
	def __div__(self, other):
		if self.total == 0:
			self.roll()
		self.total = self.total / other
		self.calc += ' / %s' % other
		return self
	
	def __add__(self, other):
		if self.total == 0:
			self.roll()
		self.total = self.total + other
		self.calc += ' + %s' % other
		return self
	
	def __sub__(self, other):
		if self.total == 0:
			self.roll()
		self.total = self.total - other
		self.calc += ' - %s' % other
		return self


class diceCalc(object):
	def __init__(self, inputstr):
		self.dicesets = []
		self.inputstr = inputstr
		self.total = 0
		self.calc = inputstr
		valid = re.compile('^[0-9d()+\-*/ ]+$')
		if valid.match(inputstr) is None:
			self.total = "%s is not a valid dice calc." % inputstr
			return
		finddice = re.compile('[0-9]*d[0-9]+')
		while True:
				match = finddice.search(self.calc)
				if match is None:
					break
				print match.group()
				self.dicesets.append(self.dstring(match.group()))
				self.dicesets[-1].roll()
				self.dicesets[-1].sort()
				self.calc = self.calc[:match.start()] + str(self.dicesets[-1].total) + self.calc[match.end():]
		self.total = eval(self.calc)

	def dstring(self, inputstr):
		times, sides = inputstr.split('d', 1)
		if not times:
			times = 1
		return Die(int(sides)) * int(times)
	
	def show(self):
		#output = "%s = %s\n" % (self.calc, self.total)
		output = "Total: %s\n" % self.total
		numDice = 0
		dicelist = []
		for dice in self.dicesets:
			dice.dice_list.sort()
			for die in dice.dice_list:
				dicelist.append( str(die) )
				numDice += 1
		if numDice < 2 :
			output = ""
		output += ', '.join(dicelist)
		return output