############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Extension Core
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
# Title:         GeniSys NLU Extension Core
# Description:   Core extension functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
############################################################################################

import os, time, json, importlib

from datetime import datetime

class Extensions():

    def __init__(self):
        pass

    def setExtension(self, intent):

        extensionResponses = []
        extension = intent["extension"]["function"] if "function" in intent["extension"] and intent["extension"]["function"] !="" else None

        if extension != None:
            extensionResponses = intent["extension"]["responses"]

        return extension, extensionResponses