## THIS FILE HAS NOT BEEN TOUCHED FOR A LONG TIME, SAVING FOR  USE IN THE FUTURE.

import time

class Repetition():

    def checkReptInitiate(self,intent,session,settings):

        if not intent in session["history"] and not intent in settings["repetition"][0]["repetitionSkip"]:

            return True

        elif intent in session["history"] and not intent in settings["repetition"][0]["repetitionSkip"]:

            return False

    def checkReptIgnored(self,intent,settings):

        if not intent in settings["repetition"][0]["repetitionSkip"]:

            return True

        else:

            return False

    def checkReptContinue(self,intent,session,settings):

        if intent in session["history"] and session["history"][intent]["count"] > 0 and session["history"][intent]["count"] < settings["repetition"][0]["ignoreCount"]:

            return True

        else:

            return False

    def checkReptContinues(self,intent,session,settings):

        if intent in session["history"] and session["history"][intent]["count"] > settings["repetition"][0]["ignoreCount"]:

            return True

        else:

            return False

    def checkReptStop(self,intent,session,settings):

        if intent in session["history"] and session["history"][intent]["count"] == settings["repetition"][0]["ignoreCount"]:

            return True

        else:

            return False

    def setIgnoreResponses(self,settings):

        return [settings["repetition"][0]["ignoreMessage"]]

    def checkIgnoreStop(self,intent,session,settings):

        if "countTime" in session["history"][intent] and int(time.time()) > session["history"][intent]["countTime"] + settings["repetition"][0]["ignoreReset"]:

            return True

        else:

            return False