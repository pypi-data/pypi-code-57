#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project : ML Studio                                                         #
# Version : 0.1.0                                                             #
# File    : validation.py                                                     #
# Python  : 3.8.2                                                             #
# --------------------------------------------------------------------------  #
# Author  : John James                                                        #
# Company : DecisionScients                                                   #
# Email   : jjames@decisionscients.com                                        #
# URL     : https://github.com/decisionscients/MLStudio                       #
# --------------------------------------------------------------------------  #
# Created       : Thursday, May 14th 2020, 1:33:31 pm                         #
# Last Modified : Thursday, May 14th 2020, 1:35:41 pm                         #
# Modified By   : John James (jjames@decisionscients.com)                     #
# --------------------------------------------------------------------------  #
# License : BSD                                                               #
# Copyright (c) 2020 DecisionScients                                          #
# =========================================================================== #
"""Functions used to validate the state, parameters or data of an estimator."""
import sys

import numpy as np
import sklearn.utils.validation as skl

# --------------------------------------------------------------------------  #
def check_X(X):
    """Wraps sklearn's check array function."""
    return skl.check_array(array=X, accept_sparse=['csr'], 
                           accept_large_sparse=True)

def check_X_y(X, y):
    return skl.check_X_y(X, y, accept_sparse=['csr'],  
                        accept_large_sparse=True)    

def check_is_fitted(estimator):
    skl.check_is_fitted(estimator)

def is_one_hot(x):
    """Returns true if a 2 dimensional matrix is in one-hot encoded format."""
    if np.ndim(x) == 1:
        return False
    try:
        return np.sum(x) / x.shape[0]  == 1
    except:
        return False

def is_multilabel(y):
    """Returns true if y is multilabel"""
    y = np.asarray(y)
    if np.ndim(y) == 1:
        return False
    if is_one_hot(y):
        return False
    if y.shape[1] > 1:
        return True
# --------------------------------------------------------------------------  #
def validate_bool(param, param_name=""):        
    if not isinstance(param, bool):
        msg = "{s} must be a boolean value.".format(s=param_name)
        raise TypeError(msg)
    else:
        return True             
# --------------------------------------------------------------------------  #
def validate_int(param, param_name="", minimum=0, maximum=np.inf, left="closed",
                 right='closed'):        
    if not isinstance(param, int):
        msg = "{s} must be an integer.".format(s=param_name)
        raise TypeError(msg)
    else:
        return True           
# --------------------------------------------------------------------------  #
def validate_learning_rate_schedule(schedule):  
    from mlstudio.supervised.callbacks.learning_rate import LearningRateSchedule  
    valid_learning_rate_schedules = [cls.__name__ for cls in LearningRateSchedule.__subclasses__()]
    if not isinstance(schedule, LearningRateSchedule):
        msg = "{s} is an invalid LearningRateSchedule object. \
            The valid LearningRateSchedule classes include : \
            {v}".format(s=schedule, v=str(valid_learning_rate_schedules))
        raise TypeError(msg)
    else:
        return True         
# --------------------------------------------------------------------------  #
def validate_early_stop(stop):    
    from mlstudio.supervised.callbacks.early_stop import EarlyStop
    valid_early_stops = [cls.__name__ for cls in EarlyStop.__subclasses__()]
    if not isinstance(stop, EarlyStop):
        msg = "{s} is an invalid EarlyStop object. The valid EarlyStop classes include : \
            {v}".format(s=stop, v=str(valid_early_stops))
        raise TypeError(msg)
    else:
        return True        
# --------------------------------------------------------------------------  #
def validate_scorer(scorer):    
    from mlstudio.supervised.core.scorers import Scorer
    valid_scorers = [cls.__name__ for cls in Scorer.__subclasses__()]
    if not isinstance(scorer, Scorer):
        msg = "{s} is an invalid Scorer object. The valid Scorer classes include : \
            {v}".format(s=scorer, v=str(valid_scorers))
        raise TypeError(msg)
    else:
        return True
# --------------------------------------------------------------------------  #
def validate_activation(activation):    
    from mlstudio.supervised.core.activations import Activation
    valid_activations = [cls.__name__ for cls in Activation.__subclasses__()]
    if not isinstance(activation, Activation):
        msg = "{s} is an invalid Activation object. The valid Activation classes include : \
            {v}".format(s=activation, v=str(valid_activations))
        raise TypeError(msg)
    else:
        return True

# --------------------------------------------------------------------------  #
def validate_objective(objective):    
    from mlstudio.supervised.core.objectives import Objective
    valid_objectives = [cls.__name__ for cls in Objective.__subclasses__()]
    if not isinstance(objective, Objective):
        msg = "{s} is an invalid Objective function object. The valid Objective \
        function classes include : {v}".format(s=objective, v=str(valid_objectives))
        raise TypeError(msg)
    else:
        return True      
