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

##############################################################################

class Library (object):

    CURSECDN_URL_BASE = 'https://modloaders.cursecdn.com/647622546/maven/'

    def __init__(self, library):
        super(Library, self).__init__()
        self.library = library
        parts = self.library['name'].split(':')
        self.group, self.artifact, self.version = parts[:3]
        self.type = parts[3] if len(parts) >= 4 else None
        self.extension = 'jar'
        if '@' in self.version:
            self.version, self.extension = self.version.split('@', 1)

    def get_native_string(self):
        if 'natives' in self.library:
            return self.library['natives']['linux']
        return None

    def get_filename(self):
        nativestring = self.get_native_string()
        if nativestring:
            return '{}-{}-{}.{}'.format(self.artifact, self.version, nativestring, self.extension)
        elif self.type is not None:
            return '{}-{}-{}.{}'.format(self.artifact, self.version, self.type, self.extension)
        return '{}-{}.{}'.format(self.artifact, self.version, self.extension)

    def get_path(self):
        if 'path' in self.library:
            return self.library['path']

        if 'downloads' in self.library:
            nativestring = self.get_native_string()
            if nativestring:
                return self.library['downloads']['classifiers'][nativestring]['path']
            else:
                return self.library['downloads']['artifact']['path']

        return '{}/{}/{}/{}'.format(self.group.replace('.', '/'),
                                    self.artifact,
                                    self.version,
                                    self.get_filename())

    def get_download_url(self):
        if 'downloads' in self.library:
            nativestring = self.get_native_string()
            if nativestring:
                return self.library['downloads']['classifiers'][nativestring]['url']
            else:
                return self.library['downloads']['artifact']['url']
        if 'url' in self.library:
            return '{}{}'.format(self.library['url'], self.get_path())
        return None

    def get_alternate_download_url(self):
        if not self.get_native_string():
            return '{}{}'.format(self.CURSECDN_URL_BASE, self.get_path())
        return None

    def get_artifact(self):
        return '{}:{}'.format(self.group, self.artifact)

    def matches(self, environment):
        if 'rules' not in self.library:
            return True

        allow = False
        for rule in self.library['rules']:
            if self.matches_rule(rule, environment):
                allow = rule['action'] == 'allow'
        return allow

    def matches_rule(self, rule, environment):
        if 'os' in rule:
            return rule['os']['name'] == 'linux'
        return True

    def must_extract(self):
        return 'natives' in self.library

    def extract_excludes(self):
        excludes = []
        if 'extract' in self.library and 'exclude' in self.library['extract']:
            excludes = self.library['extract']['exclude']
        return excludes

##############################################################################
# THE END
