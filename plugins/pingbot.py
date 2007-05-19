import logging

class pingbot(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.bot.addIMCommand('ping', self.handle_ping)
		self.bot.addMUCCommand('ping', self.handle_ping)
		self.bot.addHelp('ping', 'Ping Command', "Discover latency to a jid.", 'ping jid')
			
	def handle_ping(self, command, args, msg):
		latency = self.bot['xep_0199'].sendPing(args, 10)
		if latency == False:
			response = "No response when pinging " + args
		else:
			response = "Ping response received from " + args + " in " + str(latency) + " seconds."
		return response