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

import re
import os
import glob
import zipfile
import json
import shutil
import base64
import copy
import uuid
from sfsdk import log, utils
from ruamel import yaml
from pathlib import Path

workspace_dir = None

def load(base_dir):

    global workspace_dir

    workspace_dir = os.path.join(
            base_dir,
            'exr'
    )

    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)

def get_standard_name(exercise_data):

     tech = re.sub(
            "[^a-z0-9]+",
            "_",
            exercise_data['technology'].lower()
            )
            
     framework = re.sub(
            "[^a-z0-9]+",
            "_",
            # TODO: make sure all the names has a framework
            str(exercise_data.get('framework')).lower()
            )

     title = re.sub(
            "[^a-z0-9]+",
            "_",
            exercise_data['title'].lower()
            )

     long_uuid = exercise_data.get('uuid', str(uuid.uuid4()))

     if long_uuid[:6] in ('local-', 'sfsdk-'):
         shorter_uuid = long_uuid[:10]
     else:
         shorter_uuid = long_uuid[:4]

     return '%s_%s_%s-%s' % (
         tech,
         framework, 
         title, 
         shorter_uuid
        )


def get_standard_flag_name(flag_data):

     title = re.sub(
            "[^a-z0-9]+",
            "_",
            flag_data['title'].lower()
            )

     flag_type = flag_data['flagList'][0]['type'].lower()

     return '%s_%s' % (title, flag_type)


def ls_exercises():

    exercises = []
    for exercise_yml_path in glob.glob('%s/*/exercise.yml' % workspace_dir):
        exercises.append(exercise_yml_path.split('/')[-2])

    return exercises

def get_exercises(raw = False):

    exercises = {}

    for exercise_yml_path in glob.glob('%s/*/exercise.yml' % workspace_dir):
        exercise_name = exercise_yml_path.split('/')[-2]
        exercise_meta = load_exercise_meta(exercise_name)

        if not raw:

            exercises[exercise_name] = {}

            for field in (
                    'id', 'uuid', 'fromHub', 'title', 'subtitle', 'author', 'score', 
                    'technology', 'trophyname', 'duration', 'difficulty', 'description', 
                    'lastUpdate', 'exerciseType', 'status', 'tags'):

                exercises[exercise_name][field] = exercise_meta.get(field)

        else:

             exercises[exercise_name] = exercise_meta


    return exercises

def get_exercise_by_uuid(uuid):

    for exercise_yml_path in glob.glob('%s/*/exercise.yml' % workspace_dir):

        exercise_name = exercise_yml_path.split('/')[-2]
        exercise_meta = load_exercise_meta(exercise_name)

        if exercise_meta['uuid'] == uuid:
            return exercise_meta

    return {}

def get_exercise_by_name(name):

    exercise_name = None
    for exercise_yml_path in glob.glob('%s/*/exercise.yml' % workspace_dir):

        current_name = exercise_yml_path.split('/')[-2]

        if current_name == name:
            exercise_name = current_name
            break

    if exercise_name:
        return load_exercise_meta(exercise_name)
    else:
        raise log.FatalMsg('The exercise does not exist locally')

def remove_exercise(exercise):

    exercise_dir = os.path.join(workspace_dir, exercise)

    if not os.path.exists(exercise_dir):
        raise log.FatalMsg("Can't find exercise directory")

    if not Path(workspace_dir) in Path(exercise_dir).parents:
        raise log.FatalMsg("Wrong folder")

    shutil.rmtree(exercise_dir)


