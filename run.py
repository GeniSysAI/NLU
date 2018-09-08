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
# Last Modified: 2018-09-02
#
# Example Usage:
#
#   $ python3 run.py TRAIN
#   $ python3 run.py INPUT  1 0.5
#   $ python3 run.py LOCAL  1 0.5 "Hi how are you?"
#   $ python3 run.py SERVER
#
############################################################################################
 
import sys, os, random, json, string

import JumpWayMQTT.Device as jumpWayDevice

from   tools.Helpers import Helpers
from   tools.Logging import Logging
from   Train         import Trainer

class NLU():
    	
	def __init__(self):
    		
		self.Helpers        = Helpers()
		self.Logging        = Logging()
		self._confs         = self.Helpers.loadConfigs()
		self.LogFile        = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"NLU/")
		self.ChatLogFile    = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"Chat/")
		
		self.Logging.logMessage(
			self.LogFile,
            "NLU",
            "INFO",
            "NLU Classifier LogFile Set")
			
		self.startMQTT()
		
	def commandsCallback(self,topic,payload):
		
		self.Logging.logMessage(
			self.LogFile,
			"iotJumpWay",
			"INFO",
			"Recieved iotJumpWay Command Data : " + str(payload))
			
		commandData = json.loads(payload.decode("utf-8"))
			
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

NLU = NLU()
	
if __name__ == "__main__":
    	
	if sys.argv[1] == "TRAIN":

		Train = Trainer(NLU.jumpwayClient)
		
		Train.Logging.logMessage(
			Train.LogFile,
			"Trainer",
			"OK",
			"NLU Trainer Ready")

		Train.trainModel()