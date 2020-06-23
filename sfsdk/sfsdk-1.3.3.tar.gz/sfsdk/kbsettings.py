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

from sfsdk import exrsettings, log, utils
from ruamel import yaml
import os
import glob
import re
import shutil
import json
import copy
import uuid
import tempfile

workspace_dir = None

def load(base_dir):

    global workspace_dir

    workspace_dir = os.path.join(
            base_dir,
            'kb'
    )

    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)

def get_standard_kb_name(kb):

    tech = re.sub(
            "[^a-z0-9]",
            "_",
            kb['technology'].lower()
            )

    title = re.sub(
            "[^a-z0-9]",
            "_",
            kb['vulnerability'].lower()
            )

    long_uuid = kb['uuid']

    if long_uuid[:6] in ('local-', 'sfsdk-'):
         shorter_uuid = long_uuid[:10]
    else:
         shorter_uuid = long_uuid[:4]

    return '%s_%s-%s' % (tech, title, shorter_uuid)

def save_kb_meta(kb_yaml_orig):

    kb_yaml = copy.deepcopy(kb_yaml_orig)

    kb = get_standard_kb_name(kb_yaml)

    kb_dir = os.path.join(workspace_dir, kb)

    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir)


    information_text = kb_yaml['md']['text']
    information_text = utils.save_and_replace_b64_with_media(
        base_folder = kb_dir,
        content = information_text,
        content_name = 'kb'
    )
    with open(os.path.join(kb_dir, 'kb.md'), 'w+') as f:
        f.write(information_text)
    kb_yaml['md']['text'] = '!import kb.md'

    if log.verbose:
        kb_meta_debug_path = os.path.join(kb_dir, '.last-saved.json')
        log.debug('Saving JSON debug to %s' % (kb_meta_debug_path))
        with open(kb_meta_debug_path, 'w') as f:
              json.dump(kb_yaml_orig, f, indent=4)

    with open(os.path.join(kb_dir, "kb.yml"), "w") as f:
        yaml.dump(kb_yaml, f, default_flow_style=False)

    return kb_dir

def load_kb_meta(kb):

    kb_dir = os.path.join(workspace_dir, kb)

    if not os.path.exists(kb_dir):
        os.makedirs(kb_dir)

    kb_meta_path = os.path.join(kb_dir, 'kb.yml')

    kb_yaml = {}

    try:

        with open(kb_meta_path, 'r') as stream:
            try:
                kb_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise log.FatalMsg(exc)

            with open(os.path.join(kb_dir, 'kb.md'), 'r') as stream:
                kb_yaml['md']['text'] = utils.load_and_replace_media_with_b64(
                        kb_dir,
                        stream.read()
                    )

            

    except IOError:
        pass

    return kb_yaml

def get_kbs():

    kbs = {}

    for kb_yml_path in glob.glob('%s/*/kb.yml' % workspace_dir):

        current_name = kb_yml_path.split('/')[-2]
        
        kbs[current_name] = load_kb_meta(current_name)

    return kbs

def get_kb_by_uuid(kb_uuid):
    
    for kb_yml_path in glob.glob('%s/*/kb.yml' % workspace_dir):

        current_name = kb_yml_path.split('/')[-2]

        kb_data = load_kb_meta(current_name)

        if kb_data['uuid'] == kb_uuid:
            return kb_data

def delete_kb_by_uuid(kb_uuid):
        
    for kb_yml_path in glob.glob('%s/*/kb.yml' % workspace_dir):

        current_name = kb_yml_path.split('/')[-2]
        current_folder = os.path.dirname(kb_yml_path)

        kb_data = load_kb_meta(current_name)

        if kb_data['uuid'] == kb_uuid:
    
            tempfolder = tempfile.mkdtemp()

            print("Moving %s to %s" % (current_folder, tempfolder))

            os.rename(current_folder, tempfolder)

            return kb_uuid

def update_kb_folder(old_kb_dir, new_kb_data):

    new_kb_dir = save_kb_meta(new_kb_data)

    if old_kb_dir != new_kb_dir:
        log.warn("Moved from %s to %s" % (old_kb_dir, new_kb_dir))
        shutil.rmtree(old_kb_dir)