def load_exercise_meta(exercise):

    exercise_dir = os.path.join(workspace_dir, exercise)

    if not os.path.exists(exercise_dir):
        os.makedirs(exercise_dir)

    exercise_meta_path = os.path.join(exercise_dir, 'exercise.yml')

    exercise_yaml = {}

    try:

        with open(exercise_meta_path, 'r') as stream:

            try:
                exercise_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise log.FatalMsg(exc)

            with open(os.path.join(exercise_dir, 'description.txt.md'), 'r') as stream:
                exercise_yaml['description'] = utils.load_and_replace_media_with_b64(
                    exercise_dir,
                    stream.read()
                )

            with open(os.path.join(exercise_dir, 'information.md'), 'r') as stream:
                exercise_yaml['information']['text'] = utils.load_and_replace_media_with_b64(
                    exercise_dir,
                    stream.read()
                )

            with open(os.path.join(exercise_dir, 'solution.md'), 'r') as stream:
                exercise_yaml['solution']['text'] = utils.load_and_replace_media_with_b64(
                    exercise_dir,
                    stream.read()
                )

            # Skip stack KB
            #with open(os.path.join(exercise_dir, 'stack.md'), 'r') as stream:
            #    exercise_yaml['stack']['md']['text'] = stream.read()

            # Dirty validation on multiple flags with the same name
            added_flag_names = []

            for i, flag_yaml in enumerate(exercise_yaml['flags']):

                flag_name = get_standard_flag_name(flag_yaml)

                if flag_name in added_flag_names:
                    raise log.FatalMsg("Error, flag %s with the same name detected" % (flag_name))
                added_flag_names.append(flag_name)

                # Skip vuln KB
                #flag_path = 'flag_%s_kb.md' % flag_name

                #with open(os.path.join(exercise_dir, flag_path), 'r') as stream:
                #    exercise_yaml['flags'][i]['kb']['md']['text'] = stream.read()

                # Dirty validation here
                if len(flag_yaml['flagList']) > 1:
                    raise log.FatalMsg("Error, more than one flagList per flag")

                flaglist = flag_yaml['flagList'][0]

                flaglist_md_path = 'flag_%s_text.md' % (flag_name)

                # Check if the old flag was named in the same way
                if (
                    exercise_yaml['flags'][i]['flagList'][0]['md']['text'] !=
                    f"!import {flaglist_md_path}"
                ):
                    raise log.FatalMsg(
                        f"Mismatch between the expected flag file '{flaglist_md_path}' and the previous import '{exercise_yaml['flags'][i]['flagList'][0]['md']['text']}'"
                        )

                with open(os.path.join(exercise_dir, flaglist_md_path), 'r') as stream:
                    exercise_yaml['flags'][i]['flagList'][0]['md']['text'] = utils.load_and_replace_media_with_b64(
                        exercise_dir,
                        stream.read()
                    )

                if 'text' in flaglist['hint']['md']:
                    flaglist_hint_md_path = 'flag_%s_hint.md' % (flag_name)

                    # Check if the old flag was named in the same way
                    if (
                        exercise_yaml['flags'][i]['flagList'][0]['hint']['md']['text'] !=
                        f"!import {flaglist_hint_md_path}"
                    ):
                        raise log.FatalMsg(
                            f"Mismatch between the expected flag file '{flaglist_hint_md_path}' and the previous import '{exercise_yaml['flags'][i]['flagList'][0]['hint']['md']['text']}'"
                            )

                    with open(os.path.join(exercise_dir, flaglist_hint_md_path), 'r') as stream:
                        exercise_yaml['flags'][i]['flagList'][0]['hint']['md']['text'] = utils.load_and_replace_media_with_b64(
                            exercise_dir,
                            stream.read()
                        )

    except FileNotFoundError as e:
        raise log.FatalMsg(f"Can't load the metadata: {e.filename} was expected but not found.")

    return exercise_yaml

