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

import os

import yaml
try:
    yamlload = yaml.full_load
except AttributeError:
    yamlload = yaml.load

from .packlock import PackLock

##############################################################################


class PackDefinition (object):

    def __init__(self, filenames):
        super(PackDefinition, self).__init__()
        self.definition_filenames = filenames
        self.name = None
        self.title = None
        self.version = None
        self.authors = []
        self.icon = None
        self.news = None
        self.minecraft_version = None
        self.forge_version = None
        self.routhio = None
        self.mods = {}
        self.resourcepacks = {}
        self.files = []

    def load(self):
        for filename in self.definition_filenames:
            self.load_one(filename)

    def load_one(self, filename):
        with open(filename, 'r') as pf:
            packtext = pf.read()
        packdict = yamlload(packtext)
        self.populate(packdict)

    def populate(self, packdict):
        if 'name' in packdict:
            self.name = packdict['name']
        if 'title' in packdict:
            self.title = packdict['title']
        if 'version' in packdict:
            self.version = packdict['version']
        if 'authors' in packdict:
            self.authors.extend(packdict['authors'])
        if 'icon' in packdict:
            self.icon = packdict['icon']
        if 'news' in packdict:
            self.news = packdict['news']
        if 'minecraft' in packdict:
            self.minecraft_version = packdict['minecraft']
        if 'forge' in packdict:
            self.forge_version = packdict['forge']
        if 'routhio' in packdict:
            self.routhio = packdict['routhio']

        if 'mods' in packdict:
            for mod in packdict['mods']:
                if type(mod) is str:
                    slug, moddef = mod, None
                else:
                    slug, moddef = mod.popitem()
                self.mods[slug] = ModDefinition(slug, moddef)

        if 'resourcepacks' in packdict:
            for resp in packdict['resourcepacks']:
                if type(resp) is str:
                    slug, respdef = resp, None
                else:
                    slug, respdef = resp.popitem()
                self.resourcepacks[slug] = ResourcepackDefinition(slug, respdef)

        if 'files' in packdict:
            self.files.extend(packdict['files'])

    def get_mod(self, slug):
        return self.mods[slug]

    def get_all_mods(self):
        return self.mods.values()

    def get_resourcepack(self, slug):
        return self.resourcepacks[slug]

    def get_all_resourcepacks(self):
        return self.resourcepacks.values()

    def get_packlock(self):
        lockfile = os.path.splitext(self.definition_filenames[0])[0] + '.lock'
        return PackLock(lockfile)

##############################################################################


class PackElementDefinition (object):

    default_version = 'latest'
    default_optional = False
    default_recommendation = 'starred'
    default_selected = False

    def __init__(self, slug, elem):
        super(PackElementDefinition, self).__init__()
        self.slug = slug
        self.populate(elem)

    def populate(self, elem):
        if elem is not None:
            self.version = elem.get('version', self.default_version)
            self.optional = elem.get('optional', self.default_optional)
            self.recommendation = elem.get('recommendation', self.default_recommendation)
            self.selected = elem.get('selected', self.default_selected)
        else:
            self.version = self.default_version
            self.optional = self.default_optional
            self.recommendation = self.default_recommendation
            self.selected = self.default_selected

        if self.recommendation not in ('starred', 'avoid'):
            raise Exception('mod recommendation for "{}" must be either "starred" or "avoid"'.format(self.slug))


class ModDefinition (PackElementDefinition):

    default_clientonly = False
    default_serveronly = False

    def __init__(self, slug, moddef):
        super(ModDefinition, self).__init__(slug, moddef)

    def populate(self, moddef):
        super(ModDefinition, self).populate(moddef)
        if moddef is not None:
            self.clientonly = moddef.get('clientonly', ModDefinition.default_clientonly)
            self.serveronly = moddef.get('serveronly', ModDefinition.default_serveronly)
        else:
            self.clientonly = ModDefinition.default_clientonly
            self.serveronly = ModDefinition.default_serveronly


class ResourcepackDefinition (PackElementDefinition):

    def __init__(self, slug, respdef):
        super(ResourcepackDefinition, self).__init__(slug, respdef)

##############################################################################
# THE END
