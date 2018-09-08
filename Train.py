############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Engine Trainer
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
# Title:         GeniSys NLU Engine Trainer
# Description:   Trains the GeniSys NLU Engine
# Configuration: required/confs.json
# Training Data: data/training.json
# Last Modified: 2018-09-08
#
############################################################################################
 
import sys, os, json, re, time

import JumpWayMQTT.Device as jumpWayDevice

from datetime       import datetime
from tools.Helpers  import Helpers
from tools.Logging  import Logging
from tools.Data     import Data
from tools.Model    import Model
from tools.Mitie    import Entities

parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/MITIE/mitielib')

class Trainer():

	def __init__(self, jumpWay):
    		
		self.Helpers    = Helpers()
		self.Logging    = Logging()
		self.jumpwayCl  = jumpWay

		self._confs     = self.Helpers.loadConfigs()
		self.LogFile    = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"Train/")
		
		self.Logging.logMessage(
			self.LogFile,
            "LogFile",
            "INFO",
            "NLU Trainer LogFile Set")

		self.Model      = Model()
		self.Data       = Data(self.Logging, self.LogFile)
		self.words      = []
		self.classes    = [] 
		self.dataCorpus = []

		self.setupData()
		self.setupEntities()
		
	def setupData(self):

		self.trainingData = self.Data.loadTrainingData()
		
		self.Logging.logMessage(
			self.LogFile,
            "Trainer",
            "INFO",
            "Loaded NLU Training Data")

		self.words, self.classes, self.dataCorpus = self.Data.prepareData(self.trainingData)
		self.x, self.y = self.Data.finaliseData(self.classes, self.dataCorpus, self.words)
		
		self.Logging.logMessage(
			self.LogFile,
            "TRAIN",
            "INFO",
            "NLU Trainer Data Ready")
		
	def setupEntities(self):
    		
		if self._confs["ClassifierSettings"]["Entities"] == "Mitie":
				
			self.entityExtractor = Entities()
		
			self.Logging.logMessage(
				self.LogFile,
				"TRAIN",
				"OK",
				"NLU Trainer Entity Extractor Ready")
				
			self.entityExtractor.trainEntities(
				self._confs["ClassifierSettings"]["Mitie"]["ModelLocation"],
				self.trainingData
			) 
		
	def trainModel(self):
		
		while True:
			
			self.Logging.logMessage(
				self.LogFile,
				"TRAIN",
				"ACTION",
				"Ready To Begin Training ? (Yes/No)")
			userInput = input()

			if userInput == 'Yes': break
			if userInput == 'No':  exit()
    		
		humanStart    = str(datetime.now())
		trainingStart = time.time()
		
		self.Logging.logMessage(
			self.LogFile,
            "TRAIN",
            "INFO",
            "NLU Model Training At " + humanStart)

		self.jumpwayCl.publishToDeviceChannel(
				"Training",
				{
					"NeuralNet" : "NLU",
					"Start" : trainingStart,
					"End" : "In Progress",
					"Total" : "In Progress",
					"Message" : "NLU Model Training At " + humanStart
				}
			)

		print("")

		self.Model.trainDNN(
			self.x,
			self.y,
			self.words,
			self.classes)
    		
		trainingEnd  = time.time()
		trainingTime = trainingEnd - trainingStart
		humanEnd     = str(datetime.now())
		
		self.Logging.logMessage(
			self.LogFile,
            "TRAIN",
            "OK",
            "NLU Model Trained At "+ humanEnd + " In " + str(trainingEnd) + " Seconds"
        )

		self.jumpwayCl.publishToDeviceChannel(
				"Training",
				{
					"NeuralNet" : "NLU",
					"Start" : trainingStart,
					"End" : trainingEnd,
					"Total" : trainingTime,
					"Message" : "NLU Model Trained At "+ humanEnd + " In " + str(trainingEnd) + " Seconds"
				}
			)