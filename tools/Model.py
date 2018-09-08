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
# Title:         GeniSys NLU Data Helper
# Description:   Model helper functions for GeniSys NLU.
# Configuration: required/confs.json
# Last Modified: 2018-09-08
#
############################################################################################
 
import tflearn, json
import tensorflow as tf

from tools.Helpers import Helpers

class Model():
    
    def __init__(self):
        
        self.setup()
        
    def setup(self):
        
        self.Helpers = Helpers()
        self._confs  = self.Helpers.loadConfigs()
        
    def saveModelData(self, path, data):
        
        with open(path, "w") as outfile:
            json.dump(data, outfile)
            
    def createDNNLayers(self, x, y):
        
        net = tflearn.input_data(shape=[None, len(x[0])])

        for i in range(self._confs["ClassifierSettings"]['FcLayers']):
            net = tflearn.fully_connected(net, self._confs["ClassifierSettings"]['FcUnits'])

        net = tflearn.fully_connected(net, len(y[0]), activation=str(self._confs["ClassifierSettings"]['Activation']))
        net = tflearn.regression(net)

        return net
            
    def trainDNN(self, x, y, words, classes, intentMap):

        tf.reset_default_graph()

        tmodel = tflearn.DNN(
                        self.createDNNLayers(x, y), 
                        tensorboard_dir = self._confs["ClassifierSettings"]['TFLearn']['Logs'], 
                        tensorboard_verbose = self._confs["ClassifierSettings"]['TFLearn']['LogsLevel'])

        tmodel.fit(
                x, 
                y, 
                n_epoch = self._confs["ClassifierSettings"]['Epochs'], 
                batch_size = self._confs["ClassifierSettings"]['BatchSize'], 
                show_metric = self._confs["ClassifierSettings"]['ShowMetric'])

        tmodel.save(self._confs["ClassifierSettings"]['TFLearn']['Path'])
            
        self.saveModelData(
            self._confs["ClassifierSettings"]['TFLearn']['Data'],
            {
                'words': words, 
                'classes': classes, 
                'x': x, 
                'y': y,
                'iMap' : [intentMap]
            })

    def buildDNN(self, x, y):

        tf.reset_default_graph()
        tmodel = tflearn.DNN(self.createDNNLayers(x, y))
        tmodel.load(self._confs["ClassifierSettings"]['TFLearn']['Path'])
        return tmodel