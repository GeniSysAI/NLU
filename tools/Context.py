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
# Last Modified: 2018-09-29
#
############################################################################################

class Context():
	
	def __init__(self):
		
		###############################################################
		#
		# Nothing to do
		#
		###############################################################
		pass
		
	def setContexts(self, theIntent, session):
		
		###############################################################
		#
		# Sets all contexts
		#
		###############################################################

		contextIn  = self.setContextIn(theIntent)
		contextOut = self.setContextOut(theIntent)
		context    = self.getCurrentContext(session)

		return contextIn, contextOut, context

	def setContextIn(self, intent):

		###############################################################
		#
		# Sets the current context in
		#
		###############################################################

		return intent["context"]["in"] if intent["context"]["in"] != "" else ""

	def setContextOut(self, intent):

		###############################################################
		#
		# Sets the current context out
		#
		###############################################################

		return intent["context"]["out"] if intent["context"]["out"] != "" else ""

	def checkSessionContext(self, session, intent):

		###############################################################
		#
		# Checks the current context session
		#
		###############################################################
		
		if("context" in session and intent["context"]["in"] == session["context"]): 
			return True 
		else: 
			return False

	def checkClearContext(self, intent, override=0):

		###############################################################
		#
		# Checks if we are to clear the current context
		#
		###############################################################

		return True if intent["context"]["clear"] == True or override == 1 else False

	def getCurrentContext(self, session):

		###############################################################
		#
		# Gets the current context
		#
		###############################################################

		return session["context"] if "context" in session else "NA"