# --------------------------------------------------------------------------  #
def validate_gradient_scaler(scaler):        
    from mlstudio.utils.data_manager import GradientScaler
    if not isinstance(scaler, GradientScaler):
        msg = "{s} is an invalid GradientScaler object. The valid Optimizer \
        classes include : {v}".format(s=scaler, v=str(data_manager.GradientScaler.__name__))
        raise TypeError(msg)
    else:
        return True     
# --------------------------------------------------------------------------  #
def validate_optimizer(optimizer):    
    from mlstudio.supervised.core.optimizers import Optimizer
    valid_optimizers = [cls.__name__ for cls in Optimizer.__subclasses__()]
    if not isinstance(optimizer, Optimizer):
        msg = "{s} is an invalid Optimizer object. The valid Optimizer \
        classes include : {v}".format(s=optimizer, v=str(valid_optimizers))
        raise TypeError(msg)
    else:
        return True         
# --------------------------------------------------------------------------  #
def validate_regularizer(regularizer):    
    from mlstudio.supervised.core.regularizers import Regularizer
    valid_regularizers = [cls.__name__ for cls in Regularizer.__subclasses__()]
    if not isinstance(regularizer, Regularizer):
        msg = "{s} is an invalid Regularizer object. The valid Regularizer \
        classes include : {v}".format(s=regularizer, v=str(valid_regularizers))
        raise TypeError(msg)
    else:
        return True   
# --------------------------------------------------------------------------  #
def validate_task(task):    
    from mlstudio.supervised.core.tasks import Task
    valid_tasks = [cls.__name__ for cls in Task.__subclasses__()]
    if not isinstance(task, Task):
        msg = "{s} is an invalid Task object. The valid Task \
        classes include : {v}".format(s=task, v=str(valid_tasks))
        raise TypeError(msg)
    else:
        return True           
# --------------------------------------------------------------------------  #
def validate_metric(metric):
    valid_metrics = ['train_cost', 'train_score', 'val_cost', 'val_score',
                     'gradient_norm']
    if not isinstance(metric, str):
        msg = "The metric parameter must be a string including one of {v}.".\
            format(v=str(valid_metrics))
        raise TypeError(msg)
    elif metric not in valid_metrics:
        msg = "{m} is an invalid metric. The valid metrics include : {v}".\
            format(m=metric,
                   v=str(valid_metrics))
        raise ValueError(msg)
    else:
        return True

# --------------------------------------------------------------------------  #
def validate_string(param, param_name="", valid_values=None):
    if not isinstance(param, str) and not valid_values:
        msg = param_name + " must be a string."
        raise TypeError(msg)
    elif param not in valid_values:
        msg = param_name + " must be in {v}".format(v=str(valid_values))
        raise ValueError(msg)
    else:
        return True        

# --------------------------------------------------------------------------  #
def validate_range(param, minimum, maximum, param_name = "", left='open', right='open'):        
    if not isinstance(param, (int,float)):
        msg = param_name + " hyperparameter must be numeric."
        raise TypeError(msg)
    elif left == 'open' and right == 'open':
        if param <= minimum or param >= maximum:
            msg = param_name + " hyperparameter must be in (" + str(minimum) + "," + str(maximum) + ")"      
            raise ValueError(msg)
    elif left == 'open' and right != 'open':
        if param <= minimum or param > maximum:
            msg = param_name + " hyperparameter must be in (" + str(minimum) + "," + str(maximum) + "]"      
            raise ValueError(msg)
    elif left != 'open' and right == 'open':
        if param < minimum or param >= maximum:
            msg = param_name + " hyperparameter must be in [" + str(minimum) + "," + str(maximum) + ")"                  
            raise ValueError(msg)
    else:
        if param < minimum or param > maximum:
            msg = param_name + " hyperparameter must be in [" + str(minimum) + "," + str(maximum) + "]"                  
            raise ValueError(msg)
        
# --------------------------------------------------------------------------  #
def validate_zero_to_one(param, param_name = "", left='closed', right='closed'):
    """Validates a parameter whose values should be 0 and 1."""
    if not isinstance(param, (int,float)):
        msg = param_name + " hyperparameter must be numeric."
        raise TypeError(msg)
    elif left == 'open' and right == 'open':
        if param <= 0 or param >= 1:
            msg = param_name + " hyperparameter must be in (0,1)."      
            raise ValueError(msg)
    elif left == 'open' and right != 'open':
        if param <= 0 or param > 1:
            msg = param_name + " hyperparameter must be in (0,1]."      
            raise ValueError(msg)
    elif left != 'open' and right == 'open':
        if param < 0 or param >= 1:
            msg = param_name + " hyperparameter must be in [0,1)"      
            raise ValueError(msg)
    else:
        if param < 0 or param > 1:
            msg = param_name + " hyperparameter must be in [0,1]."      
            raise ValueError(msg)
# --------------------------------------------------------------------------  #
def search_all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in search_all_subclasses(c)])  
     