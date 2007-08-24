import logging
import Tkinter
import Queue
import thread
import time
import math
import re
from datetime import datetime
from traceback import print_exc

class eggdropbot(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.bot.addIMCommand('eggdrop', self.handle_eggdrop)
		self.bot.addMUCCommand('eggdrop', self.handle_eggdrop)
		self.bot.addHelp('eggdrop', 'Eggdrop control command', "Configure eggdrop compatability support.", 'eggdrop [args]')
		self.bot.add_event_handler("message", self.handle_message_event, threaded=True)
		self.bot.add_event_handler("groupchat_message", self.handle_muc_event, threaded=True)
		# queue of outgoing TCL
		self.queue = Queue.Queue()
		# list of incoming messages from tcl
		self.messageQueue = []
		#self.queueExec('puts "bert"')
		#TCL support scripts - these are the TCL side of the eggdrop emulation
		self.queueExec('source "plugins/eggdrop/support.tcl"')
		self.queueExec('source "plugins/eggdrop/eggdropcompat.tcl"')
		#load the user-specified eggdrop scripts
		scripts = self.config.findall('script')
		if scripts:
			for script in scripts:
				logging.info("eggdropbot.py loading script %s." % script.attrib['file'])
				self.queueExec('source "scripts/' + script.attrib['file'] + '"')
		
		thread.start_new(self.loop,())
			
	def handle_eggdrop(self, command, args, msg):
		response = "No options for eggdrop currently."
		return response
	
	def handle_muc_event(self, msg):
		body = msg.get('message', '')
		if not body:
			return
		groupchat = msg.get('room', '')
		nick = msg.get('name', '')
		self.tcl_print(body)
		source = groupchat
		quote = re.compile("'")
		body = quote.sub("\\'", body)
		doublequote = re.compile('"')
		body = doublequote.sub('\\"', body)
		#slash = re.compile('\\\\')
		#body = slash.sub('\\\\\\\\',body)
		print "Escaped output = %%%" + body + "%%%"
		self.tcl_exec('eggsupp_process_pub "' + nick + '" "' + self.get_hostmask(groupchat+'/'+nick) + '" "' + self.get_handle(nick) + '" "' + groupchat + '" "' + body + '"')
	
	def handle_message_event(self, msg):
		return
		# text = msg.get('message', '')
		# if ' ' in msg.get('message', ''):
		#	args = msg['message'].split(' ', 1)[-1]
		# else:
		#	args = ''
		# if command.startswith(prefix):
		#	if len(prefix):
		#		command = command.split(prefix, 1)[-1]
		#	if command in self.im_commands:
		#		response = self.im_commands[command](command, args, msg)
		#		if msg['type'] == 'groupchat':
		#			self.sendMessage("%s" % msg.get('room', ''), response, mtype=msg.get('type', 'groupchat'))
		#		else:
		#			self.sendMessage("%s/%s" % (msg.get('jid', ''), msg.get('resource', '')), response, mtype=msg.get('type', 'chat'))



	def eggdrop_handler_outgoing_message(self, target, body):
#		 if self.config.groupchats.has_key(target) or not body:
#			 return
		self.tcl_print(body, self.config.default_nick, 'private',
				self.get_true_jid(target))


	def eggdrop_handler_join(self, groupchat, nick):
		self.tcl_print('%s has become available' % (nick))
		self.tcl_exec('eggsupp_process_join "' + nick + '" "' +	 self.get_hostmask(nick) + '" "' + self.get_handle(nick) + '" "' + groupchat + '"')

	def eggdrop_handler_part(self, groupchat, nick):
		self.tcl_print('%s has left' % (nick))

	def tcl_print(self, text):
		self.tcl_exec('puts "' + text + '"')
		
	def tcl_exec(self, command):
		self.queueExec(command)

	def get_handle(self, nick):
		return self.get_true_jid(nick)

	def get_hostmask(self, nick):
		return self.get_true_jid(nick)

	def get_true_jid(self, nick):
		return nick

	def process_message_queue(self):
		message = self.getMessage()
		while message != None:
			print "eggdropbot.py got message " + str(message)
			tokens = message.split(" ",2)
			if tokens[0].lower() != "privmsg":
				print "I don't recognise this type of message, ignoring"
			target = tokens[1]
			body = tokens[2].lstrip(":")#.replace(':',"%%%%")
			#body = body.replace('<',"&lt;")
			#body = body.replace('>',"&lt;")
			#self.conn.msg(target, body)
			##body = body.replace(':', "%%%")
			##body = body.replace('!', "%%%")
			illegals = re.compile("[^a-zA-Z0-9!: @#$%^&*/=+-]")
			body = illegals.sub("", body)
			self.bot.sendMessage("%s" % target, body, mtype='groupchat')
			message = None
			time.sleep(1)
			#message = self.tcl.getMessage()

	def loop(self):
		self.tcl = Tkinter.Tcl()
		self.tcl.mainloop()
		lastSecond = math.floor(time.time())
		lastTime = datetime.now()
		while 1:
			newSecond = math.floor(time.time())
			secondsPassed = newSecond - lastSecond
			for i in range(math.floor(secondsPassed)):
				self.secondTick()
			newTime = datetime.now()
			if newTime.minute != lastTime.minute:
				 self.minuteTick()
				 self.timeEvent()
				 lastTime = newTime
			time.sleep(1)
			self.tryQueue()
			lastSecond = newSecond
			self.process_message_queue()

	def queueExec(self, command):
		print "Queueing command\n" + command
		self.queue.put(command)
	def minuteTick(self):
		self.queue.put("eggsupp_minute_tick")
	def secondTick(self):
		self.queue.put("eggsupp_second_tick")
	def timeEvent(self):
		now = datetime.now()
		self.queueExec("eggsupp_process_time "+str(now.minute).zfill(2)+" "+str(now.hour).zfill(2)+" "+str(now.day).zfill(2)+" "+str(now.month).zfill(2)+" "+str(now.year))
	def tryQueue(self):
		notend = True
		while notend:
			try:
				command = self.queue.get_nowait()
				if command is None:
					notend = False
				else:
					#print "command : " + command
					try:
						self.tcl.tk.call('eval', command)
					except:
						print "Tcl evaluation of '" + command + "' failed"
						print_exc()
					self.tryQueue()
			except:
				notend = False
		notend = True
		while notend:
			try:
				message = str(self.tcl.tk.call('eval', 'eggsup_get_message_queue'))
				#print "Polled tcl for messages, got '" + message + "'"
				if message == "()" or message == "":
					notend = False
				else:
					self.messageQueue.append(message)
			except:
				notend = False
			#print "breaking out"

	def getMessage(self):
		if (len(self.messageQueue) < 1):
			return None
		message = self.messageQueue[0]
		self.messageQueue[0:1] = []
		return message
