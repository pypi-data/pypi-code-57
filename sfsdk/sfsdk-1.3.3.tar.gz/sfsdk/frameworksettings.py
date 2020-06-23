# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sfsdk import log, utils
from ruamel import yaml
import os
import glob
import re
import shutil
import json
import copy

workspace_dir = None

def load(base_dir):
    
    global workspace_dir

    workspace_dir = base_dir

def save_framework(framework):

    framework_path = os.path.join(workspace_dir, 'frameworks.yml')

    try:
        with open(framework_path, "r") as f:
            frameworks_list = yaml.safe_load(f)
    except OSError:
        frameworks_list = []
    except yaml.YAMLError:
        raise log.FatalMsg("Settings file %s has broken YAML, delete it to recreate" % framework_path)

    if not frameworks_list or not isinstance(frameworks_list, list):
        frameworks_list = []

    # Add if it does not exist
    if not framework in [ n['name'] for n in frameworks_list ]:

        ids = [ n['id'] for n in frameworks_list ]

        # Pick the first available id from 0 to 1000
        random_id = next(iter(set(range(0, 1000)) - set(ids)))

        frameworks_list.append({
            'id': random_id,
            'name': framework,
            'local': True
        })

    with open(framework_path, "w+") as f:
        yaml.dump(frameworks_list, f, default_flow_style=False)

    return framework_path

def get_frameworks():

    framework_path = os.path.join(workspace_dir, 'frameworks.yml')

    try:
        with open(framework_path, "r") as f:
            yaml_data = yaml.safe_load(f)
    except IOError:
        yaml_data = []

    if yaml_data and isinstance(yaml_data, list):
        return yaml_data

    return []

def delete_framework_by_name(framework):
    
    framework_path = os.path.join(workspace_dir, 'frameworks.yml')

    new_framework_list = []

    with open(framework_path, "r") as f:
        frameworks_list = yaml.safe_load(f)

        if not frameworks_list or not isinstance(frameworks_list, list):
            return []

        for f in frameworks_list:
            if f['name'] != framework:
                new_framework_list.append(f)

    with open(framework_path, "w+") as f:
        yaml.dump(new_framework_list, f, default_flow_style=False)

    return new_framework_list