import os
import pickle


def version_config(update=False):
    filename = os.path.join(os.path.dirname(__file__), 'version_config.yaml')
    config = yaml_load(filename)
    # config = load(filename)
    if update:
        config["version"] += 1
        yaml_dump(filename, config)
        # save(filename, config)
    __version__ = '0.' + '.'.join(list(str(config["version"])))
    __name__ = config["name"]
    return __version__, __name__


def save(filename, data):
    with open(filename, 'wb') as fw:
        pickle.dump(data, fw)


def load(filename):
    with open(filename, 'rb') as fi:
        data = pickle.load(fi)
    return data


def yaml_dump(filepath, data):
    from yaml import dump
    try:
        from yaml import CDumper as Dumper
    except ImportError:
        from yaml import Dumper
    with open(filepath, "w", encoding='utf-8') as fw:
        fw.write(dump(data, Dumper=Dumper))


def yaml_load(filepath):
    from yaml import load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    with open(filepath, 'r', encoding="utf-8") as stream:
        #     stream = stream.read()
        content = load(stream, Loader=Loader)
    return content
