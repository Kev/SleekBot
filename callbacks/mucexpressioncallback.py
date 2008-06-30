"""
    This file is part of SleekXMPP.

    SleekXMPP is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    SleekXMPP is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SleekXMPP; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import re

class MucExpressionCallback(object):
    """Callback running a regexp against MUC messages."""
    def __init__(self, expressionString, callbackMethod):
        """ Construct a callback, matching a regexp string to muc messages.
        """
        self.expression = re.compile(expressionString)
        self.callbackMethod = callbackMethod
        self.pluginName = callbackMethod.im_class
        
    def evaluate(event):
        """ Attempt to match the 
        """