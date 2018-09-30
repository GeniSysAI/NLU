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
# Last Modified: 2018-09-29
#
############################################################################################
 
import sys, os, json, re, time, warnings

import JumpWayMQTT.Device as jumpWayDevice

from tools.Helpers  import Helpers
from tools.Logging  import Logging
from tools.Data     import Data
from tools.Model    import Model
from tools.Mitie    import Entities

if not sys.warnoptions:
	warnings.simplefilter("ignore")

class Trainer():

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

	def __init__(self, jumpWay): 
    		
		self.Helpers    = Helpers()
		self._confs     = self.Helpers.loadConfigs()
		self.LogFile    = self.Helpers.setLogFile(self._confs["aiCore"]["Logs"]+"Train/")

		self.jumpwayCl  = jumpWay

		self.intentMap  = {}
		self.words      = []
		self.classes    = [] 
		self.dataCorpus = []
		
		self.Model      = Model()
		self.Data       = Data()
		
	def setupData(self):

		self.trainingData = self.Data.loadTrainingData()

		self.words, self.classes, self.dataCorpus, self.intentMap = self.Data.prepareData(self.trainingData)
		self.x, self.y = self.Data.finaliseData(self.classes, self.dataCorpus, self.words)
		
		self.Helpers.logMessage(
			self.LogFile,
			"TRAIN",
			"INFO",
			"NLU Training Data Ready")
		
	def setupEntities(self):
    		
		if self._confs["NLU"]["Entities"] == "Mitie":
				
			self.entityController = Entities()
				
			self.entityController.trainEntities(
				self._confs["NLU"]["Mitie"]["ModelLocation"],
				self.trainingData) 
		
			self.Helpers.logMessage(
				self.LogFile,
				"TRAIN",
				"OK",
				"NLU Trainer Entities Ready")
		
	def trainModel(self):
		
		while True:
			
			self.Helpers.logMessage(
				self.LogFile,
				"TRAIN",
				"ACTION",
				"Ready To Begin Training ? (Yes/No)")

			userInput = input(">")

			if userInput == 'Yes': break
			if userInput == 'No':  exit()

		self.setupData()
		self.setupEntities()
    		
		humanStart, trainingStart = self.Helpers.timerStart()

		self.jumpwayCl.publishToDeviceChannel(
			"Training",
			{
				"NeuralNet" : "NLU",
				"Start" : trainingStart,
				"End" : "In Progress",
				"Total" : "In Progress",
				"Message" : "NLU Model Training At " + humanStart})

		self.Model.trainDNN(
			self.x,
			self.y,
			self.words,
			self.classes,
			self.intentMap)
    		
		trainingEnd, trainingTime, humanEnd = self.Helpers.timerEnd(trainingStart)
		
		self.Helpers.logMessage(
			self.LogFile,
			"TRAIN",
			"OK",
			"NLU Model Trained At "+ humanEnd + " In " + str(trainingEnd) + " Seconds")

		self.jumpwayCl.publishToDeviceChannel(
			"Training",
			{
				"NeuralNet" : "NLU",
				"Start" : trainingStart,
				"End" : trainingEnd,
				"Total" : trainingTime,
				"Message" : "NLU Model Trained At "+ humanEnd + " In " + str(trainingEnd) + " Seconds"})