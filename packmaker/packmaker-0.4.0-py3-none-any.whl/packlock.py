# vim:set ts=4 sw=4 et nowrap syntax=python ff=unix:
#
# Copyright 2019 Mark Crewson <mark@crewson.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os.path
import re

from .framew.application import OperationError
from .framew.log import getlog

##############################################################################


class PackLock (object):

    SUBST_REX = re.compile(r'\${(\w+)(:-(.+))?}')

    def __init__(self, filenames):
        super(PackLock, self).__init__()
        self.log = getlog()
        if not isinstance(filenames, (list, tuple)):
            filenames = [filenames]
        self.lock_filenames = filenames
        self.lockedmods = {}
        self.lockedreps = {}
        self.metadata = {}
        self.files = []
        self.files_fullpath = []
        self.extraopt = {}

    def load(self):
        for filename in self.lock_filenames:
            self.load_one(filename)

    def load_one(self, filename):
        self.log.info('Loading packlock file: {}'.format(filename))
        with open(filename, 'r') as pl:
            lockdict = json.load(pl)
        self.parse(lockdict, filename)

    def parse(self, lockdict, filename):
        version = lockdict.get('version', None)
        if version is None:
            self.parse_ver0(lockdict, filename)
        elif version == '1':
            self.parse_ver1(lockdict, filename)
        else:
            raise OperationError('Unknown format for pack lock file: {}', filename)

    def parse_ver0(self, lockdict, filename):
        # pre-versioned format. Only has locked mods in it
        for slug in lockdict.keys():
            resolveddict = lockdict[slug]
            self.lockedmods[slug] = LockedElement(slug, resolveddict, 'mod')

    def parse_ver1(self, lockdict, filename):
        metadata = lockdict.get('metadata', {})
        if metadata:
            for m in ('name', 'title', 'version', 'authors', 'minecraft_version', 'forge_version'):
                if m in metadata and metadata[m]:
                    val = self.parse_environ_variables(metadata[m])
                    self.set_metadata(m, val)

        parsed_files = lockdict.get('files', [])
        if parsed_files:
            self.files.extend(parsed_files)
            lock_basedir = os.path.dirname(os.path.abspath(filename))
            for parsed_file in parsed_files:
                parsed_location = parsed_file['location']
                if not parsed_location.startswith(os.path.sep):
                    parsed_location = os.path.join(lock_basedir, parsed_location)
                self.files_fullpath.append({'location': parsed_location,
                                            'clientonly': parsed_file.get('clientonly', False),
                                            'serveronly': parsed_file.get('serveronly', False)
                                            })

        self.extraopt.update(lockdict.get('extraopt', {}))
        resolutions = lockdict.get('resolutions')

        mod_resolutions = {}
        rep_resolutions = {}
        for slug, resolution in resolutions.items():
            if 'type' not in resolution:
                mod_resolutions[slug] = resolution
            else:
                if resolution['type'] == 'mod':
                    mod_resolutions[slug] = resolution
                elif resolution['type'] == 'resourcepack':
                    rep_resolutions[slug] = resolution
                else:
                    raise Exception('Unknown resolution type for "{}": {}'.format(slug, resolution['type']))

        self.parse_ver0(mod_resolutions, filename)

        for slug, resolveddict in rep_resolutions.items():
            self.lockedreps[slug] = LockedElement(slug, resolveddict, 'resourcepack')

    def parse_environ_variables(self, val):
        if isinstance(val, list):
            for n in range(len(val)):
                val[n] = self.parse_environ_variables(val[n])

        elif isinstance(val, dict):
            for k, v in val.items():
                val[k] = self.parse_environ_variables(val[k])

        else:
            subst = PackLock.SUBST_REX.search(val)
            while subst:
                var = subst.group(1)
                try:
                    substval = os.environ[var]
                except KeyError:
                    substval = subst.group(3)
                    if substval is None:
                        raise Exception('Undefined environment variable in pack lock file: {}'.format(var))
                val = re.sub(r'\${%s}' % subst.group(0)[2:-1], substval, val)
                subst = PackLock.SUBST_REX.search(val)

        return val

    def save(self):
        resolutions = {}
        for slug, mod in self.lockedmods.items():
            resolutions[slug] = mod.as_dict()
        for slug, rep in self.lockedreps.items():
            resolutions[slug] = rep.as_dict()

        lockdata = {'version': '1',
                    'metadata': self.metadata,
                    'resolutions': resolutions,
                    'files': self.files,
                    'extraopt': self.extraopt
                    }
        lock = json.dumps(lockdata)
        with open(self.lock_filenames[0], 'w') as lockfile:
            lockfile.write(lock)

    def add_resolved_mod(self, moddef, modobj):
        slug = moddef.slug
        if isinstance(modobj, LockedElement):
            self.lockedmods[slug] = modobj
        else:
            self.lockedmods[slug] = LockedElement(slug, modobj, 'mod', moddef)

    def add_resolved_resourcepack(self, repdef, repobj):
        slug = repdef.slug
        if isinstance(repobj, LockedElement):
            self.lockedreps[slug] = repobj
        else:
            self.lockedreps[slug] = LockedElement(slug, repobj, 'resourcepack', repdef)

    def add_files(self, filesdef):
        self.files.append(filesdef)

    def add_extraopt(self, key, extraopt):
        self.extraopt[key] = extraopt

    def set_all_metadata(self, packdef):
        if packdef.name:
            self.set_metadata('name', packdef.name)
        if packdef.title:
            self.set_metadata('title', packdef.title)
        if packdef.version:
            self.set_metadata('version', packdef.version)
        if packdef.authors:
            self.set_metadata('authors', packdef.authors)
        if packdef.minecraft_version:
            self.set_metadata('minecraft_version', packdef.minecraft_version)
        if packdef.forge_version:
            self.set_metadata('forge_version', packdef.forge_version)

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def get_mod(self, slug):
        return self.lockedmods[slug]

    def get_all_mods(self):
        return self.lockedmods.values()

    def get_resourcepack(self, slug):
        return self.lockedreps[slug]

    def get_all_resourcepacks(self):
        return self.lockedreps.values()

    def yield_clientonly_mods(self, include_optional=False):
        for mod in self.lockedmods.values():
            if not include_optional and mod.optional is True:
                continue
            if mod.serveronly is True:
                continue
            yield mod

    def yield_serveronly_mods(self, include_optional=False):
        for mod in self.lockedmods.values():
            if not include_optional and mod.optional is True:
                continue
            if mod.clientonly is True:
                continue
            yield mod

    def yield_clientonly_files(self):
        for files in self.files_fullpath:
            if files['serveronly'] is True:
                continue
            yield files

    def yield_serveronly_files(self):
        for files in self.files_fullpath:
            if files['clientonly'] is True:
                continue
            yield files

    def get_extraopt(self, key):
        return self.extraopt.get(key, None)

    def get_metadata(self, key):
        return self.metadata.get(key, None)

    def get_all_metadata(self):
        return self.metadata

##############################################################################


class LockedElement (object):

    _attrs = ['projectId', 'name', 'fileId', 'fileName', 'author', 'downloadUrl',
              'website', 'version', 'clientonly', 'serveronly', 'optional',
              'recommendation', 'selected', 'description', 'type'
              ]

    def __init__(self, slug, resolveddict, resolvedtype, moddef=None):
        super(LockedElement, self).__init__()
        self.slug = slug
        for attr in self._attrs:
            val = resolveddict.get(attr, None)
            if val is None and moddef is not None and hasattr(moddef, attr):
                val = moddef.__dict__[attr]
            self.__dict__[attr] = val
        self.__dict__['type'] = resolvedtype

    def as_dict(self):
        asdict = {}
        for attr in self._attrs:
            asdict[attr] = self.__dict__[attr]
        return asdict

##############################################################################
# THE END
