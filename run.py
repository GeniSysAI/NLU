############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Engine
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
# Title:         GeniSys NLU Engine
# Description:   Serves an NLU endpoint for intent / entity classification
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
# Example Usage:
#
#   $ python3 Run.py TRAIN
#   $ python3 Run.py INPUT 
#   $ python3 Run.py LOCAL "Hi how are you?"
#   $ python3 Run.py SERVER 
#
############################################################################################
 
import sys, os, random, json, string, warnings

from flask            import Flask, Response, request

from Train            import Trainer

from tools.Helpers    import Helpers
from tools.Data       import Data
from tools.Mitie      import Entities
from tools.Model      import Model
from tools.Context    import Context
from tools.Extensions import Extensions
from tools.JumpWay    import JumpWay

app    = Flask(__name__)

class NLU():
    	
	def __init__(self):

		###############################################################
		#
		# Sets up all default requirements and placeholders 
		# needed for the NLU engine to run. 
		#
		# - Helpers: Useful global functions
		# - JumpWay/jumpWayClient: iotJumpWay class and connection
		# - Logging: Logging class
		#
		###############################################################
			
		self.isTraining    = False 
		self.ner           = None 
    		
		self.Helpers       = Helpers()
		self._confs        = self.Helpers.loadConfigs()

		self.user          = {}

		self.LogFile       = self.Helpers.setLogFile(self._confs["aiCore"]["Logs"]+"NLU/")
		self.ChatLogFile   = self.Helpers.setLogFile(self._confs["aiCore"]["Logs"]+"Chat/")

		self.jumpWay       = JumpWay()
		self.jumpWayClient = self.jumpWay.startMQTT()

		self.jumpWayClient.subscribeToDeviceChannel(self._confs["iotJumpWay"]["Channels"]["Commands"])
		self.jumpWayClient.deviceCommandsCallback = self.commandsCallback
		
	def initiateSession(self):

		###############################################################
		#
		# Initiates empty guest user session, GeniSys will ask the user 
		# verify their GeniSys user by speaking or typing if it does 
		# not know who it is speaking to. 
		#
		###############################################################

		self.userID = 0
		if not self.userID in self.user:
			self.user[self.userID] = {}
			self.user[self.userID]["history"] = {}

	def initNLU(self):

		###############################################################
		#
		# Initiates the NLU setting up the data, NLU / entities models 
		# and required modules such as context and extensions.
		#
		###############################################################

		self.Data          = Data()
		self.trainingData  = self.Data.loadTrainingData()
		self.trainedData   = self.Data.loadTrainedData()
		
		self.Model         = Model()
		self.Context       = Context()
		self.Extensions    = Extensions()

		self.restoreData()
		self.restoreNER()
		self.restoreNLU()

		self.initiateSession()
		self.setThresholds()
		
	def commandsCallback(self,topic,payload):

		###############################################################
		#
		# The callback function that is triggerend in the event of a 
		# command communication from the iotJumpWay.
		#
		###############################################################
		
		self.Helpers.logMessage(
			self.LogFile,
			"iotJumpWay",
			"INFO",
			"Recieved iotJumpWay Command Data : " + str(payload))
			
		commandData = json.loads(payload.decode("utf-8"))

	def restoreData(self):

		###############################################################
		#
		# Sets the local trained data using data retrieved above
		#
		###############################################################

		self.trainedWords   = self.trainedData["words"]
		self.trainedClasses = self.trainedData["classes"]
		self.x              = self.trainedData["x"]
		self.y              = self.trainedData["y"]
		self.intentMap      = self.trainedData["intentMap"][0]
		
	def loadEntityController(self):

		###############################################################
		#
		# Initiates the entity extractor class from tools
		#
		###############################################################

		self.entityController = Entities()
		
	def restoreNER(self):

		###############################################################
		#
		# Loads entity controller and restores the NER model
		#
		###############################################################

		self.loadEntityController()
		self.ner = self.entityController.restoreNER()
		
	def restoreNLU(self):

		###############################################################
		#
		# Restores the NLU model
		#
		###############################################################

		self.tmodel = self.Model.buildDNN(self.x, self.y) 
		
	def setThresholds(self):

		###############################################################
		#
		# Sets the threshold for the NLU engine, this can be changed
		# using arguments to commandline programs or paramters for 
		# API calls.
		#
		###############################################################

		self.threshold     = self._confs["NLU"]["Threshold"]
		self.entityThrshld = self._confs["NLU"]["Mitie"]["Threshold"]
			
	def communicate(self, sentence):

		###############################################################
		#
		# First checks to ensure that the program is not training, 
		# then parses any entities that may be in the intent, then 
		# checks context and extensions before providing a response.
		#
		###############################################################

		if self.isTraining == False:

			parsed, fallback, entityHolder, parsedSentence = self.entityController.parseEntities(
				sentence,
				self.ner,
				self.trainingData
			)
			
			classification = self.Model.predict(self.tmodel, parsedSentence, self.trainedWords, self.trainedClasses)

			if len(classification) > 0:

				clearEntities = False
				theIntent     = self.trainingData["intents"][self.intentMap[classification[0][0]]]

				if len(entityHolder) and not len(theIntent["entities"]):
					clearEntities = True

				if(self.Context.checkSessionContext(self.user[self.userID], theIntent)):

					if self.Context.checkClearContext(theIntent, 0): 
						self.user[self.userID]["context"] = ""

					contextIn, contextOut, contextCurrent = self.Context.setContexts(theIntent,self.user[self.userID])
					
					if not len(entityHolder) and len(theIntent["entities"]):
						response, entities = self.entityController.replaceResponseEntities(random.choice(theIntent["fallbacks"]), entityHolder)
						extension, extensionResponses, exEntities = self.Extensions.setExtension(theIntent)

					elif clearEntities:
						entityHolder = []
						response = random.choice(theIntent["responses"])
						extension, extensionResponses, exEntities = self.Extensions.setExtension(theIntent)

					else:
						response, entities = self.entityController.replaceResponseEntities(random.choice(theIntent["responses"]), entityHolder)
						extension, extensionResponses, exEntities = self.Extensions.setExtension(theIntent)

					if extension != None:

						classParts     = extension.split(".")
						classFolder    = classParts[0]
						className      = classParts[1]
						theEntities    = None

						if exEntities != False:
							theEntities = entities
						
						module         = __import__(classParts[0]+"."+classParts[1], globals(), locals(), [className])
						extensionClass = getattr(module, className)()
						response       = getattr(extensionClass, classParts[2])(extensionResponses, theEntities)

					return {
						"Response": "OK",
						"ResponseData": [{
							"Received": sentence,
							"Intent": classification[0][0],
							"Confidence": str(classification[0][1]),
							"Response": response,
							"Context":  [{
								"In": contextIn,
								"Out": contextOut,
								"Current": contextCurrent
							}],
							"Extension": extension,
							"Entities": entityHolder
						}]
					}

				else:

					self.user[self.userID]["context"] = ""
					contextIn, contextOut, contextCurrent = self.Context.setContexts(theIntent, self.user[self.userID])

					if fallback and fallback in theIntent and len(theIntent["fallbacks"]):
						response = self.entityController.replaceResponseEntities(random.choice(theIntent["fallbacks"]), entityHolder)
						extension, extensionResponses = None, []

					else:
						response = self.entityController.replaceResponseEntities(random.choice(theIntent["responses"]), entityHolder)
						extension, extensionResponses, exEntities = self.Extensions.setExtension(theIntent)

					if extension != None:

						classParts     = extension.split(".")
						classFolder    = classParts[0]
						className      = classParts[1]
						theEntities    = None

						if exEntities != False:
							theEntities = entities
						
						module         = __import__(classParts[0]+"."+classParts[1], globals(), locals(), [className])
						extensionClass = getattr(module, className)()
						response       = getattr(extensionClass, classParts[2])(extensionResponses, theEntities)

					else:
						response = self.entityController.replaceResponseEntities(random.choice(theIntent["responses"]), entityHolder)

					return {
						"Response": "OK",
						"ResponseData": [{
							"Received": sentence,
							"Intent": classification[0][0],
							"Confidence": str(classification[0][1]),
							"Response": response,
							"Context":  [{
								"In": contextIn,
								"Out": contextOut,
								"Current": contextCurrent
							}],
							"Extension": extension,
							"Entities": entityHolder
						}]
					}

			else:

				contextCurrent = self.Context.getCurrentContext(self.user[self.userID])

				return {
					"Response": "FAILED",
					"ResponseData": [{
						"Received": sentence,
						"Intent": "UNKNOWN",
						"Confidence": "NA",
						"Responses": [],
						"Response": random.choice(self._confs["NLU"]["defaultResponses"]),
						"Context":  [{
							"In": "NA",
							"Out": "NA",
							"Current": contextCurrent
						}],
						"Extension":"NA",
						"Entities": entityHolder
					}]
				}
		else:	

			return {
				"Response": "FAILED",
				"ResponseData": [{
					"Status": "Training",
					"Message": "NLU Engine is currently training"
				}]
			}

