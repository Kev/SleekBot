"""
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
import logging
from xml.etree import cElementTree as ET

class oauth(object):
	def __init__(self, bot, config):
		self.bot = bot
		#print dir(self.bot)
		self.config = config
		self.xmpp = self.bot
		self.bot.add_handler("<iq type='get' xmlns='jabber:client'><query xmlns='urn:xmpp:oauth:request' /></iq>", self.handleOAuthRequest, threaded=True)
		self.bot.add_handler("<iq type='get' xmlns='jabber:client'><query xmlns='urn:xmpp:oauth:access' /></iq>", self.handleOAuthAccess, threaded=True)

	def handleOAuthRequest(self, xml):
		oauth = xml.find('{urn:xmpp:oauth:request}query/{urn:xmpp:oauth}oauth')
		id = xml.get('id','0')
		if oauth is None:
			error = self.xmpp.makeIqError(id)
			error.append(self.xmpp.makeStanzaError(self.xmpp.makeStanzaErrorCondition('bad-request'), 'cancel'))
			self.xmpp.send(error)
			return
		# check signature
		# generate random token and secret
		# store in DB
		r = self.xmpp.makeIqResult(id)
		q = ET.Element('{urn:xmpp:oauth:request}query')
		r.append(q)
		q.append(self.makeOAuthToken('requestkey', 'requestsecret'))
		self.xmpp.send(r)

	def handleOAuthAccess(self, xml):
		oauth = xml.find('{urn:xmpp:oauth:access}query/{urn:xmpp:oauth}oauth')
		id = xml.get('id','0')
		if oauth is None:
			error = self.xmpp.makeIqError(id)
			error.append(self.xmpp.makeStanzaError(self.makeStanzaErrorCondition('bad-request'), 'cancel'))
			return
		# check signature
		# check status of request token
		# generate random token and secret
		# store in DB
		r = self.xmpp.makeIqResult(id)
		q = ET.Element('{urn:xmpp:oauth:request}query')
		r.append(q)
		q.append(self.makeOAuthToken('accesskey', 'accesssecret'))
		self.xmpp.send(r)

	def makeOAuthToken(self, token, secret):
		oauth = ET.Element('{urn:xmpp:oauth:token}oauth')
		tokenxml = ET.Element('oauth_token')
		tokenxml.text = token
		secretxml = ET.Element('oauth_token_secret')
		secret.text = secret
		oauthxml.append(tokenxml)
		oauth.append(secretxml)
		return oauth
