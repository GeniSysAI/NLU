############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU MySql Helper
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
# Title:         GeniSys NLU MySql Helper
# Description:   MySql helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
############################################################################################

import sys, os, time, pymysql, json

from datetime      import datetime
from tools.Helpers import Helpers
 
class MySql():

    def __init__(self):

		###############################################################
		#
		# Sets up all default requirements and placeholders 
		# needed for the MySql connection. 
		#
		# - Helpers: Useful global functions
		#
		###############################################################

        self.Helpers = Helpers()
        self._confs  = self.Helpers.loadConfigs()

        self.mysqlDbConn = None
        self.mysqlDbCur  = None

        self.mysqlConnect()

    def mysqlConnect(self):

		###############################################################
		#
		# Connects to MySql using configuration in required/confs.json
		#
		###############################################################

        try:
            self.mysqlDbConn = pymysql.connect(
                                        host = self._confs["aiCore"]["IP"],
                                        user = self._confs["MySql"]["dbusername"],
                                        passwd = self._confs["MySql"]["dbpassword"],
                                        db = self._confs["MySql"]["dbname"])
        except Exception as errorz:
            print('FAILED')
            print(errorz)

    def setMysqlCursor(self):

        try:
            self.mysqlDbCur = self.mysqlDbConn.cursor()
        except Exception as errorz:
            print('FAILED')
            print(errorz)

    def setMysqlCursorRows(self):

        try:
            self.mysqlDbCur = self.mysqlDbConn.cursor(pymysql.cursors.DictCursor)
        except Exception as errorz:
            print('FAILED')
            print(errorz)