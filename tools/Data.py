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
# Last Modified: 2018-09-08
#
############################################################################################

import json, random, pickle, nltk, numpy as np 

from nltk.stem.lancaster import LancasterStemmer

class Data():

    def __init__(self, Logging, LogFile):
        
        self.LancasterStemmer = LancasterStemmer()

        self.Logging          = Logging
        self.LogFile          = LogFile
        
        self.ignore  = [
            '?',
            '!'
        ]
        
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Data Helper Ready")
            
    def loadTrainingData(self):

        with open("data/training.json") as jsonData:
            trainingData = json.load(jsonData)
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Training Data Ready")
            
        return trainingData

    def loadTrainedData(self):
    
        with open("model/model.json") as jsonData:
            modelData = json.load(jsonData)
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Model Data Ready")
        
        return modelData

    def loadIntentMap(self):

        with open("data/intentMapper.json") as jsonData:
            intentsMap = json.load(jsonData)
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Intent Map Ready")
            
        return intentsMap

    def writeIntentMap(self, intentMapper, saveTo):
        
        with open(saveTo, 'w') as file:
            json.dump(
                intentMapper, 
                file)
                
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Intent Map Saved")
            
    def sortList(self, listToSort):

        return sorted(list(set(listToSort)))
        
    def extract(self, data=None, lowerIt=True, splitIt=False, ignoreWords=False):
        
        if ignoreWords:
            return [self.LancasterStemmer.stem(word if lowerIt == False else word.lower()) for word in (data.split() if splitIt == True else data) if word not in self.ignore]
        else:
            return [self.LancasterStemmer.stem(word if lowerIt == False else word.lower()) for word in (data.split() if splitIt == True else data)]

    def makeTrainingBag(self, bagWords, words, bagOfWords = []):
        
        for word in words: bagOfWords.append(1) if word in bagWords else bagOfWords.append(0)

        return bagOfWords

    def makeInferenceBag(self, sentence, trainedWords):
         
        bagOfWords = np.zeros(len(trainedWords))
        for cword in self.extract(sentence, True, True):
            for i, word in enumerate(trainedWords):
                if word == cword: bagOfWords[i] += 1

        return np.array(bagOfWords)

    def prepareClasses(self, intent, classes):
                    
        if intent not in classes: classes.append(intent)

        return classes
        
    def prepareData(self, trainingData = [], wordsHldr = [], dataCorpusHldr = [], classesHldr = []):

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

        self.writeIntentMap(
            intentMap, 
            "data/intentMapper.json")

        words   = self.sortList(self.extract(wordsHldr, True, False,  True))
        classes = self.sortList(classesHldr)

        self.writeIntentMap(
            intentMap, 
            "data/intentMapper.json")
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Corpus: "+str(dataCorpusHldr))
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Classes: "+str(classes))
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Words: "+str(words))
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Intent Map: "+str(intentMap))

        return words, classes, dataCorpusHldr
        
    def finaliseData(self, classes, dataCorpus, words):

        trainData = []
        out       = np.zeros(len(classes))

        for document in dataCorpus:
            output = list(out)
            output[classes.index(document[1])] = 1
            trainData.append([self.makeTrainingBag(self.extract(document[0], True, False, False), words), output])

        random.shuffle(trainData)
        trainData = np.array(trainData)
            
        self.Logging.logMessage(
            self.LogFile,
            "Data",
            "INFO",
            "Finalised Training Data Ready"

        return list(trainData[:,0]), list(trainData[:,1])