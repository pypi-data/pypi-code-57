import numpy as np

def to_array(df, cols):
    data = []
    for col in cols:
        data.append(np.stack(df[col].values))
    
    return data

def model_file(path, name, fold):
    if fold is not None:
        return "{}/{}_fold_{}".format(path, name, fold)
    return "{}/{}_whole".format(path, name)

def model_weights_file(path, name, fold):
    if fold is not None:
        return "{}/{}_fold_{}/{}".format(path, name, fold, name)
    return "{}/{}_whole/{}".format(path, name, name)

def model_files_for(path, name, folds, include_final):
    names = []

    for i in range(folds):
        names.append(model_file(path, name, i))
    
    if include_final:
        names.append(model_file(path, name, fold=None))
    
    return names