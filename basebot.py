import logging

class basebot(object):
	def __init__(self):
		self.im_commands = {}
		self.im_prefix = '/'
		self.muc_commands = {}
		self.muc_prefix = '!'
		self.polls = []
		self.help = []
		self.addIMCommand('help', self.handle_help)
		self.addMUCCommand('help', self.handle_help)
		self.addHelp('help', 'Help Command', "Returns this list of help commands if no topic is specified.  Otherwise returns help on the specific topic.", 'help [topic]')
		self.add_event_handler("message", self.handle_message_event)
		self.add_event_handler("groupchat_message", self.handle_message_event)
	
	def handle_message_event(self, msg):
		if msg['type'] == 'groupchat':
			prefix = self.muc_prefix
		else:
			prefix = self.im_prefix
		command = msg.get('message', '').split(' ', 1)[0]
		if ' ' in msg.get('message', ''):
			args = msg['message'].split(' ', 1)[-1]
		else:
			args = ''
		if command.startswith(prefix):
			if len(prefix):
				command = command.split(prefix, 1)[-1]
			if command in self.im_commands:
				response = self.im_commands[command](command, args, msg)
				if msg['type'] == 'groupchat':
					self.sendMessage("%s" % msg.get('room', ''), response, mtype=msg.get('type', 'groupchat'))
				else:
					self.sendMessage("%s/%s" % (msg.get('jid', ''), msg.get('resource', '')), response, mtype=msg.get('type', 'chat'))
	
	def handle_help(self, command, args, msg):
		response = ''
		if not args:
			response += "Commands:\n"
			for topic in self.help:
				response += "%s -- %s\n" % (topic[0], topic[1])
			args = 'help'
			response += "---------\n"
		found = False
		for topic in self.help:
			if topic[0] == args:
				found = True
				break
		if found:
			response += "%s\n" % topic[1]
			if topic[3]:
				response += "Usage: %s%s\n" % (self.im_prefix, topic[3])
			response += topic[2]
		return response
	
	def addHelp(self, command, title, body, usage=''):
		self.help.append((command, title, body, usage))
	
	def addIMCommand(self, command, pointer):
		self.im_commands[command] = pointer
	
	def addMUCCommand(self, command, pointer):
		self.muc_commands[command] = pointer
