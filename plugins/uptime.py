import logging
import datetime, time

class uptime(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "Allows users to query the bot's uptime."
		self.bot.addIMCommand('uptime', self.handle_uptime)
		self.bot.addMUCCommand('uptime', self.handle_uptime)
		self.bot.addHelp('uptime', 'Uptime Command', "See how long the bot has been up", 'uptime')
		self.started = datetime.timedelta(seconds = time.time())
			
	def handle_uptime(self, command, args, msg):
		now = datetime.timedelta(seconds = time.time())
		diff = now - self.started
		days = diff.days
		seconds = diff.seconds
		weeks = hours = minutes = 0
		weeks = days / 7
		days -= weeks * 7
		hours = seconds / 3600
		seconds -= hours * 3600
		minutes = seconds / 60
		seconds -= minutes * 60
		return "%s weeks %s days %s hours %s minutes %s seconds" % (weeks, days, hours, minutes, seconds)
		

