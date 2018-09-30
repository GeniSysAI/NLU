############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Mitie Helpers
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
# Title:         GeniSys NLU Mitie Helpers
# Description:   Helper functions for GeniSys NLU using Mitie.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
# Uses code from https://github.com/mit-nlp/MITIE
#
############################################################################################
 
import sys, os, nltk

parent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(parent + '/../MITIE/mitielib')

from nltk.stem.lancaster import LancasterStemmer
from tools.Helpers       import Helpers
from mitie               import *

class Entities():
    
    def __init__(self):

        ###############################################################
        #
        # Sets up all default requirements
        #
        # - Helpers: Useful global functions
        # - LancasterStemmer: Word stemmer
        #
        ###############################################################
        
        self.Helpers = Helpers()
        self._confs  = self.Helpers.loadConfigs()

        self.stemmer = LancasterStemmer()
        
    def restoreNER(self):

        ###############################################################
        #
        # Restores the NER model, in this case MITIE
        #
        ###############################################################
         
        if os.path.exists(self._confs["NLU"]["EntitiesDat"]):
            return named_entity_extractor(self._confs["NLU"]["EntitiesDat"])

    def parseEntities(self, sentence, ner, trainingData):

        ###############################################################
        #
        # Parses entities in intents/sentences
        #
        ###############################################################

        entityHolder   = []
        fallback       = False
        parsedSentence = sentence
        parsed         = ""

        if os.path.exists(self._confs["NLU"]["EntitiesDat"]):

            tokens   = sentence.lower().split()
            entities = ner.extract_entities(tokens)

            for e in entities:

                range     = e[0]
                tag       = e[1]
                score     = e[2]
                scoreText = "{:0.3f}".format(score)
                
                if score > self._confs["NLU"]["Mitie"]["Threshold"]:
                    
                    parsed, fallback = self.replaceEntity(
                        " ".join(tokens[i] for i in range),
                        tag,
                        trainingData)

                    entityHolder.append({
                        "Entity":tag,
                        "ParsedEntity":parsed,
                        "Confidence":str(scoreText)})

                    parsedSentence = sentence.replace(
                        " ".join(sentence.split()[i] for i in range), 
                        "<"+tag+">")

                else:
                    
                    parsed, fallback = self.replaceEntity(
                        " ".join(tokens[i] for i in range),
                        tag,
                        trainingData)

                    entityHolder.append({
                        "Entity":tag,
                        "ParsedEntity":parsed,
                        "Confidence":str(scoreText)})

                    parsed = parsedSentence
                    
        return parsed, fallback, entityHolder, parsedSentence
        
    def replaceResponseEntities(self, response, entityHolder):

        ###############################################################
        #
        # Replaces entities in responses
        #
        ###############################################################

        entities = []

        for entity in entityHolder: 
            response = response.replace("<"+entity["Entity"]+">", entity["ParsedEntity"].title())
            entities.append( entity["ParsedEntity"].title())

        return response, entities

    def replaceEntity(self, value, entity, trainingData):

        ###############################################################
        #
        # Replaces entities/synonyms
        #
        ###############################################################

        lowEntity = value.lower()
        match     = True

        if "entitieSynonyms" in trainingData:
            for entities in trainingData["entitieSynonyms"]:
                for synonyms in entities[entity]:
                    for synonym in synonyms["synonyms"]:
                        if lowEntity == synonym.lower():
                            lowEntity = synonyms["value"]
                            match = False
                            break

        return lowEntity, match 

    def trainEntities(self, mitiemLocation, trainingData):

        ###############################################################
        #
        # Trains the NER model
        #
        ###############################################################
        
        trainer     = ner_trainer(mitiemLocation)
        counter     = 0
        hasEnts = 0

        for intents in trainingData['intents']:

            i = 0
            for entity in intents['entities']:

                hasEnts = 1
                tokens  = trainingData['intents'][counter]["text"][i].lower().split()
                data    = ner_training_instance(tokens)
                data.add_entity(
                    xrange(
                        entity["rangeFrom"],
                        entity["rangeTo"]), 
                    entity["entity"])
                trainer.add(data)
                
                i = i + 1
            counter = counter + 1

        if hasEnts:
            trainer.num_threads = 4
            ner = trainer.train()
            ner.save_to_disk(self._confs["NLU"]["EntitiesDat"])