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

from sfsdk import log, containers, utils
import os
import os.path
import yaml
import requests
import shutil

settings = {}

workspace_dir = None
settings_path = None

def get_container_conf(image_name):
    
    image_settings = settings['images'][image_name]['container']

    container_run_conf = {
        'image': image_settings['image_name'],
        'name': image_settings['container_name'],
        'ports': {
            # RDP
            3389: ( '127.0.0.1', image_settings['external_rdp_port']),
            # HTTP
            image_settings['internal_http_port']: ('127.0.0.1', image_settings['external_http_port']),
            },
        'cap_add': [] if image_settings['allow_internet'] else [ 'NET_ADMIN' ],
        'environment': { 
            'USR_PWD': image_settings['rdp_password'],
            'ALLOW_INTERNET': 'true' if image_settings['allow_internet'] else 'false'
            }
    }

    container_run_conf['environment'].update(image_settings.get('environment', {}))

    return container_run_conf

def get_settings(image_name):
    # Generate the settings for a built container
    return [
        {
            'name': 'image_name',
            'default': image_name,
            'validate': lambda answer: "Invalid choice" if not answer else True
            },
        {
            'name': 'container_name',
            'default': '%s-inst' % (image_name),
            'validate': lambda answer: "Invalid choice" if not answer else True
            },
        {
            'name': 'rdp_password',
            'default': 'password',
            'validate': lambda answer: "Invalid choice" if not answer else True
            },
        {
            'name': 'allow_internet',
            'default': True,
            },
        {
            'name': 'external_rdp_port',
            'default': '3389',
            'validate': lambda answer: "Invalid choice" if not answer.isdigit() or not 0 < int(answer) < 65535 else True
            },
        {
            'name': 'external_http_port',
            'default': '8050',
            'validate': lambda answer: "Invalid choice" if not answer.isdigit() or not 0 < int(answer) < 65535 else True
            },
        {
            'name': 'internal_http_port',
            'default': '80',
            'validate': lambda answer: "Invalid choice" if not answer.isdigit() or not 0 < int(answer) < 65535 else True
            },
        {
            'name': 'environment',
            'default': {}
        }
    ]

def _check_existing_image_structure(build_dir):

    build_fs_dir = os.path.join(build_dir, 'fs/') 
    build_app_dir = os.path.join(build_dir, 'app/')
    build_dockerfile = os.path.join(build_dir, 'Dockerfile')

    return os.path.exists(build_fs_dir) or os.path.exists(build_app_dir) or os.path.exists(build_dockerfile)

def _create_image_structure(image_name, base_img, from_dir, app_dir):

    image_settings = settings['images'][image_name]

    # Create base folder 
    os.makedirs(os.path.join(workspace_dir, image_name), exist_ok=True) 

    build_dir = image_settings['build_dir']

    build_fs_dir = os.path.join(build_dir, 'fs/') 
    build_app_dir = os.path.join(build_dir, 'app/')
    build_dockerfile = os.path.join(build_dir, 'Dockerfile')

    os.makedirs(build_fs_dir, exist_ok=True) 
    os.makedirs(build_app_dir, exist_ok=True) 

    # Warn if import has been requested but the build dir is not empty
    # This actually copies only the Dockerfile, app, and fs dir
    if from_dir:

        if not os.path.isdir(from_dir) or not os.listdir(from_dir):
            log.warn('Directory %s can\'t be imported because missing or empty' % (from_dir))
        else:
            utils.merge_tree(os.path.join(from_dir, 'fs'), build_fs_dir)
            utils.merge_tree(os.path.join(from_dir, 'app'), build_app_dir)
            shutil.copy(os.path.join(from_dir, 'Dockerfile'), build_dockerfile)
            log.header('Build directory has been copied to %s' % (build_dir))

    if app_dir:

        if not os.path.isdir(app_dir) or not os.listdir(app_dir):
            log.warn('Application directory %s can\'t be imported because missing or empty' % (app_dir))
        else:
            utils.merge_tree(app_dir, build_app_dir)
            log.header('Application directory has been copied to %s' % (build_app_dir))

    if not os.path.exists(os.path.join(build_dir, 'Dockerfile')):
        containers.generate_dockerfile(build_dir, base_img)

def remove_image(image_name, force):

    img_dir = settings['images'][image_name]['build_dir']

    if os.path.isdir(img_dir):
        if not force:
            log.warn("Image directory %s exists, but it hasn't been deleted. Re-run with --force" %  img_dir)
        else:            
            log.warn("Image directory %s has been deleted" %  img_dir)
            shutil.rmtree(img_dir)

    try:
        containers.image_remove(image_name)
    except log.FatalMsg as e:
        log.warn(e)

    try:
        del settings['images'][image_name]
    except KeyError:
        if not force:
            raise log.FatalMsg("Didn't find image %s in images.yml" %  image_name)


    save()

def add_image_settings(image_name, base_img = None, build_dir = None, from_dir = None, app_dir = None, container_settings = {}):

    if not build_dir:
        build_dir = os.path.join(workspace_dir, image_name, 'build')

    # build_dir must be absolute
    build_dir = os.path.abspath(build_dir)

    if settings.get('images').get(image_name):
        raise log.FatalMsg('Image %s already exists. Remove it with img-rm and retry.' % image_name)

    settings['images'][image_name] = {
            'base_img': base_img,
            'build_dir': build_dir,
            'container': container_settings
        }

    if _check_existing_image_structure(build_dir):
        log.warn('Build directory %s already contains the image structure, skipping its initialization.' % build_dir)
    else:
        _create_image_structure(image_name, base_img, from_dir, app_dir)

    save()

def load(base_dir):
    """ Load or create workspace and settings file"""
    global settings, workspace_dir, settings_path

    workspace_dir = os.path.join(
            base_dir,
            'img'
    )
    settings_path = os.path.join(
        base_dir, 
        'images.yml'
    )

    try:
        with open(settings_path, 'r') as yaml_file:
            settings = yaml.safe_load(yaml_file)
    except OSError as e:
        os.makedirs(workspace_dir, exist_ok=True)
        settings = {
                'images' : {},
                }
        save()
    except yaml.YAMLError as e:
        raise log.FatalMsg("Settings file %s has broken YAML, delete it to recreate" % settings_path)

def save():
    """ Save settings file"""
    global settings

    try:
        with open(settings_path, 'w+') as outfile:
            yaml.dump(settings, outfile, default_flow_style=False)
    except OSError as e:
        log.debug(str(e))
        os.makedirs(workspace_dir, exist_ok=True)
    except yaml.YAMLError as e:
        raise log.FatalMsg("Error saving current settings" % settings_path)

def get_package_path():
    return os.path.dirname(os.path.realpath(__file__))

def resolve_images(names):

    if len(names) == 1 and names[0] == 'all':
        return list(settings.get('images', {}).keys())
    else:
        return names

def get_snapshot_name(name):

    while name in settings['images'].keys():

        try:
            img_name, version_raw = name.rsplit('-v', 1)
            version = int(version_raw) + 1
        except (IndexError, ValueError):
            img_name = name
            version = 1

        name = '%s-v%d' % (img_name, version)

    return name