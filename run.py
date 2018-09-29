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
#   $ python3 Run.py INPUT  1 0.5
#   $ python3 Run.py LOCAL  1 0.5 "Hi how are you?"
#   $ python3 Run.py SERVER 0.5
#
############################################################################################
 
import sys, os, random, json, string

import JumpWayMQTT.Device as jumpWayDevice

from   flask            import Flask, Response, request
from   tools.Helpers    import Helpers
from   tools.Logging    import Logging
from   Train            import Trainer
from   tools.Data       import Data
from   tools.Model      import Model
from   tools.Mitie      import Entities
from   tools.Context    import Context
from   tools.Mitie      import Entities
from   tools.Extensions import Extensions

parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/MITIE/mitielib')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
app    = Flask(__name__)

class NLU():
    	
	def __init__(self):
    		
		self.Helpers     = Helpers()
		self.Logging     = Logging()
		self._confs      = self.Helpers.loadConfigs()
		self.LogFile     = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"NLU/")
		self.ChatLogFile = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"Chat/")
			
		self.startMQTT()
			
	def startMQTT(self):
		
		try:
			self.jumpwayClient = jumpWayDevice.DeviceConnection({
				"locationID": self._confs["iotJumpWay"]["Location"],
				"zoneID": self._confs["iotJumpWay"]["Zone"],
				"deviceId": self._confs["iotJumpWay"]["Device"],
				"deviceName": self._confs["iotJumpWay"]["DeviceName"],
				"username": self._confs["iotJumpWay"]["MQTT"]["Username"],
				"password": self._confs["iotJumpWay"]["MQTT"]["Password"]})
			
			self.jumpwayClient.connectToDevice()
			self.jumpwayClient.subscribeToDeviceChannel("Commands")
			self.jumpwayClient.deviceCommandsCallback = self.commandsCallback
		
			self.Logging.logMessage(
				self.LogFile,
				"iotJumpWay",
				"INFO",
				"iotJumpWay Client Ready")
			
		except Exception as e:
		
			self.Logging.logMessage(
				self.LogFile,
				"iotJumpWay",
				"INFO",
				"iotJumpWay Client Initiation Failed")

			print(str(e))
			sys.exit()
		
	def commandsCallback(self,topic,payload):
		
		self.Logging.logMessage(
			self.LogFile,
			"iotJumpWay",
			"INFO",
			"Recieved iotJumpWay Command Data : " + str(payload))
			
		commandData = json.loads(payload.decode("utf-8"))
		
	def setup(self):
		
		self.Data           = Data(self.Logging, self.LogFile)
		self.Model          = Model()
		self.Context        = Context()
		self.Extensions     = Extensions()
		
		self.user           = {}
		self.ner            = None
		self.trainingData   = self.Data.loadTrainingData()
		self.trainedData    = self.Data.loadTrainedData()

		self.setTrainedData()
		self.restoreEntitiesModel()
		self.restoreModel()
		
		self.Logging.logMessage(
			self.LogFile,
			"NLU",
			"INFO",
			"NLU Ready")

	def setTrainedData(self):

		self.trainedWords   = self.trainedData["words"]
		self.trainedClasses = self.trainedData["classes"]
		self.x              = self.trainedData["x"]
		self.y              = self.trainedData["y"]
		self.intentMap      = self.trainedData["intentMap"][0]
		
	def restoreEntitiesModel(self):
			
		if os.path.exists(self._confs["ClassifierSettings"]["EntitiesDat"]):
			self.ner = named_entity_extractor(self._confs["ClassifierSettings"]["EntitiesDat"])
		
	def restoreModel(self):
		
		self.tmodel = self.Model.buildDNN(self.x, self.y) 
		
	def setupEntities(self):
    		
		if self._confs["ClassifierSettings"]["Entities"] == "Mitie":
			self.entityExtractor = Entities()
		
	def initiateSession(self, userID):
    		
		self.userID = userID
		if not self.userID in self.user:
			self.user[self.userID] = {}
			self.user[self.userID]["history"] = {}
		
	def setThresholds(self, threshold):

		self.threshold      = float(threshold)
		self.entityThrshld  = self._confs["ClassifierSettings"]["Mitie"]["Threshold"]

	def predict(self, parsedSentence):
				
		predictions = [[index, confidence] for index, confidence in enumerate(
			self.tmodel.predict([
				self.Data.makeInferenceBag(
					parsedSentence,
					self.trainedWords)])[0]) if confidence > self.threshold]
		predictions.sort(key=lambda x: x[1], reverse=True)

		classification = []
		for prediction in predictions: 
			classification.append((
				self.trainedClasses[prediction[0]], 
				prediction[1]))
				
		return classification
			
	def communicate(self, sentence, debug=False):
    		
		parsed, fallback, entityHolder, parsedSentence = self.entityExtractor.parseEntities(
			sentence,
			self.ner,
			self.trainingData
		)

		classification = self.predict(parsedSentence)

		if len(classification) > 0:

			clearEntities = False
			theIntent     = self.trainingData["intents"][self.intentMap[classification[0][0]]]

			if len(entityHolder) and not len(theIntent["entities"]):
				clearEntities = True

			if(self.Context.checkSessionContext(self.user[self.userID], theIntent)):

				if self.Context.checkClearContext(theIntent, 0): 
					self.user[self.userID]["context"] = ""

				contextIn, contextOut, contextCurrent = self.Context.setContexts(theIntent,self.user[self.userID])

				if fallback and "fallbacks" in theIntent and len(theIntent["fallbacks"]):
					response = self.entityExtractor.replaceResponseEntities(random.choice(theIntent["fallbacks"]), entityHolder)
					extension, extensionResponses = self.Extensions.setExtension(theIntent)
					
				elif "entityType" in theIntent and theIntent["entityType"] == "Numbers":
					response = random.choice(theIntent["responses"])
					extension, extensionResponses = self.Extensions.setExtension(theIntent)
					
				elif not len(entityHolder) and len(theIntent["entities"]):
					response = self.entityExtractor.replaceResponseEntities(random.choice(theIntent["fallbacks"]), entityHolder)
					extension, extensionResponses = self.Extensions.setExtension(theIntent)

				elif clearEntities:
					entityHolder = []
					response = random.choice(theIntent["responses"])
					extension, extensionResponses = self.Extensions.setExtension(theIntent)

				else:
					response = self.entityExtractor.replaceResponseEntities(random.choice(theIntent["responses"]), entityHolder)
					extension, extensionResponses = self.Extensions.setExtension(theIntent)

				if extension != None:

					classParts     = extension.split(".")
					classFolder    = classParts[0]
					className      = classParts[1]
					module         = __import__(classParts[0]+"."+classParts[1], globals(), locals(), [className])
					extensionClass = getattr(module, className)()
					response       = getattr(extensionClass, classParts[2])(random.choice(extensionResponses))

				return {
					"Response": "OK",
					"ResponseData": [{
						"Received": sentence,
						"Intent": classification[0][0],
						"Confidence": str(classification[0][1]),
						"Response": response,
						"ContextIn": contextIn,
						"ContextOut": contextOut,
						"Context": contextCurrent,
						"Extension": extension,
						"Entities": entityHolder
					}]
				}

			else:

				self.user[self.userID]["context"] = ""
				contextIn, contextOut, contextCurrent = self.Context.setContexts(theIntent, self.user[self.userID])

				if fallback and fallback in theIntent and len(theIntent["fallbacks"]):
					response = self.entityExtractor.replaceResponseEntities(random.choice(theIntent["fallbacks"]), entityHolder)
					extension, extensionResponses = None, []

				else:
					response = self.entityExtractor.replaceResponseEntities(random.choice(theIntent["responses"]), entityHolder)
					extension, extensionResponses   = self.Extensions.setExtension(theIntent)

				if extension != None:

					classParts     = extension.split(".")
					classFolder    = classParts[0]
					className      = classParts[1]
					module         = __import__(classParts[0]+"."+classParts[1], globals(), locals(), [className])
					extensionClass = getattr(module, className)()
					response       = getattr(extensionClass, classParts[2])(random.choice(extensionResponses))

				else:
					response = self.entityExtractor.replaceResponseEntities(random.choice(theIntent["responses"]), entityHolder)

				return {
					"Response": "OK",
					"ResponseData": [{
						"Received": sentence,
						"Intent": classification[0][0],
						"Confidence": str(classification[0][1]),
						"Response": response,
						"ContextIn": contextIn,
						"ContextOut": contextOut,
						"ContextCurrent": contextCurrent,
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
					"Response": random.choice(self._confs["ClassifierSettings"]["defaultResponses"]),
					"ContextIn": "NA",
					"ContextOut": "NA",
					"ContextCurrent": contextCurrent,
					"Extension":"NA",
					"Entities": entityHolder
				}]
			}

