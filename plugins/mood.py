import logging
from xml.etree import cElementTree as ET

class mood(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.pubsub = self.bot.plugin['xep_0060']
		self.xform = self.bot.plugin['xep_0004']
		self.adhoc = self.bot.plugin['xep_0050']
		self.moods = ['afraid', 'amazed', 'angry', 'annoyed', 'anxious', 'aroused', 'ashamed', 'bored', 'brave', 'calm', 'cold', 'confused', 'contented', 'cranky', 'curious', 'depressed', 'disappointed', 'disgusted', 'distracted', 'embarrassed', 'excited', 'flirtatious', 'frustrated', 'grumpy', 'guilty', 'happy', 'hot', 'humbled', 'humiliated', 'hungry', 'hurt', 'impressed', 'in_awe', 'in_love', 'indignant', 'interested', 'intoxicated', 'invincible', 'jealous', 'lonely', 'mean', 'moody', 'nervous', 'neutral', 'offended', 'playful', 'proud', 'relieved', 'remorseful', 'restless', 'sad', 'sarcastic', 'serious', 'shocked', 'shy', 'sick', 'sleepy', 'stressed', 'surprised', 'thirsty', 'worried']

		setmood = self.bot.plugin['xep_0004'].makeForm('form', "Set Mood")
		moods = setmood.addField('mood', 'list-single', 'Mood')
		for mood in self.moods:
			moods.addOption(mood, mood.title())
		setmood.addField('desc', 'text-single', 'Description')
		self.bot.plugin['xep_0050'].addCommand('setmood', 'Set Mood', setmood, self.setMoodHandler, True)

	def setMoodHandler(self, form, sessid):
		value = form.getValues()
		moodx = ET.Element('{http://jabber.org/protocol/mood}mood')
		moodel = ET.Element(value['mood'])
		text = ET.Element('text')
		text.text = value['desc']
		moodx.append(moodel)
		moodx.append(text)
		self.pubsub.setItem(self.bot.server, 'http://jabber.org/protocol/mood', {None:moodx})
		done = self.xform.makeForm('form', "Finished")
		done.addField('done', 'fixed', value="Mood updated.")
		return done, None, False
