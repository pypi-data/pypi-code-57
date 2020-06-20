import json
import os


def read_config():
    file_name = os.path.expanduser("~/.pyapt/config.json")
    data = json.loads(file_name)
    return data

def apply_ppa():
    pass
