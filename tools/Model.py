############################################################################################
#
# The MIT License (MIT)
# 
# GeniSys NLU Model Helper
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
# Title:         GeniSys NLU Model Helper
# Description:   Model helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-29
#
############################################################################################

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tflearn, json
import tensorflow as tf

from tools.Data    import Data
from tools.Helpers import Helpers

class Model():
    
    def __init__(self):

        ###############################################################
        #
        # Sets up all default requirements
        #
        # - Helpers: Useful global functions
        # - Data: Data functions
        #
        ###############################################################
        
        self.Helpers = Helpers()
        self._confs  = self.Helpers.loadConfigs()

        self.Data = Data()
            
    def createDNNLayers(self, x, y):

        ###############################################################
        #
        # Sets up the DNN layers, configuration in required/confs.json
        #
        ###############################################################
        
        net = tflearn.input_data(shape=[None, len(x[0])])

        for i in range(self._confs["NLU"]['FcLayers']):
            net = tflearn.fully_connected(net, self._confs["NLU"]['FcUnits'])

        net = tflearn.fully_connected(net, len(y[0]), activation=str(self._confs["NLU"]['Activation']))

        if self._confs["NLU"]['Regression']:
            net = tflearn.regression(net)

        return net
            
    def trainDNN(self, x, y, words, classes, intentMap):

        ###############################################################
        #
        # Trains the DNN, configuration in required/confs.json
        #
        ###############################################################

        tf.reset_default_graph()

        tmodel = tflearn.DNN(
                        self.createDNNLayers(x, y), 
                        tensorboard_dir = self._confs["NLU"]['TFLearn']['Logs'], 
                        tensorboard_verbose = self._confs["NLU"]['TFLearn']['LogsLevel'])

        tmodel.fit(
                x, 
                y, 
                n_epoch = self._confs["NLU"]['Epochs'], 
                batch_size = self._confs["NLU"]['BatchSize'], 
                show_metric = self._confs["NLU"]['ShowMetric'])
            
        self.saveModelData(
            self._confs["NLU"]['TFLearn']['Data'],
            {
                'words': words, 
                'classes': classes, 
                'x': x, 
                'y': y,
                'intentMap' : [intentMap]
            },
            tmodel)
        
    def saveModelData(self, path, data, tmodel):

        ###############################################################
        #
        # Saves the model data for TFLearn and the NLU engine, 
        # configuration in required/confs.json
        #
        ###############################################################

        tmodel.save(self._confs["NLU"]['TFLearn']['Path'])
        
        with open(path, "w") as outfile:
            json.dump(data, outfile)

    def buildDNN(self, x, y):

        ###############################################################
        #
        # Loads the DNN model, configuration in required/confs.json
        #
        ###############################################################

        tf.reset_default_graph()
        tmodel = tflearn.DNN(self.createDNNLayers(x, y))
        tmodel.load(self._confs["NLU"]['TFLearn']['Path'])
        return tmodel
        
    def predict(self, tmodel, parsedSentence, trainedWords, trainedClasses):
        
        ###############################################################
        #
        # Makes a prediction against the trained model, checking the 
        # confidence and then logging the results.
        #
        ###############################################################
         
        predictions = [[index, confidence] for index, confidence in enumerate(
			tmodel.predict([
				self.Data.makeBagOfWords(
					parsedSentence,
					trainedWords)])[0])]

        predictions.sort(key=lambda x: x[1], reverse=True)
        
        classification = []
        for prediction in predictions:  classification.append((trainedClasses[prediction[0]], prediction[1]))
            
        return classification