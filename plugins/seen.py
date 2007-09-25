import datetime, time

class seenstore(object):
	def __init__(self):
		self.null = None
		self.data = {}
		self.loaddefault()
		
	
	def update(self, nick):
		print "updating seen for " + nick
		self.data[nick.lower()] = fact
		self.savedefault()

		
	def get(self, nick):
		if self.data.has_key(nick.lower()):
			return self.data[term.lower()]
		return "I have never seen " + nick
		
	def delete(self, nick):
		if self.data.has_key(nick.lower()):
			del self.data[nick.lower()]
			self.savedefault()
	
	def loaddefault(self):
		self.load("seen.dat")
		
	def savedefault(self):
		self.save("seen.dat")
		
	def load(self, filename):
		try:
			f = open(filename, 'rb')
		except:
			print """Error loading seen data"""
			return
		self.data = pickle.load(f)
		f.close()

	def save(self, filename):
		try:
			f = open(filename, 'wb')
		except IOError:
			print """Error saving seen data"""
			return
		pickle.dump(self.data, f)
		f.close()

class seen(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.seenstore = seenstore()
		self.about = "Allows users to query the last time a sure was seen."
		self.bot.addIMCommand('seen', self.handle_seen_request)
		self.bot.addMUCCommand('seen', self.handle_seen_request)
		self.bot.addHelp('seen', 'Last seen Command', "See when a user was last seen", 'seen')
		self.started = datetime.timedelta(seconds = time.time())
	
	def handle_seen_request(self):
		if args == None or args == "":
			return "Please supply a a nickname to search for"
		return "'" + args + "' was last seen in one of my conferences " + self.seenstore.get(args)