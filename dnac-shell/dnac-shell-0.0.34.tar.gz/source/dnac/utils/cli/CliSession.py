from signal import signal, SIGINT
import copy
import shlex
import argparse
import time
from sys import exit
import requests
import socket
import getopt
import sys
import datetime
from datetime import datetime
import os
from dnac.utils.cli.SessionState import SessionState
from dnac.service.site.SiteType import SiteType
from dnac.DnacCluster import DnacCluster
from dnac.service.site.Site import Site
from dnac.service.maps.Floor import Floor
from dnac.service.maps.FloorGeometry import FloorGeometry
from dnac.service.site.Building import Building
from dnac.service.maps.export.DnacMapExporter import DnacMapExporter
from dnac.utils.os.FileSystem import FileSystem


# copyright (c) 2020 cisco Systems Inc., ALl righhts reseerved
# @author rks@cisco.com

class CliSession:
    def __init__(self, dnac_cluster=None):
        self.__cwd__ = None, None
        self.__state__ = SessionState.UNINITIALIZED
        self.__num_children_sites__ = 0
        self.__versionx__ = '<Unknown>'
        self.__prompt__ = 'DNAC Maps> '
        self.__dnac_cluster__ = dnac_cluster
        self.__batch_file__ = None
        signal(SIGINT, CliSession.handler)

    @property
    def dnac_cluster(self):
        return self.__dnac_cluster__

    @dnac_cluster.setter
    def dnac_cluster(self, given_cluster):
        self.__dnac_cluster__ = given_cluster

    @property
    def prompt(self):
        return self.__prompt__

    @property
    def state(self):
        return self.__state__

    @state.setter
    def state(self, new_state):
        self.__state__ = new_state

    @property
    def cwd(self):
        return self.__cwd__

    @cwd.setter
    def cwd(self, newcwd):
        self.__cwd__ = newcwd

    @property
    def num_children_sites(self):
        return self.__num_children_sites__

    @property
    def version(self):
        return self.__versionx__

    @property
    def batch_file(self):
        return self.__batch_file__

    @batch_file.setter
    def batch_file(self, command_file):
        self.__batch_file__ = command_file

    def batch(self, command_file):
        self.batch_file = open(command_file, 'r') if FileSystem.is_file_readable(command_file) else None
        self.start()

    def start(self):
        if self.dnac_cluster:
            self.cwd = 'Global', self.dnac_cluster.global_site.id, SiteType.SITE
            self.state = SessionState.RUNNING
        else:
            self.state = SessionState.UNINITIALIZED
        self.shell()
        self.cwd = 'Global', self.dnac_cluster.global_site, SiteType.SITE
        self.state = SessionState.STOPPED

    @staticmethod
    def site_type(typeenum):
        if typeenum == SiteType.FLOOR:
            return 'Floor'
        if typeenum == SiteType.BUILDING:
            return 'Building'
        return 'Site'

    @staticmethod
    def preamble():
        requests.packages.urllib3.disable_warnings()
        print(' ')
        print('*** DNAC Map Shell, (c) 2020 cisco Systems Inc. ***')
        print('***           ver. 2.1, Jun 2020                ***')
        print(' ')

    def cd(self, site=None):
        sitex = self.dnac_cluster.groupingService.discover_site_hierarchy(site)
        if isinstance(sitex, list):
            sitex = sitex[0] if len(sitex) > 0 else None
        if not sitex:
            print('??? Unrecognized site: "', site, '"')
        else:
            typex = SiteType.UNKNOWN
            if isinstance(sitex, Floor):
                typex = SiteType.FLOOR
            elif isinstance(sitex, Building):
                typex = SiteType.BUILDING
            else:
                typex = SiteType.SITE

            self.cwd = site, sitex.id, typex

        self.do_prompt()

    def get_full_path(self, rel_path):
        rel_path = rel_path.strip() if rel_path else None
        if not rel_path or rel_path == '.':
            return self.cwd[0]
        rel_path = os.path.normpath(rel_path)
        if rel_path == '..':
            brk = self.cwd[0].split('/')
            if brk and len(brk) > 0:
                brk.pop()
                rel_path = '/'.join(brk)
        elif rel_path.startswith('/'):
            if rel_path == '/Global':
                rel_path = 'Global'
            elif rel_path.startswith('/Global/'):
                rel_path = rel_path[1:]
            elif not rel_path.startswith('Global/'):
                rel_path = 'Global' + rel_path
        elif rel_path == '~':
            rel_path = 'Global'
        else:
            rel_path = os.path.join(self.cwd[0], rel_path)
            rel_path = os.path.normpath(rel_path)
        return rel_path.strip() if rel_path.startswith('Global') else None

    def usage(self, command, *kwargs):
        if command:
            if command == 'login':
                print('Usage: ', 'login [to <dnac-ip> [as <dnac-admin-user> [using password <dnac-admin-password>]]]')
                return

            if command == 'cd':
                print('Usage: ', 'cd [<site hierarchy>]')
                return

            if command == 'export':
                print('Usage: ', 'export [--map-archive|--bulk-apa] --file <file>]')
                return

            if command == 'pwd' or command == 'info' or command == 'date':
                print('Usage: ', command)
                return
        print('??' + command + '??')
        return

    def execute_server(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        versx = str(self.dnac_cluster.version) if self.dnac_cluster.version else '<Unknown>'
        print('[DNAC Server: ' + self.dnac_cluster.address + ', vers. ' + versx + ']')

    def execute_info(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        self.execute_server()
        self.execute_pwd()
        print('Number of children sites: ', self.num_children_sites)

    def execute_pwd(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        print(CliSession.site_type(self.cwd[2]) + ': ' + self.cwd[0] + '\t, Id: ' + self.cwd[1])

    def execute_version(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        print('DNAC Version: ', self.dnac_cluster.version)

    def execute_date(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%b %d %Y, %H:%M:%S")
        print(dt_string, time.localtime().tm_zone)

    def execute_time(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        print(datetime.now().strftime("%H:%M:%S"))

    def execute_export_map(self, root, file):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        saved_file = DnacMapExporter.do_export(self.dnac_cluster, root, file)
        print(' ')
        if saved_file:
            print('*** Export completed: archive file: ', saved_file)
        return

    def list_floor_aps(self):
        elements = self.dnac_cluster.mapService.discover_floor_aps(self.cwd[1])
        element_count = len(elements) if elements else 0
        print('=> ' + str(element_count) + ' Access Points ')

    def list_floor_paps(self):
        elements = self.dnac_cluster.mapService.discover_floor_paps(self.cwd[1])
        element_count = len(elements) if elements else 0
        print('=> ' + str(element_count) + ' Planned Access Points ')

    def execute_ls(self):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        print(' ')
        print('[' + CliSession.site_type(self.cwd[2]) + ': ' + self.cwd[0] + ']')
        if self.cwd[2] == SiteType.FLOOR:
            print('*** Items on the floor area: ')
            self.list_floor_aps()
            self.list_floor_paps()
            print(' ')
        else:
            children = self.dnac_cluster.groupingService.discover_site_children(self.cwd[1])
            for child in children:
                print(child.name, "\t", child.id)
        self.do_prompt()

    def execute_login(self, args):
        l = len(args) if args else 0
        if l == 1 or l == 3 or l == 5 or l == 6 or l > 7:
            print('099')
            self.usage('login')
            return
        if l > 1:
            token = args[0]
            rest = args[1:]
        else:
            token, *rest = None, None
        if token and (token != 'to'):
            print('199')
            self.usage('login')
            return

        if rest and len(rest) > 0:
            dnac_ip = rest[0]
            rest = rest[1:]
        else:
            dnac_ip = None
            rest = None

        using_token = None
        password_token = None
        dnac_password = None
        dnac_ip = dnac_ip if dnac_ip else input('DNAC Address: ')
        if rest and len(rest) == 2:
            token, admin_user = rest[0], rest[1]
        elif rest and len(rest) == 5:
            token, admin_user, using_token, password_token, dnac_password = rest[0], rest[1], rest[2], rest[3], rest[4]
        else:
            token, admin_user = None, None
        if token and (token != 'as' or not admin_user):
            print('299')
            self.usage('login')
            return

        if using_token != 'using' or password_token != 'password':
            print('399')
            self.usage('login')
            return

        if admin_user:
            dnac_password = dnac_password if dnac_password else DnacCluster.get_password()
            dnac_credentials = (admin_user, dnac_password)
        else:
            dnac_credentials = DnacCluster.get_credentials()
        self.dnac_cluster = DnacCluster(socket.getfqdn(dnac_ip), dnac_credentials)
        try:
            self.dnac_cluster.login_as(dnac_credentials)
        except requests.exceptions.ConnectionError:
            print('??? Unable to reach ' + dnac_ip + ' - did yiu mistype IP/FQDN?')
            self.usage('login')
            self.dnac_cluster = None
            return
        if not self.dnac_cluster.global_site:
            print('??? Unable to connect to ' + dnac_ip + ' - did you mistype IP/FQDN?')
            return

        if self.dnac_cluster.valid_session():
            print('[Connected: ', self.dnac_cluster.address + ']')
            self.start()
        else:
            print('??? Invalid credentials - retry')

    def execute_cd(self, args):
        if self.state != SessionState.RUNNING:
            print('??? Not connected')
            return
        if not args:
            self.cd()
            return
        site = self.get_full_path(args)
        if not site:
            self.usage('cd', 'Cannot navigate to unknown site "' + site + '"')
            return
        self.cd(site)
        return

    def do_prompt(self):
        print(self.prompt)

    #
    # Obtain the next command either rom batch file (if in batch mode)
    # or interactively from user
    #
    def get_next_command(self):
        if self.batch_file:
            next_command = self.batch_file.readline()
            if next_command == '':
                next_command = 'exit'
            temp_copy_of_command = next_command.split()
            if 'login' in next_command and 'using' in next_command and 'password' in next_command:
                temp_copy_of_command = temp_copy_of_command[:7] if len(temp_copy_of_command) > 7 else temp_copy_of_command
                temp_copy_of_command.append('<masked>')
            print(self.prompt + ' '.join(temp_copy_of_command))
        else:
            next_command = input(self.prompt)
        return next_command

    def shell(self):
        self.preamble()
        while self.state != SessionState.STOPPED:
            self.execute(self.get_next_command())

    #
    # Retrieve from the list of tuple (opts),
    # the opt value that matchjes the given opt.
    #
    @staticmethod
    def retrieve_opt(optlist, given_opt):
        if optlist and given_opt:
            for i in optlist:
                if type(i) is tuple:
                    if i[0] == given_opt:
                        return given_opt, i[1]
        return None

    def execute(self, command):
        op_and_args = command.strip() if command else None
        if not op_and_args or op_and_args.startswith('#'):
            #
            # Comments are NOOP
            return
        op_and_args = op_and_args.split() if op_and_args else None
        if not op_and_args:
            return
        op, *args = op_and_args
        sargs = ' '.join(args) if args else None

        if op == 'login':
            self.execute_login(args)
            return
        if self.state == SessionState.STOPPED:
            return
        if op == 'dnac':
            self.execute_server()
            return
        if op == 'cd':
            self.execute_cd(sargs)
            return
        if op == 'info':
            self.execute_info()
            return
        if op_and_args[0] == 'pwd':
            self.execute_pwd()
            return
        if op_and_args[0] == 'date':
            self.execute_date()
            return
        if op_and_args[0] == 'export':
            export_config = self.parse_export_opts(sargs)
            if not export_config:
                self.usage('export')
                return
            mode, file = export_config
            if mode != 'map-archive':
                print('export: <bulk-ap> is not yet implemented')
                self.usage('export')
                return

            if not file:
                print('?? Must specify export file')
                self.usage('export')
                return

            self.execute_export_map(self.cwd[1], file)
            return
        if op_and_args[0] == 'ls':
            self.execute_ls()
            return
        if op_and_args[0] == 'exit' or op_and_args[0] == 'quit':
            sys.exit(0)
        self.usage(op)

    @staticmethod
    def handler(signal_received, frame):
        # User typed CTRL/C - clean up and quit gracefully
        print('  ')
        print('[^C detected: type "exit"/"quit" to exit]')
        return

    def export_usage(self):
        self.usage('export')

    def parse_export_opts(self, args):
        parser = argparse.ArgumentParser(usage=self.export_usage)
        mode_group = parser.add_mutually_exclusive_group(required=False)
        mode_group.add_argument('--map-archive',
                                default=False,
                                required=False,
                                dest='map_archive', action='store_true',
                                help='Export map archive')

        mode_group.add_argument('--bulk-ap',
                                default=False,
                                required=False,
                                dest='bulk_ap', action='store_true',
                                help='Export Access Points in bulk')

        parser.add_argument('--file',
                            type=str,
                            action="store",
                            required=False,
                            help='Target file to use for export')

        try:
            pargs = parser.parse_args(shlex.split(args))
            if pargs.map_archive:
                return 'map-archive', pargs.file
            if pargs.bulk_ap:
                return 'bulk-ap', pargs.file
        except:
            pass
        return None
