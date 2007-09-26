import datetime
import time
import pickle

class seenstore(object):
    def __init__(self):
        self.null = None
        self.data = {}
        self.loaddefault()
        
    
    def update(self, nick, seenData):
        self.data[nick.lower()] = seenData
        self.savedefault()

        
    def get(self, nick):
        if self.data.has_key(nick.lower()):
            return self.data[nick.lower()]
        return None
        
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
        self.bot.add_event_handler("groupchat_presence", self.handle_groupchat_presence, threaded=True)
    
    def handle_groupchat_presence(self, presence):
        """ Keep track of the presences in mucs.
        """
        presence['dateTime'] = datetime.datetime.now()
        self.seenstore.update(presence['nick'], presence)
        
    
    def handle_seen_request(self, command, args, msg):
        if args == None or args == "":
            return "Please supply a a nickname to search for"
        seenData = self.seenstore.get(args)
        if seenData == None:
            return "I have never seen '" + args + "'"
        sinceTimeSeconds = (datetime.datetime.now() - seenData['dateTime']).seconds
        sinceTime = ""
        if sinceTimeSeconds >= 3600:
            sinceTime = "%d hours ago" % (sinceTimeSeconds / 3600)
        elif sinceTimeSeconds >= 60:
            sinceTime = "%d minutes ago" % (sinceTimeSeconds / 60)
        else:
            sinceTime = "%d seconds ago" % sinceTimeSeconds
        status = ""
        if seenData['status'] != None:
            status = "(%s)" % seenData['status']
        state = "in"
        if 'type' in seenData.keys() and seenData['type'] == 'unavailable':
            state = "leaving"
        #if seenData['show'] == None:
        #    state = "joining"
        return "'%s' was last seen %s %s %s %s"  %(args, state, seenData['room'], sinceTime, status)