NLU = NLU()

@app.route("/infer/<int:userId>", methods = ["POST"])
def infer(userId):

	NLU.initiateSession(userId)

	if request.headers["Content-Type"] == "application/json":
		query = request.json
		response = NLU.communicate(query["query"])
		print(response) 
		return Response(response=json.dumps(response, indent=4, sort_keys=True), status=200, mimetype="application/json")
	
if __name__ == "__main__":
    	
	if sys.argv[1] == "TRAIN":

		Train = Trainer(NLU.jumpwayClient)

		Train.Logging.logMessage(
			Train.LogFile,
			"Trainer",
			"OK",
			"NLU Trainer Ready")

		Train.trainModel()
		
	elif sys.argv[1] == "SERVER":

		NLU.setup()
		NLU.setupEntities()
		NLU.setThresholds(sys.argv[2])

		NLU.Logging.logMessage(
			NLU.LogFile,
			"Inference",
			"INFO",
			"Inference Started In SERVER Mode") 

		app.run(host=NLU._confs["AI"]["IP"], port=NLU._confs["AI"]["Port"])
		
	elif sys.argv[1] == "INPUT":

		NLU.setup()
		NLU.setupEntities()

		NLU.Logging.logMessage(
			NLU.LogFile,
			"Inference",
			"INFO",
			"Inference Started In INPUT Mode") 

		NLU.initiateSession(sys.argv[2])
		NLU.setThresholds(sys.argv[3])
    		
		while True:

			intent = input(">")

			NLU.Logging.logMessage(
				NLU.ChatLogFile,
				"Human",
				"Intent",
				intent,
				True)
				
			response = NLU.communicate(intent)
			
			NLU.Logging.logMessage(
				NLU.ChatLogFile,
				"GeniSys",
				"Raw Reponse",
				str(response["ResponseData"])) 