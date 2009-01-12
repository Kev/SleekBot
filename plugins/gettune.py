import logging
from xml.etree import cElementTree as ET

class gettune(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "Get user tune info."
		self.sd = self.bot.plugin['xep_0030']
		self.sd.add_feature('http://jabber.org/protocol/tune+notify')
		self.bot.add_handler("""<message><event xmlns='http://jabber.org/protocol/pubsub#event'><items node='http://jabber.org/protocol/tune' /></event></message>""", self.handleTune)
		self.bot.addIMCommand('gettune', self.handleGettune)
		self.bot.addMUCCommand('gettune', self.handleGettune)
		self.tunes = {}
	
	def handleTune(self, xml):
		logging.info("Got Tune")
		jid = xml.get('from')
		tune = xml.find('{http://jabber.org/protocol/pubsub#event}event/{http://jabber.org/protocol/pubsub#event}item/{http://jabber.org/protocol/tune}tune')
		if tune is null:
			self.tunes[jid] = 'No tune.'
			return
		artist = tune.find('{http://jabber.org/protocol/tune}artist')
		if artist is None:
			artist = 'No Artist'
		else:
			artist = artist.text
		title = tune.find('{http://jabber.org/protocol/tune}title')
		if title is None:
			title = 'No Title'
		else:
			title = title.text
		self.tunes[jid] = "%s - %s" % (artist, title)
		
	def handleGettune(self, cmd, args, msg):
		if not args:
			output = []
			for jid in self.tunes:
				output.append("%s: %s" (jid, self.tunes[jid]))
			output = '\n'.join(output)
		else:
			output = self.tunes.get(args[0], 'No tune published.')
		return output
