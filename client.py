############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Engine API Client
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
# Title:         GeniSys NLU Engine API Client
# Description:   API client for communicating with the GeniSys AI NLU API endpoint
# Configuration: required/confs.json
# Last Modified: 2018-09-08
#
# Example Usage:
#
#   $ python3 client.py
#
############################################################################################

import sys, time, string, requests, json

from tools.Helpers  import Helpers
from tools.Logging  import Logging

class Client():
    
    def __init__(self, user):
        
        self.Helpers = Helpers()
        self.Logging = Logging()
        
        self._confs  = self.Helpers.loadConfigs()
        self.LogFile = self.Logging.setLogFile(self._confs["AI"]["Logs"]+"Client/")
        
        self.apiUrl  = self._confs["AI"]["FQDN"] + "/communicate/infer/"+user
        self.headers = {"content-type": 'application/json'}
        
        self.Logging.logMessage(
            self.LogFile,
            "CLIENT",
            "INFO",
            "GeniSys AI Client Ready")
            
if __name__ == "__main__":
    
    if sys.argv[1] == "CLASSIFY":
        
        Client = Client(sys.argv[2])
        data   = {"query": str(sys.argv[3])}
        
        Client.Logging.logMessage(
            Client.LogFile,
            "CLIENT",
            "INFO",
            "Sending string for classification...")
            
        response = requests.post(
                            Client.apiUrl,
                            data=json.dumps(data), 
                            headers=Client.headers)
                            
        Client.Logging.logMessage(
            Client.LogFile,
            "CLIENT",
            "OK",
            "Response: "+str(response)) 