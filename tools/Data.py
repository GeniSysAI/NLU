############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Data Helper
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
# Title:         GeniSys NLU Data Helper
# Description:   Data helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
############################################################################################

import json, random, nltk, numpy as np 

from nltk.stem.lancaster import LancasterStemmer
from tools.Helpers       import Helpers
from tools.Logging       import Logging

class Data():

    def __init__(self):

        ###############################################################
        #
        # Sets up all default requirements and placeholders 
        # needed for the NLU engine to run. 
        #
        # - Helpers: Useful global functions
        # - Logging: Logging class
        # - LancasterStemmer: Word stemmer
        #
        ###############################################################
        
        self.ignore  = [',','.','!','?']
        
        self.Helpers = Helpers()
        self._confs  = self.Helpers.loadConfigs()
        self.LogFile = self.Helpers.setLogFile(self._confs["aiCore"]["Logs"]+"JumpWay/")
        
        self.LancasterStemmer = LancasterStemmer()
            
    def loadTrainingData(self):

        ###############################################################
        #
        # Loads the NLU and NER training data from data/training.json
        #
        ###############################################################

        with open("data/training.json") as jsonData:
            trainingData = json.load(jsonData)
            
        self.Helpers.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Training Data Ready")
            
        return trainingData

    def loadTrainedData(self):

        ###############################################################
        #
        # Loads the saved training configuratuon
        #
        ###############################################################
    
        with open("model/model.json") as jsonData:
            modelData = json.load(jsonData)
            
        self.Helpers.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Model Data Ready")
        
        return modelData
            
    def sortList(self, listToSort):

        ###############################################################
        #
        # Sorts a list by sorting the list, and removing duplicates 
        # 
        # https://www.programiz.com/python-programming/methods/built-in/sorted 
        # https://www.programiz.com/python-programming/list
        # https://www.programiz.com/python-programming/set
        #
        ###############################################################

        return sorted(list(set(listToSort)))
        
    def extract(self, data=None, splitIt=False):

        ###############################################################
        #
        # Extracts words from sentences, stripping out characters in 
        # the ignore list above
        # 
        # https://www.nltk.org/_modules/nltk/stem/lancaster.html
        # http://insightsbot.com/blog/R8fu5/bag-of-words-algorithm-in-python-introduction
        #
        ###############################################################
        
        return [self.LancasterStemmer.stem(word) for word in (data.split() if splitIt == True else data) if word not in self.ignore]

    def makeBagOfWords(self, sInput, words):

        ###############################################################
        #
        # Makes a bag of words used by the inference and training 
        # features. If makeBagOfWords is called during training, sInput 
        # will be a list.
        # 
        # http://insightsbot.com/blog/R8fu5/bag-of-words-algorithm-in-python-introduction
        #
        ###############################################################
        
        if type(sInput) == list:
            bagOfWords = []
            for word in words: 
                if word in sInput:
                    bagOfWords.append(1)
                else:
                    bagOfWords.append(0)
            return bagOfWords
        
        else:
            bagOfWords = np.zeros(len(words))
            for cword in self.extract(sInput, True):
                for i, word in enumerate(words):
                    if word == cword: bagOfWords[i] += 1
            return np.array(bagOfWords)

    def prepareClasses(self, intent, classes):

        ###############################################################
        #
        # Adds an intent key to classes if it does not already exist
        #
        ###############################################################

        if intent not in classes: classes.append(intent)
        return classes
        
    def prepareData(self, trainingData = [], wordsHldr = [], dataCorpusHldr = [], classesHldr = []):

        ###############################################################
        #
        # Prepares the NLU and NER training data, loops through the 
        # intents from our dataset, converts any entities / synoynms  
        #
        ###############################################################

        counter   = 0
        intentMap = {}

        for intent in trainingData['intents']:

            theIntent = intent['intent']
            for text in intent['text']:

                if 'entities' in intent and len(intent['entities']):
                    i = 0
                    for entity in intent['entities']:
                        tokens = text.replace(trainingData['intents'][counter]["text"][i], "<"+entity["entity"]+">").lower().split()
                        wordsHldr.extend(tokens)
                        dataCorpusHldr.append((tokens, theIntent))
                        i = i + 1
                else:
                    tokens = text.lower().split()
                    wordsHldr.extend(tokens)
                    dataCorpusHldr.append((tokens, theIntent))

            intentMap[theIntent] = counter
            classesHldr          = self.prepareClasses(theIntent, classesHldr)
            counter              = counter + 1

        return self.sortList(self.extract(wordsHldr, False)), self.sortList(classesHldr), dataCorpusHldr, intentMap
        
    def finaliseData(self, classes, dataCorpus, words):

        ###############################################################
        #
        # Finalises the NLU training data 
        #
        ###############################################################

        trainData = []
        out = np.zeros(len(classes))

        for document in dataCorpus:
            output = list(out)
            output[classes.index(document[1])] = 1
            trainData.append([self.makeBagOfWords(self.extract(document[0], False), words), output])

        random.shuffle(trainData)
        trainData = np.array(trainData)
            
        self.Helpers.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Finalised Training Data Ready")

        return list(trainData[:,0]), list(trainData[:,1])