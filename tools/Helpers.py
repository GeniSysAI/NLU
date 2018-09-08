############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Helpers
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
# Title:         GeniSys NLU Helpers
# Description:   Helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-08
#
############################################################################################

import os, json

class Helpers():

    def __init__(self):

        pass

    def loadConfigs(self):

        with open("required/confs.json") as configs:
            configs = json.loads(configs.read())
        return configs

    def setAction(self, intent):

        return intent["action"] if "action" in intent else "NA"