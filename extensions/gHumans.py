############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Time Helpers
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
# Title:         GeniSys NLU Time Helpers
# Description:   Time helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
############################################################################################
 
import os, time, json, hashlib, hmac 

from tools.Helpers     import Helpers
from tools.Logging     import Logging
from tools.JumpWay     import JumpWay

from datetime          import datetime

class Humans():
    
    def __init__(self):
        
        self.Helpers = Helpers()
        self.Logging = Logging()
        self.JumpWay = JumpWay()
        
        self._confs  = self.Helpers.loadConfigs()
        self.LogFile = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"Client/")
        
        self.Logging.logMessage(
            self.LogFile,
            "EXTENSIONS",
            "HUMANS",
            "Humans Extension Ready")
        
    def getHumanByFace(self, response):

        data          = {}
        headers       = {'content-type': 'application/json'}
        cameraEnpoint = self._confs["iotJumpWay"]["API"]["REST"] + "/TASS/0_1_0/checkCamera"
        
        self.Logging.logMessage(
            self.LogFile,
            "EXTENSIONS",
            "HUMANS",
            "Checking Camera...")
            
        response = self.JumpWay.apiCall(
                                        cameraEnpoint, 
                                        data, 
                                        headers)
                            
        self.Logging.logMessage(
            self.LogFile,
            "EXTENSIONS",
            "HUMANS",
            "Response: "+str(response)) 

        if response["Response"] == "OK":
            responseLength = len(response["ResponseData"])
            if responseLength == 1:
                message = "I detected " + str(responseLength) + " human, " + response["ResponseData"][0]["userid"]
            else:
                message = "I detected " + str(responseLength) + " humans, "

            return message
        else:
            
            return response["ResponseMessage"]