import os
import pickle
import yaml

from pathlib import Path

def get_run_dir():
    nni_run_dir = os.path.join(str(Path.home()), 'nni', 'runs')
    return nni_run_dir

def to_pickle(obj):
    if obj is not None:
        return pickle.dumps(obj)

def from_pickle(pkl):
    if pkl is not None:
        return pickle.loads(pkl)

def class_detail(instance):
    module = instance.__class__.__module__
    clazz = instance.__class__.__name__
    if module is None or module == str.__class__.__module__:
        return clazz
    return module, clazz, module+'.'+clazz

def parse_nni_exec_yaml(file_path):
    yml = yaml.safe_load(open(file_path, 'r'))
    result = {}
    for item in yml['nniExecution']:
        result[item['property']] = item['value']
    return result

def parse_model_space_yaml(file_path):
    yml = yaml.safe_load(open(file_path, 'r'))
    result = {}
    for model in yml['models']:
        name = model['name']
        sp = []
        for item in model['searchSpace']:
            d = {}
            for key in item:
                d[key] = item[key]
            sp.append(d)

        result[name] = sp
    return result


if __name__ == "__main__":
    test = parse_model_space_yaml('../tuner/config/default_models.yml')
    print(test)