############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Human Helpers
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
# Title:         GeniSys NLU Human Helpers
# Description:   Human helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
############################################################################################
 
import os, time, json, hashlib, hmac, random 

from tools.Helpers     import Helpers
from tools.Logging     import Logging
from tools.JumpWay     import JumpWay
from tools.MySql       import MySql

from datetime          import datetime

class gHumans():
    
    def __init__(self):

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
        
        self.Helpers = Helpers()
        self._confs  = self.Helpers.loadConfigs()

        self.JumpWay = JumpWay()

        self.MySql   = MySql()
        self.MySql.setMysqlCursorRows()

        self.Logging = Logging()
        self.LogFile = self.Logging.setLogFile(self._confs["aiCore"]["Logs"]+"Client/")
        
    def getHumanByFace(self, response, entities = None):

        ###############################################################
        #
        # Checks to see who was seen in the system camera within the 
        # last few seconds
        #
        ###############################################################

        results       = None
        resultsLength = None

        try:
            self.MySql.mysqlDbCur.execute("SELECT users.id, users.name, users.zone FROM a7fh46_users_logs logs INNER JOIN a7fh46_users users ON logs.uid = users.id  WHERE logs.timeSeen > (NOW() - INTERVAL 10 SECOND) ")

            results       =  self.MySql.mysqlDbCur.fetchall()
            resultsLength = len(results)

            if resultsLength > 0:
                if resultsLength == 1: message = "I detected " + str(responseLength) + " human, #"+str(results[0]["id"])+ " " + results[0]["name"]
                else: message = "I detected " + str(responseLength) + " humans"
            else:
                message = "I didn't detect any humans in the system camera feed, please stand in front of the camera"

            return message

        except Exception as errorz:
            print('FAILED1')
            print(errorz)
            return results
        
    def getCurrentHuman(self, responses, entities = None):

        ###############################################################
        #
        # Checks to see who was seen in the system camera within the 
        # last few seconds
        #
        ###############################################################

        results       = None
        resultsLength = None

        try:
            self.MySql.mysqlDbCur.execute("SELECT users.id, users.name, users.zone FROM a7fh46_user_current currentH INNER JOIN a7fh46_users users ON currentH.uid = users.id  WHERE currentH.timeSeen > (NOW() - INTERVAL 1 MINUTE) ORDER BY id DESC LIMIT 1")

            results       =  self.MySql.mysqlDbCur.fetchone()

            if results != None: 
                return random.choice(responses).replace("%%HUMAN%%", results["name"])
            else:
                return "Sorry I could not identify you, this system will now self destruct! You have 5 seconds..."

        except Exception as errorz:
            print('FAILED1')
            print(errorz)
            return results
        
    def updateHuman(self, responses, entities):

        results       = None
        
        try:
            self.MySql.mysqlDbCur.execute("SELECT id, name FROM a7fh46_users users WHERE name = '%s'" % (entities[0]))
            results =  self.MySql.mysqlDbCur.fetchone()

            if results != None:
                timeSeen = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') 
                self.MySql.mysqlDbCur.execute("""
                    INSERT INTO a7fh46_user_current 
                        (uid, lid, fid, zid, did, timeSeen)
                    VALUES 
                        (%s, %s, %s, %s, %s, %s); """, (results["id"], self._confs["iotJumpWay"]["Location"], 0, self._confs["iotJumpWay"]["Zone"], self._confs["iotJumpWay"]["Device"], timeSeen[:-3])) 
                self.MySql.mysqlDbConn.commit()
                return random.choice(responses).replace("%%HUMAN%%", results["name"])

            else:
                return "Sorry I could not identify you, this system will now self destruct! You have 5 seconds..."

        except Exception as errorz:
            print('FAILED2')
            print(errorz)
            return results

