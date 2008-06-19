"""
    .py - A plugin for pinging Jids.
    Copyright (C) 2008 Nathan Fritz

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

class pubsub_browser(object):
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.about = "Create and configure nodes, leafs, and add items."
		self.pubsub = self.bot.plugin['xep_0060']
		self.xform = self.bot.plugin['xep_0004']
		self.adhoc = self.bot.plugin['xep_0050']
		
		createleaf = self.bot.plugin['xep_0004'].makeForm('form', "Create Leaf")
		createleaf.addField('node', 'text-single')
		self.bot.plugin['xep_0050'].addCommand('newleaf', 'Create Leaf', createleaf, self.createLeafHandler, True)

		createcollect = self.bot.plugin['xep_0004'].makeForm('form', "Create Collection")
		createcollect.addField('node', 'text-single', 'Node name')
		self.bot.plugin['xep_0050'].addCommand('newcollection', 'Create Collection', createcollect, self.createCollectionHandler, True)
		setitem = self.bot.plugin['xep_0004'].makeForm('form', "Set Item")
		setitem.addField('node', 'text-single')
		setitem.addField('id', 'text-single')
		setitem.addField('xml', 'text-multi')
		self.bot.plugin['xep_0050'].addCommand('setitem', 'Set Item', setitem, self.setItemHandler, True)
		
		confnode = self.bot.plugin['xep_0004'].makeForm('form', "Configure Node")
		confnode.addField('node', 'text-single')
		self.bot.plugin['xep_0050'].addCommand('confnode', 'Configure Node', confnode, self.updateConfigHandler, True)
	
	def getStatusForm(self, title, msg):
		status = self.xform.makeForm('form', title)
		status.addField('done', 'fixed', value=msg)
		return status

	def createLeafHandler(self, form, sessid):
		value = form.getValues()
		node = value.get('node')
		self.adhoc.sessions[sessid]['pubsubnode'] = node
		nodeform = self.pubsub.getNodeConfig(self.bot.server)
		logging.debug("nodeform: %s" % nodeform)
		if nodeform:
			return nodeform, self.createLeafHandlerSubmit, True
		else:
		#if True:
			if self.bot.plugin['xep_0060'].create_node(self.bot.server, self.adhoc.sessions[sessid]['pubsubnode']):
				return self.getStatusForm('Error', "Unable to retrieve default node configuration.\nNode without configuration was created instead."), None, False
			return self.getStatusForm('Error', "Unable to retrieve default node configuration.\nFurthermore, creating a node without a configuration failed."), None, False
	
	def createLeafHandlerSubmit(self, form, sessid):
		if not self.bot.plugin['xep_0060'].create_node(self.bot.server, self.adhoc.sessions[sessid]['pubsubnode'], form):
			return self.getStatusForm('Error', "Could not create node."), None, False
		else:
			return self.getStatusForm('Done', "Node %s created." % self.adhoc.sessions[sessid]['pubsubnode']), None, False
	
	def createCollectionHandler(self, form, sessid):
		value = form.getValues()
		node = value.get('node')
		self.adhoc.sessions[sessid]['pubsubnode'] = node
		self.bot.plugin['xep_0060'].create_node(self.bot.server, node, collection=True)
		nodeform = self.pubsub.getNodeConfig(self.bot.server, node)
		if nodeform:
			return nodeform, self.updateConfigHandler, True
	
	def updateConfigHandler(self, form, sessid):
		value = form.getValues()
		node = value.get('node')
		self.adhoc.sessions[sessid]['pubsubnode'] = node
		nodeform = self.pubsub.getNodeConfig(self.bot.server, node)
		if nodeform:
			return nodeform, self.updateConfigHandlerSubmit, True
		else:
			return self.getStatusForm('Error', 'Unable to retrieve node configuration.'), None, False
	
	def updateConfigHandlerSubmit(self, form, sessid):
		node = self.adhoc.sessions[sessid]['pubsubnode']
		self.pubsub.setNodeConfig(self.bot.server, node, form)
		return self.getStatusForm('Done', "Updated node %s." % node), None, False
	
	
	def setItemHandler(self, form, sessid):
		value = form.getValues()
		self.pubsub.setItem(self.bot.server, value['node'], {value['id']: ET.fromstring(value['xml'])})
		done = self.xform.makeForm('form', "Finished")
		done.addField('done', 'fixed', value="Published Item.")
		return done, None, False
