import logging
import pickle

class factstore(object):
	def __init__(self):
		self.null = None
		self.data = {}
		self.loaddefault()
		

	def list_terms(self):
		return self.data.keys()
	
	def add(self, term, fact):
		print "factadd"
		self.data[term.lower()] = fact
		print "factadd2"
		self.savedefault()
		print "factadded"
		
	def get(self, term):
		if self.data.has_key(term.lower()):
			return self.data[term.lower()]
		return "No facts known about " + term
		
	def delete(self, term):
		if self.data.has_key(term.lower()):
			del self.data[term.lower()]
			self.savedefault()
	
	def loaddefault(self):
		self.load("factoids.dat")
		
	def savedefault(self):
		self.save("factoids.dat")
		
	def load(self, filename):
		try:
			f = open(filename, 'rb')
		except:
			print """Error loading factoids"""
			return
		self.data = pickle.load(f)
		f.close()

	def save(self, filename):
		try:
			f = open(filename, 'wb')
		except IOError:
			print """Error saving factoids"""
			return
		pickle.dump(self.data, f)
		f.close()

class factoidbot(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.factstore = factstore()
		self.bot.addIMCommand('fact', self.handle_fact)
		self.bot.addMUCCommand('fact', self.handle_fact)
		self.bot.addHelp('fact', 'Factoid Command', "Returns facts.", 'fact [topic]')
		self.bot.addIMCommand('factoid', self.handle_fact)
		self.bot.addMUCCommand('factoid', self.handle_fact)
			
	def handle_fact(self, command, args, msg):
		subcommand = None
		term = None
		fact = None
		if args.count(" ") > 1:
			[subcommand, term, fact] = args.split(" ",2)
		elif args.count(" ") > 0:
			[subcommand, term] = args.split(" ",1)
		else:
			subcommand = args
		print "handle_fact, "+command+", "+args+", "+subcommand	
		admin_commands = ['list', 'modadd', 'moddelete']
		
		#non-admin commands
		if subcommand not in admin_commands:
			response = "facts for " + args + "\n" + args + ": " + self.factstore.get(args)
			return response
		
		#admin commands
			
		if "list" == subcommand:
			terms = self.factstore.list_terms()
			response = "I know about the following topics:\n"
			for term in terms:
				response = response + "\t" + term
			response = response + "."
		elif "modadd" == subcommand:
			print "add"
			if term != None and fact != None:
				print "ad"
				self.factstore.add(term, fact)
				response = "Fact added"
			else:
				response = "To add a fact, both a topic and description are needed."
			print "addedish"
		elif "moddelete" == subcommand:
			self.factstore.delete(term)
			response = "Deleted (if found)"
		print "handle_fact done: "+response
		return response


