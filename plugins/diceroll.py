import random
import time
import sys

class diceroll(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.bot.addIMCommand('roll', self.handle_roll)
		self.bot.addMUCCommand('roll', self.handle_roll)
		self.bot.addHelp('roll', 'Roll Dice Command', "Rolls dice for you.\nExample: !roll (1 + d6 + 2d10 + 5 + d4) * 2", 'roll [dice calculation]')
	
	def handle_roll(self, command, args, msg):
		try:
			d = diceCalc(args)
			return d.show()
		except:
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
	
	def __repr__(self):
		return self.show()
	
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
		self.calc = ''
		for word in inputstr.split(' '):
			if 'd' in word:
				newword = ''
				newcalc = ''
				for char in word:
					if char in ['1', '2', '3', '4','5','6','7','8','9','0','d']:
						newword += char
					else:
						newcalc += char
				self.dicesets.append(self.dstring(newword))
				self.dicesets[-1].roll()
				self.calc += str(self.dicesets[-1].total)
				self.calc += newcalc + ' '
			else:
				self.calc += word + ' '
		self.total = eval(self.calc)


	def dstring(self, inputstr):
		times, sides = inputstr.split('d', 1)
		if not times:
			times = 1
		return Die(int(sides)) * int(times)
	
	def show(self):
		output = "%s= %s\n" % (self.calc, self.total)
		dicelist = []
		for dice in self.dicesets:
			for die in dice.dice_list:
				dicelist.append(str(die))
		output += ', '.join(dicelist)
		return output
		

