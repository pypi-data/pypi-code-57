"""
utility script for optimization techniques
"""

from hyperopt import hp, fmin, tpe, Trials

# local
from foresee.scripts import fitter


def tune(train_fact, test_fact, model, params=None, args=None):
    """[summary]

    Parameters
    ----------
    train_fact : [type]
        [description]
    test_fact : [type]
        [description]
    model : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """    

    ts_train = train_fact['y']
    ts_test = test_fact['y']
    
    tune_class_obj = fitter.tuner(model)
    best, err = tune_class_obj.tune(ts_train, ts_test, params, args)
    
    return best, err