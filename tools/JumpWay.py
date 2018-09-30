############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU JumpWay REST Helpers
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
# Title:         GeniSys NLU JumpWay REST Helpers
# Description:   iotJumpWay REST helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
############################################################################################

import os, sys, time, requests, json, hashlib, hmac, base64

import JumpWayMQTT.Device as jumpWayDevice

from datetime      import datetime
from requests.auth import HTTPBasicAuth

from tools.Helpers import Helpers
from tools.Logging import Logging
from Train         import Trainer

class JumpWay():
    
    def __init__(self):
        
        self.Helpers = Helpers()
        self._confs  = self.Helpers.loadConfigs()
        self.LogFile = self.Helpers.setLogFile(self._confs["aiCore"]["Logs"]+"JumpWay/")
        
    def startMQTT(self):

        ###############################################################
        #
        # Starts an iotJumpWay MQTT connection
        #
        ###############################################################
        
        try:
            
            self.jumpwayClient = jumpWayDevice.DeviceConnection({
				"locationID": self._confs["iotJumpWay"]["Location"],
				"zoneID": self._confs["iotJumpWay"]["Zone"],
				"deviceId": self._confs["iotJumpWay"]["Device"],
				"deviceName": self._confs["iotJumpWay"]["DeviceName"],
				"username": self._confs["iotJumpWay"]["MQTT"]["Username"],
				"password": self._confs["iotJumpWay"]["MQTT"]["Password"]})
                
            self.jumpwayClient.connectToDevice()
            
            self.Helpers.logMessage(
				self.LogFile,
				"iotJumpWay",
				"INFO",
				"iotJumpWay Client Ready")
                
            return self.jumpwayClient
            
        except Exception as e:
            
            self.Helpers.logMessage(
				self.LogFile,
				"iotJumpWay",
				"INFO",
				"iotJumpWay Client Initiation Failed")
                
            print(str(e))
            sys.exit()

    def createHashMac(self, secret, data):

        ###############################################################
        #
        # Creates a hash
        #
        ###############################################################

        return hmac.new(bytearray(secret.encode("utf-8")), data.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()
    
    def apiCall(self, apiUrl, data, headers):
        
        self.Helpers.logMessage(
            self.LogFile,
            "JUMPWAY",
            "INFO",
            "Sending JumpWay REST Request")
            
        response = requests.post(
                        apiUrl, 
                        data=json.dumps(data), 
                        headers=headers, 
                        auth=HTTPBasicAuth(
                                    self._confs["iotJumpWay"]["App"], 
                                    self.createHashMac(
                                                self._confs["iotJumpWay"]["API"]["Secret"],
                                                self._confs["iotJumpWay"]["API"]["Secret"])))
                                                
        output = json.loads(response.content)
        
        self.Helpers.logMessage(
            self.LogFile,
            "JUMPWAY",
            "INFO",
            "JumpWay REST Response Received: " + str(output))
    
        return output