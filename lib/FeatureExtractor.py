#!/bin/python3

import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from keras.models import load_model
import pickle

class FeatureExtractor:
    def __init__(self):
        pass
    
    def __get_data__(self):
        pass
    
    def __clean_data__(self):
        pass

    def __load_model__(self, paths):
        models = []
        for i in paths:
            if 'h5' in i.split(".")[-1]:
                models.append(load_model(i))
            else:
                models.append(pickle.load(open(i, 'rb')))
        return models

    def __get_vectors__(self):
        pass

    def __analyse_mood__(self):
        pass
        
        