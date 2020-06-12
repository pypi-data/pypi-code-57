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

import datetime
import dateutil.parser
import json

from ..curse.curseforge import Curseforge
from ..framew.cmdapplication import Subcommand
from ..framew.config import ConfigError
from ..framew.log import getlog
from ..packdef import PackDefinition

##############################################################################


class LockCommand (Subcommand):
    """
    Lock the modpack. Find mod download urls, generate a packmaker.lock file.
    """

    name = 'lock'

    default_packmaker_yml = 'packmaker.yml'

    def setup(self):
        super(LockCommand, self).setup()
        self.log = getlog()
        self.setup_api()
        self.setup_db()

    def setup_api(self):
        authn_token = self.config.get('curseforge::authentication_token')
        if authn_token is None:
            raise ConfigError('No curseforge authentication token')
        self.api = Curseforge(authn_token)

    def setup_db(self):
        db_filename = self.config.get('curseforge::moddb_filename')
        if db_filename is None:
            raise ConfigError('No moddb_filename parameter in configuration')

        self.log.info('Loading curseforge database ...')
        with open(db_filename, 'r') as cf:
            self.db = json.load(cf)

    def get_cmdline_parser(self):
        parser = super(LockCommand, self).get_cmdline_parser()
        parser.add_argument('packdef',
                            nargs='*',
                            default=[LockCommand.default_packmaker_yml],
                            help='modpack definition file')
        return parser

    def run_command(self, parsed_args):

        self.log.info('Reading pack definition ...')
        pack = PackDefinition(parsed_args.packdef)
        pack.load()

        packlock = pack.get_packlock()
        packlock.set_all_metadata(pack)

        self.resolve_mods(pack, packlock)
        self.resolve_resourcepacks(pack, packlock)

        self.log.info('Adding files...')
        for filesdef in pack.files:
            packlock.add_files(filesdef)

        self.log.info('Adding extra options (if any)...')
        if pack.routhio is not None:
            packlock.add_extraopt('routhio', pack.routhio)

        self.log.info('Writing pack lock...')
        packlock.save()

        self.log.info('Done.')

    def resolve_mods(self, pack, packlock):
        self.log.info('Resolving mods...')
        for moddef in pack.get_all_mods():
            if moddef.slug in self.db:
                modid = self.db[moddef.slug]['id']
                modname = self.db[moddef.slug]['name']
                modauthor = self.db[moddef.slug]['authors'][0]['name']
                modwebsite = self.db[moddef.slug]['websiteUrl']
            else:
                modname, modid, modauthor, modwebsite = self.manual_addon_search(moddef, 6, pack.minecraft_version)

            modfile_found = self.resolve_addon(modid, moddef, pack.minecraft_version)
            if modfile_found is None:
                raise Exception('Cannot find a mod file for {}'.format(moddef.slug))

            packlock.add_resolved_mod(moddef, {'projectId': modid,
                                               'name': modname,
                                               'author': modauthor,
                                               'website': modwebsite,
                                               'fileId': modfile_found['id'],
                                               'fileName': modfile_found['fileName'],
                                               'downloadUrl': modfile_found['downloadUrl']
                                               })

    def resolve_resourcepacks(self, pack, packlock):
        self.log.info('Resolving resourcepacks...')
        for repdef in pack.get_all_resourcepacks():
            if repdef.slug in self.db:
                repid = self.db[repdef.slug]['id']
                repname = self.db[repdef.slug]['name']
                repauthor = self.db[repdef.slug]['authors'][0]['name']
                repwebsite = self.db[repdef.slug]['websiteUrl']
            else:
                repname, repid, repauthor, repwebsite = self.manual_addon_search(repdef, 12, pack.minecraft_version)

            repfile_found = self.resolve_addon(repid, repdef, pack.minecraft_version)
            if repfile_found is None:
                raise Exception('Cannot find a resourcepack file for {}'.format(repdef.slug))

            packlock.add_resolved_resourcepack(repdef, {'projectId': repid,
                                                        'name': repname,
                                                        'author': repauthor,
                                                        'website': repwebsite,
                                                        'fileId': repfile_found['id'],
                                                        'fileName': repfile_found['fileName'],
                                                        'downloadUrl': repfile_found['downloadUrl']
                                                        })

    def manual_addon_search(self, addondef, addontype, gameversion):
        self.log.info('  Cannot find addon in local db: {}\n  Manually searching...'.format(addondef.slug))

        searchresults = list(({'name': addon['name'], 'id': addon['id'], 'slug': addon['slug'],
                               'authors': addon['authors'], 'websiteUrl': addon['websiteUrl']}
                              for addon in self.api.yield_addons_by_criteria(gameId=432, sectionId=addontype,
                                                                             gameVersions=gameversion,
                                                                             searchFilter=addondef.slug)))

        if len(searchresults) < 1:
            raise Exception('Cannot find an addon named \'{}\''.format(addondef.slug))
        elif len(searchresults) > 1:
            self.log.info('    Multiple search results found ({}).  Looking for an exact match in results...'
                          .format(len(searchresults)))
            for sresult in searchresults:
                if sresult['slug'] == addondef.slug:
                    searchresult = sresult
                    self.log.info('    Found it! ... {} (id = {})'.format(searchresult['slug'], searchresult['id']))
                    break
            else:
                searchresult = searchresults[0]
                self.log.info('    No exact match found! Using the first one (this could be wildly wrong) ... {} (id = {})'
                              .format(searchresult['slug'], searchresult['id']))
        else:
            searchresult = searchresults[0]
            self.log.info('    Found it! ... {} (id = {})'.format(searchresult['slug'], searchresult['id']))

        return (searchresult['name'], searchresult['id'], searchresult['authors'][0]['name'], searchresult['websiteUrl'])

    def resolve_addon(self, id, addondef, gameversion):
        latestTimestamp = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
        addon_found = None
        for addonfile in self.api.get_addon_files(id):
            if gameversion not in addonfile['gameVersion']:
                continue
            if addondef.version == 'latest':
                timestamp = dateutil.parser.parse(addonfile['fileDate'])
                if timestamp > latestTimestamp:
                    addon_found = addonfile
                    latestTimestamp = timestamp

            elif addonfile['fileName'] == addondef.version:
                addon_found = addonfile

        return addon_found

##############################################################################
# THE END
