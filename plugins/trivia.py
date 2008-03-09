"""
	trivia.py - Run a trivia game in the channel.
	Copyright (C) 2007 Kevin Smith

    SleekBot is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    SleekBot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this software; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import datetime
import time
import logging

class TriviaRepository(object):
    """ Repository of trivia questions.
    """
    
    def __init__(self, store):
        """ Boring constructor.
        """
        self.store = store
        pass
        
    def getQuestion(self):
        """ Find a question which hasn't been used too recently, and 
            return question and answer.
        """
        question = "Script's author"
        answer = "Kevin Smith"
        #FIXME
        return {'q':question, 'a':answer}
        


class TriviaGame(object):
    """ Game controller
    """
    def __init__(self, muc, repository, length, bot):
        """ Boring constructor.
        """
        self.muc = muc
        self.repository = repository
        self.length = length
        self.bot = bot
        self.bot.add_event_handler("groupchat_message", self.handleGroupchatMessage, threaded=True)
        self.bot.sendMessage(self.muc, "Starting a trivia game. This game will continue for %d turns if left unchecked" %length, mtype='groupchat')
        self.startTurn()

    def handleGroupchatMessage(self, message):
        """ Parse incoming messages
        """
        if "%s/%s" %(message['room'],message['name']) == self.bot['xep_0045'].getOurJidInRoom(self.muc):
            return
        if not message['room'] == self.muc:
            return
        self.assessAttempt(message['message'], message['name'])

    def assessAttempt(self, guess, name):
        """ Check for a successful guess.
        """
        if guess.lower() == self.question['a'].lower():
            self.correct(guess, name)
        else:
            self.incorrect(guess, name)

    def incorrect(self, guess, name):
        """ The user gave an incorrect answer.
        """
        self.bot.sendMessage(self.muc, "Sorry %s, '%s' just isn't the right answer." %(name, guess), mtype='groupchat')

    def correct(self, guess, name):
        """ User guessed correctly.
        """
        self.bot.sendMessage(self.muc, "Spot on, %s, the answer is '%s'." %(name, guess), mtype='groupchat')

    def maskAnswer(self, answer, proportion=1.0):
        """ Mask out the answer characters with underscores, with a 
            given proportion.
        """
        #FIXME
        return "_____ _____"        

    def startTurn(self):
        """ Choose a question, and start a turn.
        """
        self.question = self.repository.getQuestion()
        self.clueCount = 1
        self.bot.sendMessage(self.muc, "Question: %s" %(self.question['q']), mtype='groupchat')
        self.giveClue()

    def giveClue(self):
        """ Give an appropriate clue.
        """
        self.bot.sendMessage(self.muc, "Clue %d: %s" %(self.clueCount, self.maskAnswer(self.question['a'])), mtype='groupchat')
        self.clueCount += 1
 
    def stop(self):
        """ Stop the game.
        """
        #FIXME - unregister
        pass
        
class trivia(object):
    """ Trivia script.
    """    
    
    def __init__(self, bot, config):
        logging.debug("Firing up the trivia script.")
        self.bot = bot
        self.config = config
        self.repository = TriviaRepository(self.bot.store)
        self.about = "Run a trivia game."
        self.bot.addMUCCommand('trivia', self.handle_trivia_muc_command)
        #Something, possibly sleekbot itself, is broken and the following line
        #is needed for MUCs, too
        self.bot.addIMCommand('trivia', self.handle_trivia_muc_command)
        self.bot.addHelp('trivia', 'Trivia command', "Control a trivia game", 'trivia')
        self.games = {}
    
    def canStartGame(self, muc):
        """ Check if it's possible to start a game.
            Game must not be running, room must be allowed trivia, etc.
        """
        #FIXME
        if muc in self.games.keys():
            return False
        return True
    
    def startGame(self, muc, length):
        """ Start the game for a given number of questions.
        """
        if not self.canStartGame(muc):
            #FIXME
            pass
        self.games[muc] = TriviaGame(muc, self.repository, length, self.bot)
        
    def canStopGame(self, muc):
        """ Check if it's possible to stop a game.
            Game must be running.
        """
        if muc not in self.games.keys():
            return False
        return True

    def stopGame(self, muc):
        """ Stop a running game.
        """
        if not canStopGame(muc):
            #FIXME
            pass
        self.games[muc].stop()
        del self.games[muc]
        pass
        
    def handle_trivia_muc_command(self, command, args, msg):
        """ Trivia control.
        """
        logging.debug("Handling trivia command")
        if args == None or args == "":
            return "Please supply a trivia command to run [start|stop]"

        if self.bot.getRealJidFromMessage(msg) not in self.bot.getOwners() + self.bot.getAdmins():
            return "You do not have access to trivia functions."
                
        muc = msg['room']
        
        splitargs = args.split(" ")
        if splitargs[0] == 'start':
            length = 5
            if len(splitargs) > 1:
                length = int(splitargs[1])
            if self.canStartGame(muc):
                logging.debug("Trivia: calling startGame")
                self.startGame(muc, length)

        if args == 'stop':
            if self.canStopGame(muc):
                logging.debug("Trivia: calling stopGame")
                self.stopGame(muc)
        
