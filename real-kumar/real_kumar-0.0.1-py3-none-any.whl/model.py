# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 11:23:15 2020

@author: Kumar Awanish
"""

import pandas 
from sklearn.ensemble import RandomForestRegressor
import pickle
    
    
 
def training_features(training_features):
    """
    Function to read training features csv file.
    """
    data=pandas.read_csv(training_features)
    return data


def training_targets(training_targets):
    """
    Function to read training targets csv file.
    """
    data=pandas.read_csv(training_targets)
    return data


def prediction_features(prediction_features):
    """
    Function to read prediction features csv file.
    """
    data=pandas.read_csv(prediction_features)
    return data

def model_training(training_features, training_targets):
    """
    Function to train model on training features and targets.
    """
    features=training_features(training_features)
    features.drop(labels=['datetime'],inplace=True, axis=1)
    lables=training_targets(training_targets)
    lables.drop(labels=['datetime'],inplace=True, axis=1)
    clf = RandomForestRegressor(max_depth=2, random_state=0)
    clf.fit(features, lables)
    # Save to file in the current working directory
    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(clf, file)
    return clf


def model_prediction (prediction_features,pkl_filename):
    """
    Function to predict the predction features outcomes.
    """
    perdiction_features =prediction_features(prediction_features)
    perdiction_features.drop(labels=['datetime'],inplace=True, axis=1)
    
    # Load from file
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    #predict the model
    predict = pickle_model.predict(perdiction_features)
    return predict
    
    