NLU = NLU()

@app.route("/infer", methods = ["POST"])
def infer():

	###############################################################
	#
	# Is triggered when an authorized request is made to the infer 
	# endpoint.
	#
	###############################################################

	NLU.initiateSession()

	if request.headers["Content-Type"] == "application/json":
		query = request.json
		response = NLU.communicate(query["query"])
		print(response) 
		return Response(response=json.dumps(response, indent=4, sort_keys=True), status=200, mimetype="application/json")
	
if __name__ == "__main__":
    	
	if sys.argv[1] == "TRAIN":

		###############################################################
		#
		# Is triggered when the 1st commandline line argument is TRAIN
		#
		###############################################################

		Train = Trainer(NLU.jumpWayClient)
		Train.trainModel()
		
	elif sys.argv[1] == "SERVER":

		###############################################################
		#
		# Is triggered when the 1st commandline line argument is SERVER
		#
		###############################################################

		NLU.initNLU()

		NLU.Helpers.logMessage(
			NLU.LogFile,
			"Inference",
			"INFO",
			"Inference Started In SERVER Mode") 

		app.run(host=NLU._confs["aiCore"]["IP"], port=NLU._confs["aiCore"]["Port"])
		
	elif sys.argv[1] == "INPUT":

		###############################################################
		#
		# Is triggered when the 1st commandline line argument is INPUT
		#
		###############################################################

		NLU.initNLU()
    		
		while True:

			intent = input(">")

			NLU.Helpers.logMessage(
				NLU.ChatLogFile,
				"Human",
				"Intent",
				intent)
				
			response = NLU.communicate(intent)
			
			NLU.Helpers.logMessage(
				NLU.ChatLogFile,
				"GeniSys",
				"Reponse",
				str(response["ResponseData"][0]["Response"])) 
			
			NLU.Helpers.logMessage(
				NLU.ChatLogFile,
				"GeniSys",
				"Raw Reponse",
				str(response["ResponseData"]),
				True) 