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
# Last Modified: 2018-09-08
#
############################################################################################

import os, time, requests, json, hashlib, hmac, base64

from datetime      import datetime
from requests.auth import HTTPBasicAuth

from tools.Helpers import Helpers
from tools.Logging import Logging
from Train         import Trainer

class JumpWay():
    
    def __init__(self):
        
        self.Helpers = Helpers()
        self.Logging = Logging()
        
        self._confs  = self.Helpers.loadConfigs()
        self.LogFile = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"Client/")

    def createHashMac(self, secret, data):
        
        return hmac.new(bytearray(secret.encode("utf-8")), data.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()

    def apiCall(self, apiUrl, data, headers): 
        
        self.Logging.logMessage(
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
        
        self.Logging.logMessage(
            self.LogFile,
            "JUMPWAY",
            "INFO",
            "JumpWay REST Response Received: " + str(output))

        return output