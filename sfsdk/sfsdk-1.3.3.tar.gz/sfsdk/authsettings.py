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
import getpass
from ruamel import yaml
from sfsdk import remote

settings = {}
settings_path = None
current_source = ''

default_hub_url = 'https://hub.secureflag.com'

def load(base_dir):
    """ Load or create authentication settings file"""
    global settings, settings_path

    settings_path = os.path.join(base_dir, 'login.yml')

    try:
        with open(settings_path, 'r') as yaml_file:
            settings = yaml.safe_load(yaml_file)
    except OSError as e:
        os.makedirs(base_dir, exist_ok=True)
        settings = {
                'default_source': 'default',
                'sources' : {
                    'default' : {
                        'type': '',
                        'username': '',
                        'password': ''
                    },
                }
            }
        save_to_file()
    except yaml.YAMLError as e:
        raise log.FatalMsg("Settings file %s has broken YAML, delete it to recreate" % settings_path)

    if not settings or not type(settings) is dict:
        raise log.FatalMsg("Settings file %s is not correct, delete it to recreate" % settings_path)

def save_to_file():
    """ Save settings file"""
    global settings

    try:
        with open(settings_path, 'w+') as outfile:
            yaml.dump(settings, outfile, default_flow_style=False)
    except OSError as e:
        log.debug(str(e))
    except yaml.YAMLError as e:
        raise log.FatalMsg("Error saving current settings" % settings_path)

def set_source(source):

    global current_source

    # Check source, default_source if empty
    if not source:
        current_source = settings.get('default_source')
    else:
        current_source = source

    if not current_source: 
        raise log.FatalMsg("Source is not set, re-run with --source or add 'default_source' to %s" % settings_path)

def load_or_ask_for_creds(doing_config = False):

    global settings

    source_settings = settings.get('sources', {}).get(current_source, {})

    if not doing_config and (
            not source_settings.get('username') or 
            not source_settings.get('password') or 
            not source_settings.get('type')
        ):
        log.warn("The authentication to the SecureFlag source '%s' hasn't been configured yet.\nRun 'sfsdk config' to avoid to be prompted again." % (current_source))

    source_type = source_settings.get('type')
    if doing_config or not source_type:
        log.block("Do you manage a SecureFlag Community Edition deployment?", end='\n')
        source_type_ans = input('Yes or No [%s]: ' % ('Yes' if source_type == 'deployment' else 'No') )
        if source_type_ans.lower().startswith('y'):
            source_type = 'deployment'
        elif source_type_ans.lower().startswith('n'):
            source_type = 'hub'
        elif source_type_ans == '':
            source_type = 'hub'
        else:
            raise log.FatalMsg("Unexpected answer")

    if source_type == 'deployment':
        url = source_settings.get('url', '')
        if not url or doing_config:
            log.block('Please type the URL for your SecureFlag deployment', end='\n')
            new_url = input('URL [%s]: ' % url)
            if not new_url or not new_url.startswith('https://'):
                raise log.FatalMsg("URL error, please type the full URL e.g. https://...")
            else:
                url = new_url
    else:
        url = source_settings.get('url', default_hub_url)

    username = source_settings.get('username', '')
    if not username or doing_config:
        if source_type == 'deployment':
            log.block('Please type the username for your SFAdmin user', end='\n')
        else:
            log.block('Please type the username for your SecureFlag Exercise Hub account', end='\n')

        new_username = input('Username: ')
        if new_username:
            username = new_username
        else:
            raise log.FatalMsg("Empty username")

    password = source_settings.get('password', '')
    if not password or doing_config:
        log.block('Please type %s\'s password' % (username), end='\n')
        new_password = getpass.getpass('Password: ')
        if new_password:
            password = new_password
        else:
            raise log.FatalMsg("Empty password")

    # Merge last inserted with the loaded config
    settings['sources'][current_source].update({
        'type': source_type,
        'username': username,
        'password': password,
        'url': url
    })

    return source_type, url, username, password
