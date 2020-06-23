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

from sfsdk import log
import os
import os.path
import yaml
import shutil

settings = {}

default_technologies_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "technologies.yml"
)

technologies = {}
technologies_path = None

def prepare_technologies(remote_tech_list):
    """ Merge current technologies with remote tech list """

    global technologies

    with open(default_technologies_path, 'r') as yaml_file:
        technologies = yaml.safe_load(yaml_file)

    for remote_tech in remote_tech_list:

        # Skip if empty or missing
        image_url = remote_tech.get('imageUrl')

        if not image_url or not '/' in image_url:
            log.debug("Skipping %s with no imageUrl" % (remote_tech['technology']))
            continue
        
        tag = remote_tech['imageUrl'].split('/')[-1]

        if not tag in technologies.keys():
            technologies[tag] = {}

        technologies[tag].update({
            'technology': remote_tech['technology'],
            'imageUrl': remote_tech['imageUrl']
        })

def load(base_dir):

    """ Load or create technologies settings file"""

    global technologies, technologies_path

    technologies_path = os.path.join(
        base_dir, 
        'technologies.yml'
    )

    try:
        with open(technologies_path, 'r') as yaml_file:
            technologies = yaml.safe_load(yaml_file)
    except OSError as e:
        os.makedirs(base_dir, exist_ok=True)
        shutil.copy(default_technologies_path, technologies_path)

        try:
            with open(technologies_path, 'r') as yaml_file:
                technologies = yaml.safe_load(yaml_file)
        except Exception as e:
            raise log.FatalMsg("Error loading default technology file")
    except yaml.YAMLError as e:
        raise log.FatalMsg("Settings file %s has broken YAML, delete it to recreate" % settings_path)

def save():
    """ Save settings file"""

    try:
        with open(technologies_path, 'w+') as outfile:
            yaml.dump(technologies, outfile, default_flow_style=False)
    except Exception as e:
        log.debug(str(e))
        raise log.FatalMsg("Error saving current settings" % technologies_path)

