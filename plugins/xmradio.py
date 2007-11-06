import sys
import re
import traceback
import urllib2

class xmradio(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "A plugin for seeing what's on XM Radio."
		self.bot.addIMCommand('xm', self.handle_xm)
		self.bot.addMUCCommand('xm', self.handle_xm)
		self.bot.addHelp('xm', 'XM Radio Command', "Tells you what's on XM\nExample: !xm 47", 'xm [channel number]')
	
	def handle_xm(self, command, args, msg):
		try:
			xmChan = xmChannel(args)
			return xmChan.show()
		except:
			traceback.print_exc()
			return "Invalid command. Usage: xm [channel number]"

class xmChannel(object):
	def __init__(self, inputstr):
		datapointer = urllib2.urlopen("http://xmradio.com/padData/pad_provider.jsp?channel=" + inputstr)
		self.data = datapointer.read()
		datapointer.close()
	
	def show(self):
	
		begindex = self.data.find("<artist>") + 8
		endex = self.data.find("</artist>") + 0
		artist = self.data[begindex : endex]
	
		begindex = self.data.find("<songtitle>") + 11
		endex = self.data.find("</songtitle>") + 0
		title = self.data[begindex : endex]
	
		begindex = self.data.find("<channelname>") + 13
		endex = self.data.find("</channelname>") + 0
		channelName = self.data[begindex : endex]
		
		begindex = self.data.find("<channelnumber>") + 15
		endex = self.data.find("</channelnumber>") + 0
		channelNumber = self.data[begindex : endex]
		
		output = channelNumber + " - " + channelName + " is playing \"" + title + "\" by " + artist
		if output.find("<paddata>") > 0:
			x = 4/0
		return output