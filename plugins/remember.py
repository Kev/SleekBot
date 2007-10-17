class remember(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "Remembers events"
		self.events = []
		self.bot.add_event_handler("groupchat_message", self.handle_message_event, threaded=True)
	
	def handle_message_event(self, msg):
		print msg
