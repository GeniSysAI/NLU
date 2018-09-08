############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Context Helper
# Copyright (C) 2018 Adam Milton-Barker (AdamMiltonBarker.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Title:         GeniSys NLU Context Helper
# Description:   Context helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-02
#
############################################################################################

class Context():

	def setContexts(self, theIntent, session):
		
		contextIn  = self.setContextIn(theIntent)
		contextOut = self.setContextOut(theIntent)
		context    = self.getCurrentContext(session)
		
		return contextIn, contextOut, context

	def checkClearContext(self, intent, override=0):

		return True if "contextOut" in intent or override == 1 else "NA"

	def setContextIn(self, intent):

		return intent["contextIn"] if "contextIn" in intent else "NA"

	def setContextOut(self, intent):

		return intent["contextOut"] if "contextOut" in intent else "NA"

	def getCurrentContext(self, session):

		return session["context"] if "context" in session else "NA"

	def checkSessionContext(self, session, intent):

		if("context" in session and "contextIn" in intent and intent["contextIn"] == session["context"]) or not "context" in session or session["context"]=="": 
			return True 
		else: 
			return False