import yaml
from printy import printy, inputy
from os import path
from os.path import expanduser


def init(conf_path):
    settings = [ {"workspace_warp_database": "~/.wws_data.yaml" }, {"exclude_patterns": ["Icon?",".DS_Store"]} ]
    with open(conf_path,'w+') as f:
        f.seek(0)
        f.truncate()
        yaml.dump(settings, f, default_flow_style=False)
    
    

def load_settings(conf_path):
    conf_path = expanduser(conf_path)

    if not path.exists(conf_path):
        print("Abort, configuration settings file not found.")
        exit()

    with open(conf_path,'r') as f:
        settings = yaml.load(f, Loader=yaml.FullLoader)
    return settings



def _safe_print(msg, **kwargs):
    try:
        print(msg, **kwargs)
    except UnicodeEncodeError:
        print(msg.encode('ascii','ignore'), **kwargs)


def _info(msg, **kwargs):
    _safe_print(CCYAN + "¡" + CRESET + " " + msg, **kwargs)


def _local_with_brew_check(pkg):
    brew = local.get('brew','/usr/local/bin/brew')

    brew_has_pkg = brew['ls', '--versions', pkg].run(retcode=None)
    if brew_has_pkg[0] == 1:
        _info("Installing '" + pkg +"' terminal tool")
        if brew['install', pkg].run(retcode=None)[0] == 1:
            # return None if we fail to install
            return None

    return local.get(pkg, '/usr/local/bin/'+pkg)


import os
import sys

def get_script_path():
    return os.path.realpath(sys.argv[0])


# Prompt the yes/no-*question* to the user
# ref: https://stackoverflow.com/a/3041990/1700053
def _confirm(question, default='no'):
  from distutils.util import strtobool

  while True:
    try:
      return strtobool(inputy(question + " (y/n): ").lower())
    except ValueError:
      print("\tPlease use y/n or yes/no.\n")