def save_exercise_meta(exercise_yaml_orig):

    exercise_yaml = copy.deepcopy(exercise_yaml_orig)

    exercise = get_standard_name(exercise_yaml)

    exercise_dir = os.path.join(workspace_dir, exercise)

    if not os.path.exists(exercise_dir):
        os.makedirs(exercise_dir)

    if log.verbose:
        exercise_meta_debug_path = os.path.join(exercise_dir, '.last-saved.json')
        log.debug('Saving JSON debug to %s' % (exercise_meta_debug_path))
        with open(exercise_meta_debug_path, 'w') as f:
              json.dump(exercise_yaml, f, indent=4)

    description = exercise_yaml['description']
    description = utils.save_and_replace_b64_with_media(
        base_folder = exercise_dir,
        content = description,
        content_name = 'description'
    )
    with open(os.path.join(exercise_dir, 'description.txt.md'), 'w+') as stream:
        stream.write(description)

    exercise_yaml['description'] = '!import description.txt.md'

    information_text = exercise_yaml['information']['text']
    information_text = utils.save_and_replace_b64_with_media(
        base_folder = exercise_dir,
        content = information_text,
        content_name = 'information'
    )
    with open(os.path.join(exercise_dir, 'information.md'), 'w+') as stream:
        stream.write(information_text)

    exercise_yaml['information']['text'] = '!import information.md'

    solution_text = exercise_yaml['solution']['text']
    solution_text = utils.save_and_replace_b64_with_media(
        base_folder = exercise_dir,
        content = solution_text,
        content_name = 'information'
    )
    with open(os.path.join(exercise_dir, 'solution.md'), 'w+') as stream:
        stream.write(solution_text)

    exercise_yaml['solution']['text'] = '!import solution.md'

    # Do not store the complete stack KB, but only variant and technology
    try:
        exercise_yaml['stack'] = {
            'technology' : exercise_yaml['stack']['technology'],
            'variant': exercise_yaml['stack']['variant'],
            'uuid': exercise_yaml['stack']['uuid']
        }
    except KeyError as e:
        raise log.FatalMsg(f"Metadata parsing error {e}")


    # Dirty validation on multiple flags with the same name
    added_flag_names = []

    for i, flag_yaml in enumerate(exercise_yaml['flags']):

        flag_name = get_standard_flag_name(flag_yaml)

        if flag_name in added_flag_names:
            raise log.FatalMsg("Error, flag %s with the same name detected" % (flag_name))
        added_flag_names.append(flag_name)

        try:
            # Do not store the complete vulnerability KB, but only category, vulnerability, technology, and isAgnostic
            exercise_yaml['flags'][i]['kb'] = {
                'category' : exercise_yaml['flags'][i]['kb']['category'],
                'vulnerability': exercise_yaml['flags'][i]['kb']['vulnerability'],
                'technology': exercise_yaml['flags'][i]['kb']['technology'],
                'isAgnostic': exercise_yaml['flags'][i]['kb']['isAgnostic'],
                'uuid': exercise_yaml['flags'][i]['kb']['uuid']
            }
        except KeyError as e:
            raise log.FatalMsg(f"Metadata parsing error {e}")

        # Dirty validation on multiple flagList
        if len(flag_yaml['flagList']) > 1:
            raise log.FatalMsg("Error, more than one flagList per flag")

        flaglist = flag_yaml['flagList'][0]
            
        flaglist_md = flaglist['md']['text']
        flaglist_md_path = 'flag_%s_text.md' % (flag_name)

        flaglist_md = utils.save_and_replace_b64_with_media(
            base_folder = exercise_dir,
            content = flaglist_md,
            content_name = flag_name
        )

        with open(os.path.join(exercise_dir, flaglist_md_path), 'w+') as stream:
            stream.write(flaglist_md)

        exercise_yaml['flags'][i]['flagList'][0]['md']['text'] = '!import %s' % flaglist_md_path

        if 'text' in flaglist['hint']['md']:
            flaglist_hint_md = flaglist['hint']['md']['text']
            flaglist_hint_md_path = 'flag_%s_hint.md' % (flag_name)

            flaglist_hint_md = utils.save_and_replace_b64_with_media(
                base_folder = exercise_dir,
                content = flaglist_hint_md,
                content_name = f'{flag_name}_hint'
            )

            with open(os.path.join(exercise_dir, flaglist_hint_md_path), 'w+') as stream:
                stream.write(flaglist_hint_md)

            exercise_yaml['flags'][i]['flagList'][0]['hint']['md']['text'] = '!import %s' % flaglist_hint_md_path
    
    fix_incoming_exercise_data(exercise_yaml)

    with open(os.path.join(exercise_dir, "exercise.yml"), "w") as f:
        yaml.dump(exercise_yaml, f, default_flow_style=False, width=float("inf"))

    return exercise_dir


def update_exercise_folder(old_exercise_dir, new_exercise_data):

    new_exercise_dir = save_exercise_meta(new_exercise_data)

    if old_exercise_dir != new_exercise_dir:
        log.warn("Moved from %s to %s" % (old_exercise_dir, new_exercise_dir))
        shutil.rmtree(old_exercise_dir)


def get_exercise_environment_variable(exercise_name):

    exercise_settings = get_exercise_by_name(exercise_name)
    return base64.b64encode(json.dumps({'title': exercise_settings['title']}).encode())

def fix_incoming_exercise_data(exercise_json):

    # Int-ify status
    exercise_json['status'] = int(exercise_json['status'])

    # Sort by flag type, to keep always the same order
    exercise_json['flags'].sort(key=lambda f: f['flagList'][0]['type'])

    # Delete ids
    utils.recursive_del(exercise_json['flags'], 'id')
    
    try:
        del exercise_json['information']['id']
        del exercise_json['solution']['id']
    except KeyError:
        pass

def fix_outgoing_exercise_data(exercise_json):

    # Int-ify status
    exercise_json['status'] = int(exercise_json['status'])

    # Delete any reference to KBs and Stack UUIDs, let the platform guess by other meta
    utils.recursive_del(exercise_json['flags'], 'uuid')
    utils.recursive_del(exercise_json['stack'], 'uuid')

    # Delete md.id in flags that cause some issue
    utils.recursive_del(exercise_json['flags'], 'id')

def get_path(exercise_name):
   return os.path.join(workspace_dir, exercise_name)

def get_pretty_path(exercise_name):
   return utils.prettypath(os.path.join(workspace_dir, exercise_name))