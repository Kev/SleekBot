import re
import cPickle
import logging
import random
import thread
import time
import copy

class remember(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "Remembers events"
		self.know = []
		self.loaddefault()
		self.idlemin = int(self.config.get('idlemin', 60))
		self.idlemax = int(self.config.get('idlemax', 600))
		self.bot.add_event_handler("groupchat_message", self.handle_message_event, threaded=True)
		self.search = re.compile("(([Tt]he|[mM]y)[\s\w\-0-9]+ (is|are|can|has|got)|I am|i am|I'm|(?=^|,|\.\s|\?)?[\w'0-9\-]+ (is|are|can|got|has))[\s\w'0-9\-]+")
		self.prep = ["Let's see... %s.", '%s.', 'I know that %s.', 'I heard that %s.', 'Rumor has it that %s.', 'Did you hear that %s?', 'A little bird told me that %s.', '%s?!??!']
		self.bot.addIMCommand('know', self.handle_know_request)
		self.bot.addMUCCommand('know', self.handle_know_request)
		self.bot.addHelp('know', 'Random knowledge command.', "Get a random tidbit the bot has picked up", '!know')
		self.running = True
		self.lastroom = None
		self.lastmessage = ''
		thread.start_new(self.idle, tuple())
	
	def idle(self):
		while self.running:
			time.sleep(random.randint(self.idlemin, self.idlemax))
			if self.lastroom:
				msg = self.lastmessage.split(' ')
				msgs = copy.copy(msg)
				for word in msgs:
					if len(word) < 5:
						msg.remove(word)
				if len(msg) > 0:
					searchword = msg[random.randint(0, len(msg) - 1)]
					reply = self.searchKnow(searchword)
					if not reply:
						reply = self.knowledge()
				else:
					reply = self.knowledge()
				self.bot.sendMessage(self.lastroom, reply, mtype='groupchat')
	
	def handle_know_request(self, command, args, msg):
		if args:
			search = args
		else:
			search = None
		return self.knowledge(search)
	
	def getRandomKnow(self):
		return self.know[random.randint(0, len(self.know) - 1)]
	
	def searchKnow(self, search):
		found = []
		for know in self.know:
			if search in know:
				found.append("%s  " % self.wrapKnow(know))
		if not found:
			return False
		found = found[random.randint(0, len(found) - 1)]
		return found
		
	
	def knowledge(self, search=None):
		if len(self.know) > 0:
			if search:
				found = self.searchKnow(search)
				if not found:
					found = "I don't know anything about %s." % search
			else:
				found = self.wrapKnow(self.getRandomKnow())
			return found
		return "I know nothing."
	
	def wrapKnow(self, know):
		r = "%s" % (self.prep[random.randint(0, len(self.prep) - 1)]) % (know,)
		r = r[0].upper() + r[1:]
		return r
		
	
	def handle_message_event(self, msg):
		self.lastroom = msg['room']
		if self.bot.rooms[msg['room']] != (msg['name']) and not msg['message'].startswith('!'):
			self.lastmessage = msg['message']
			self.command = re.compile("^%s.*know.*?" % self.bot.rooms[msg['room']])
			match = self.command.search(msg['message'])
			if match:
				self.bot.sendMessage(msg['room'], self.knowledge(), mtype='groupchat')
				return
			match = self.search.search(msg['message'])
			if match:
				who = None
				match = match.group()
				match = match.lower()
				if not match.startswith(('what','where','why','how','when','who', 'that', 'it', 'they')):
					for person in self.bot.plugin['xep_0045'].rooms[msg['room']].keys():
						if person.lower() in msg['message'].lower():
							match = match.replace("your", "%s's" % person)
							match = match.replace('you are', "%s is" % person)
							break
					match = match.replace('my', "%s's" % msg['name'], 1)
					match = match.replace('my', "his")
					match = match.replace('i am', '%s is' % msg['name'])
					match = match.replace("i'm", '%s is' % msg['name'])
					match = match.replace(" i ", ' %s ' % msg['name'])
					match = match.replace("i've", "%s has" % msg['name'])
					match = match.strip()
					if match not in self.know:
						logging.debug("Appending knowledge: %s" % match)
						self.know.append(match)
    
	def loaddefault(self):
		self.load("remember.dat")
		
	def savedefault(self):
		self.save("remember.dat")
		
	def load(self, filename):
		try:
			f = open(filename, 'rb')
		except:
			logging.error("Error loading remember-plugin data")
			return
		self.know = cPickle.load(f)
		f.close()

	def save(self, filename):
		try:
			f = open(filename, 'wb')
		except IOError:
			logging.error("Error saving remember-plugin data")
			return
		cPickle.dump(self.know, f)
		f.close()

	def shutDown(self):
		self.savedefault()
