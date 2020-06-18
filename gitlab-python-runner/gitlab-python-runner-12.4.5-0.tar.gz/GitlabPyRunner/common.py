"""
Various functions shared between the other modules
"""
import socket
import platform
import yaml
from yaml.constructor import ConstructorError


def gethostname():
    try:
        return socket.gethostname()
    except:
        return "unknown-hostname"


def iswindows():
    return platform.system() == "Windows"


def parse_config(configfile):
    with open(configfile, "r") as infile:
        try:
            config = yaml.load(infile, Loader=yaml.SafeLoader)
        except ConstructorError:
            # this file probably has unicode still in it, use the full loader
            config = yaml.load(infile, Loader=yaml.FullLoader)

    assert config

    assert "server" in config
    assert "dir" in config
    assert "executor" in config
    assert "token" in config
    assert "shell" in config

    return config


def save_config(configfile, data):
    with open("gitlab-runner.yml", "w") as outfile:
        yaml.safe_dump(data, outfile, indent=2)

