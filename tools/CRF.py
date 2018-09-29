## THIS FILE HAS NOT BEEN TOUCHED FOR A LONG TIME AND I CANNOT REMEMBER IF I EVEN COMPLETED ENOUGH TO HAVE FUNCTIONING CODE, SAVING FOR POSSIBLE USE IN THE FUTURE.

import sklearn_crfsuite
import spacy
import json
from spacy.gold import GoldParse
import os
import joblib
nlp = spacy.load('en')

class CrfComponent():
    
    def __init__(self):
        
        pass
    
    def trainEntities(self, model, trainingData):
        
        try:
        
            dataset = self.createDataset(trainingData['intents'],nlp)
            print(dataset)
            X_train = [self.sent2features(s) for s in dataset]
            y_train = [self.sent2labels(s) for s in dataset]
            crf = sklearn_crfsuite.CRF(
                algorithm='lbfgs', 
                c1=0.1, 
                c2=0.1, 
                max_iterations=100, 
                all_possible_transitions=True
            )
            crf.fit(X_train, y_train)
            
            joblib.dump(crf,"models/mitie_"+str(model)+".pkl")
            
            print("Saving Model "+str(model)+" Entities")
            
        except Exception as ex:
            
            print("Error Training Model "+str(model)+" Entities "+str(ex))

    def createDataset(self, intents, spacy_nlp):
        
        dataset = []
        entity_offsets = []
        
        intentCounter = 0
        for intent in intents:
            
            sentenceCounter = 0
            for sentence in intent['text']:
                
                doc = spacy_nlp(sentence)
                print(doc.text)

                for entity in intent['entities'][sentenceCounter]:
                    
                    entity_offsets.append(tuple((entity['rangeFrom'],entity['rangeTo'],entity['entity'])))
                
                gold = GoldParse(doc, entities=entity_offsets)
                ents = [l[5] for l in gold.orig_annot]
                crf_format = [(doc[entity].text, doc[entity].tag_, ents[entity]) for i in range(len(doc))]
                dataset.append(crf_format)
                sentenceCounter = sentenceCounter + 1
            
            intentCounter = intentCounter + 1

        return dataset
        
    def jsonToCrf(self, json_eg, spacy_nlp):
        
        entity_offsets = []

        for sentence in json_eg['text']:

            doc = spacy_nlp(sentence)

            for i in json_eg['entities']:
                
                entity_offsets.append(tuple((i['rangeFrom'],i['rangeTo'],i['entity'])))
                
            gold = GoldParse(doc, entities=entity_offsets)
            ents = [l[5] for l in gold.orig_annot]
            crf_format = [(doc[i].text, doc[i].tag_, ents[i]) for i in range(len(doc))]
        
        return crf_format
    
    def sent2features(self, sent):
        
        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):
        
        return [label for token, postag, label in sent]
    
    def word2features(self, sent, i):
        
        word = sent[i][0]
        postag = sent[i][1]
        features = {
            'bias': 1.0,
            'word.lower()': word.lower(),
            'word[-3:]': word[-3:],
            'word[-2:]': word[-2:],
            'word.isupper()': word.isupper(),
            'word.istitle()': word.istitle(),
            'word.isdigit()': word.isdigit(),
            'postag': postag,
            'postag[:2]': postag[:2],        
        }
        if i > 0:
            word1 = sent[i-1][0]
            postag1 = sent[i-1][1]
            features.update({
                '-1:word.lower()': word1.lower(),
                '-1:word.istitle()': word1.istitle(),
                '-1:word.isupper()': word1.isupper(),
                '-1:postag': postag1,
                '-1:postag[:2]': postag1[:2],
            })
        else:
            features['BOS'] = True
            
        if i < len(sent)-1:
            word1 = sent[i+1][0]
            postag1 = sent[i+1][1]
            features.update({
                '+1:word.lower()': word1.lower(),
                '+1:word.istitle()': word1.istitle(),
                '+1:word.isupper()': word1.isupper(),
                '+1:postag': postag1,
                '+1:postag[:2]': postag1[:2],
            })
        else:
            features['EOS'] = True
                    
        return features