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
import requests
import shutil
import subprocess
import zipfile

from .framew.log import getlog
from .libraries import Library
from .minecraft import Minecraft

##############################################################################


class Forge (object):

    FORGE_REPO_URL = 'https://files.minecraftforge.net/maven/'

    INCOMPATIBLE_FORGE_VERSIONS = ['14.23.5.2851']

    BUILD_THAT_CHANGED_UNIVERSAL_FILENAME = 2851

    ##########################################################################

    def __init__(self, minecraft_version, forge_version, downloader):
        super(Forge, self).__init__()
        self.minecraft_version = minecraft_version
        self.forge_version = forge_version
        self.full_version = '{}-{}'.format(minecraft_version, forge_version)
        self.downloader = downloader
        self.installer_jar_filename = None
        self.install_profile = None
        self.version_info = None

        if self.forge_version in Forge.INCOMPATIBLE_FORGE_VERSIONS:
            raise Exception('Sorry. Forge version {} does not work with '.format(self.forge_version)
                            + 'packmaker. Upgrade to a newer version if possible.')

        self.log = getlog()

    ##########################################################################

    def installer_filename(self):
        return 'forge-{}-installer.jar'.format(self.full_version)

    ##########################################################################

    def installer_path(self):
        return 'net/minecraftforge/forge/{}/{}'.format(self.full_version,
                                                       self.installer_filename())

    ##########################################################################

    def installer_download_url(self):
        return '{}/{}'.format(Forge.FORGE_REPO_URL, self.installer_path())

    ##########################################################################

    def universal_filename(self):
        if self.minecraft_version == '1.12.2':
            build_num = int(self.forge_version.split('.')[-1])
            if build_num >= Forge.BUILD_THAT_CHANGED_UNIVERSAL_FILENAME:
                return 'forge-{}.jar'.format(self.full_version)
        return 'forge-{}-universal.jar'.format(self.full_version)

    ##########################################################################

    def universal_path(self):
        return 'net/minecraftforge/forge/{}/{}'.format(self.full_version,
                                                       self.universal_filename())

    ##########################################################################

    def universal_download_url(self):
        return '{}/{}'.format(Forge.FORGE_REPO_URL, self.universal_path())

    ##########################################################################

    def get_install_profile(self):
        if self.install_profile is None:
            installer_filename = self.get_installer_jar()
            with zipfile.ZipFile(installer_filename, 'r') as installerjar:
                with installerjar.open('install_profile.json', 'r') as installf:
                    self.install_profile = json.load(installf)
        return self.install_profile

    ##########################################################################

    def get_installer_jar(self):
        if self.installer_jar_filename is None:
            self.installer_jar_filename = self.downloader.download(self.installer_download_url())
        return self.installer_jar_filename

    ##########################################################################

    def get_universal_jar(self, filename=None):
        installer_filename = self.get_installer_jar()
        if filename is None:
            filename = os.path.join(os.path.dirname(installer_filename), self.universal_filename())

        with zipfile.ZipFile(installer_filename, 'r') as installerjar:
            try:
                universal_filename = installerjar.getinfo(self.universal_filename())
            except KeyError:
                try:
                    universal_filename = installerjar.getinfo('maven/{}'.format(self.universal_path()))
                except KeyError:
                    raise Exception('Cannot find {} in the forge jar file: {}'
                                    .format(self.universal_filename(), installer_filename))

            with open(filename, 'wb') as outjar:
                with installerjar.open(universal_filename, 'r') as injar:
                    shutil.copyfileobj(injar, outjar)

    ##########################################################################

    def get_version_info(self):
        if self.version_info is not None:
            return self.version_info

        installer_filename = self.get_installer_jar()
        with zipfile.ZipFile(installer_filename, 'r') as installerjar:
            try:
                with installerjar.open('version.json', 'r') as installf:
                    self.version_info = json.load(installf)
            except KeyError:
                install_profile = self.get_install_profile()
                if 'versionInfo' in install_profile:
                    self.version_info = install_profile['versionInfo']

        return self.version_info

    ##########################################################################

    def get_launch_arguments(self):
        version_info = self.get_version_info()
        if 'arguments' in version_info:
            return ' '.join([arg for arg in version_info['arguments']['game'] if type(arg) == str])

        elif 'minecraftArguments' in version_info:
            return version_info['minecraftArguments']

    ##########################################################################

    def get_mainclass(self):
        version_info = self.get_version_info()
        return version_info['mainClass']

    ##########################################################################

    def get_dependent_libraries(self):
        dependents = []
        version_info = self.get_version_info()
        libraries = version_info['libraries']
        for lib in libraries:
            library = Library(lib)
            if library.matches(None):
                dependents.append(library)
        return dependents

    def get_installer_libraries(self):
        dependents = []
        install_profile = self.get_install_profile()
        if 'libraries' in install_profile:
            for lib in install_profile['libraries']:
                library = Library(lib)
                if library.matches(None):
                    dependents.append(library)
        return dependents

    ##########################################################################

    def install_dependent_libraries(self, cache_location, install_location):
        dependent_libs = self.get_dependent_libraries()
        self.install_libraries(cache_location, install_location, dependent_libs)

    def install_installer_libraries(self, cache_location, install_location):
        installer_libs = self.get_installer_libraries()
        self.install_libraries(cache_location, install_location, installer_libs)

    def install_libraries(self, cache_location, install_location, libraries):
        for library in libraries:
            cached_library = os.path.join(self.downloader.download_dir, library.get_path())

            url = library.get_alternate_download_url()
            try:
                self.downloader.download(url, library.get_path())
            except requests.exceptions.HTTPError:
                url = library.get_download_url()
                if url is not None:
                    self.downloader.download(url, library.get_path())
                else:
                    continue
                    # raise Exception('Cannot download forge dependent library: {}'.format(url))

            local_library = os.path.join(install_location, library.get_path())
            if not os.path.exists(os.path.dirname(local_library)):
                os.makedirs(os.path.dirname(local_library))

            shutil.copy2(cached_library, local_library)

    def run_processors(self, install_location, side):
        install_profile = self.get_install_profile()

        if 'processors' not in install_profile:
            return

        self.log.info('Processing installer data ...')
        data = {}
        if 'data' in install_profile:
            for datakey, dataval in install_profile['data'].items():
                dataval = dataval[side]
                if dataval.startswith('[') and dataval.endswith(']'):
                    # artifact
                    data[datakey] = os.path.join(install_location,
                                                 mavenname_to_path(dataval[1:-1]))

                elif dataval.startswith('\'') and dataval.endswith('\''):
                    # literal
                    data[datakey] = dataval[1:-1]

                else:
                    self.log.info('  Extracting: {}'.format(dataval))

                    data_location = os.path.join(install_location, 'data')
                    if not os.path.exists(data_location):
                        os.makedirs(data_location)

                    installerjar = self.get_installer_jar()
                    with zipfile.ZipFile(installerjar, 'r') as installer:
                        installer.extract(dataval.lstrip('/'), data_location)

                    data[datakey] = os.path.join(data_location, dataval.lstrip('/'))

        manifest = Minecraft(self.minecraft_version).get_version_manifest()

        data['SIDE'] = side
        data['MINECRAFT_JAR'] = os.path.join(install_location, 'com', 'mojang', 'minecraft',
                                             manifest['id'], 'minecraft-{}-{}.jar'.format(manifest['id'], side))

        self.log.info('Executing forge installer processors ...')
        processors = install_profile['processors']

        i = 0
        for proc in processors:
            i += 1
            self.log.info('  Running {} of {} processors ...'.format(i, len(processors)))

            classpath = proc['classpath']
            args = proc['args']

            finalargs = []
            for arg in args:
                if arg.startswith('{') and arg.endswith('}'):
                    arg = data[arg[1:-1]]
                elif arg.startswith('[') and arg.endswith(']'):
                    arg = os.path.join(install_location,
                                       mavenname_to_path(arg[1:-1]))

                finalargs.append(arg)

            classpath = [os.path.join(install_location, mavenname_to_path(proc['jar']))]
            for lib in proc['classpath']:
                classpath.append(os.path.join(install_location, mavenname_to_path(lib)))

            mainclass = find_mainclass_in_jar(os.path.join(install_location,
                                                           mavenname_to_path(proc['jar'])))

            cmd = ['java', '-cp', ':'.join(classpath), mainclass]
            cmd.extend(finalargs)

            print('DEBUG: cmd = {}'.format(' '.join(cmd)))
            result = subprocess.run(cmd)
            if result.returncode != 0:
                raise Exception('Processor finished with errors. Abort')

##############################################################################


def mavenname_to_path(name):
    parts = name.split(':')
    filename = '{}-{}'.format(parts[2], parts[3]) if len(parts) >= 4 else parts[2]
    filename = filename.replace('@', '.') if '@' in filename else '{}.jar'.format(filename)
    initpath = parts[0].split('.')
    initpath.append(parts[1])
    initpath.append(parts[2].split('@')[0])
    initpath.append('{}-{}'.format(parts[1], filename))
    return '/'.join(initpath)


def find_mainclass_in_jar(jarfile):
    with zipfile.ZipFile(jarfile, 'r') as jar:
        with jar.open('META-INF/MANIFEST.MF', 'r') as manifest:
            lines = manifest.readlines()
            print('DEBUG: lines = {}'.format(lines))
            for line in lines:
                line = line.decode('utf-8').strip()
                if line.startswith('Main-Class:'):
                    return line.split(' ')[1]
    return None

##############################################################################
# THE END
