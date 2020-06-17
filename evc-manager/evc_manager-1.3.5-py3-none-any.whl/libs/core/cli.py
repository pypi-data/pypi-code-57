"""
    Module to manage the CLI params
"""


import sys
import os
import argparse
import getpass
from .read_file import read_file
from .singleton import Singleton
from .shortcut_file import shortcut_file
from .create_template_files import create_template_files


VERSION = "0.3"


def create_parser():
    """ Read CLI options """
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("-L", "--list-evc",
                         help="List all EVCs and output them using YAML",
                         action="store_true")
    actions.add_argument("-A", "--add-evc",
                         help="Add EVCs provided in the YAML file",
                         action="store_true")
    actions.add_argument("-R", "--add-range-evcs",
                         help="Add a range of EVCs provided in the YAML file",
                         action="store_true")
    actions.add_argument("-C", "--change-evc",
                         help="Change EVCs provided in the YAML file",
                         action="store_true")
    actions.add_argument("-D", "--delete-evc",
                         help="Delete all EVCs provided in the YAML file",
                         action="store_true")
    actions.add_argument("-M", "--move-evc",
                         help="Move one or all EVCs out the NNI provided.",
                         action="store_true")
    actions.add_argument("-X", "--template",
                         help="Create a template folder with YAML files to help.",
                         action="store_true")

    parser.add_argument("--move-from-nni",
                        help="Move out of the provided NNI")

    parser.add_argument("-f", "--source-file",
                        help="Source YAML file used by options -A or -D")
    parser.add_argument("-F", "--destination-file",
                        help="Destination YAML file used by options -L",
                        default="evcs_list.yaml")

    filters = parser.add_argument_group("filters")
    filters.add_argument("--has-uni-device",
                         help="Filter output based on the UNI's device")
    filters.add_argument("--has-uni-interface",
                         help="Filter output based on the UNI's interface")
    filters.add_argument("--has-uni-tag-value",
                         help="Filter output based on the UNI's tag value (VLAN ID)")

    filters.add_argument("--has-nni-name",
                         help="Filter output based on the NNI's name")
    filters.add_argument("--has-nni-name-primary",
                         help="Filter output when NNI's name is in primary path")
    filters.add_argument("--has-nni-name-backup",
                         help="Filter output when NNI's name is in backup path")

    group = parser.add_argument_group('authentication')
    group.add_argument("-u", "--user",
                       help="Backend user for authentication")
    group.add_argument("-t", "--tenant",
                       help="Backend user group for authentication")

    passwords = parser.add_mutually_exclusive_group()
    passwords.add_argument("-p", "--password",
                           help="Provide pass for authentication")
    passwords.add_argument("-P", "--prompt_password",
                           help="Prompt pass for authentication",
                           action='store_true')

    # backends = parser.add_mutually_exclusive_group(required=True)
    backends = parser.add_mutually_exclusive_group()
    backends.add_argument("-O", "--oess-url",
                          help="Use OESS backend. Provide OESS's URL")
    backends.add_argument("-K", "--kytos-url",
                          help="Use Kytos E-Line backend's URL.")

    parser.add_argument("-V", "--version", action="version",
                        version=VERSION)
    parser.add_argument("-v", "--verbose",
                        help="Set Verbose Level (info|warning|debug)",
                        default='info',
                        choices=["info", "warning", "debug"])
    parser.add_argument("-q", "--quiet",
                        help="Set Quiet Mode",
                        action="store_true")

    output = parser.add_mutually_exclusive_group()
    output.add_argument("-y", "--to-yaml",
                        help="Print using YAML.",
                        action="store_true")
    output.add_argument("-Y", "--to-yaml-minimal",
                        help="Print using YAML but only the smallest set of mandatory attrs.",
                        action="store_true")
    output.add_argument("-j", "--to-json",
                        help="Print using JSON.",
                        action="store_true")
    output.add_argument("-z", "--to_zabbix",
                        help="Converts output to Zabbix LLD format",
                        action="store_true")
    output.add_argument("-n", "--to-screen",
                        help="Print EVC's names to screen instead of to files",
                        action="store_true")

    parser.add_argument("-T", "--to_table",
                        help="Converts output to a table format. "
                             "Use Syntax: Primary|Backup|Any:Circuit_Name")
    parser.add_argument("-s", "--gen_stats_per_nni",
                        help="List number of EVCs per NNI"
                             "-s Any: list all NNIs"
                             " To filter use -s NNI[:JSON]")

    parser.add_argument("-S", "--shortcut-file",
                        help="Use a provided shortcut file. Default is .evc_manager")

    return parser


class CliOptions(metaclass=Singleton):
    """ Main CLI Class """

    def __init__(self, parser=None, args=None):
        self.action = None
        self.user = None
        self.password = None
        self.tenant = None
        self.is_oess = None
        self.is_kytos = None
        self.destination_file = "evcs_list.yaml"
        self.source_file = None
        self.file_content = None
        self.to_table = 'Any:None'
        self.gen_stats_per_nni = None

        self._backend_url = None
        self._output_format = None

        self._is_list = False
        self._is_add = False
        self._is_add_range = False
        self._is_delete = False
        self._is_change = False
        self._is_move = False
        self._move_from_nni = False
        self._quiet_mode = False
        self._verbose = None

        self.has_uni_filters = False
        self._has_uni_device = None
        self._has_uni_interface = None
        self._has_uni_tag_value = None

        self.has_nni_filters = False
        self._has_nni_name = None
        self._has_nni_name_primary = None
        self._has_nni_name_backup = None

        self.read_params(parser, args)

    def read_params(self, parser, args):
        """ Read CLI options """
        if not parser:
            parser = create_parser()
            args = parser.parse_args()
            args = shortcut_file(args)
        self.evaluate_input(parser, args)

    def evaluate_input(self, parser, args):
        """ Evaluate if the params provided are coherent """

        if args.template:
            create_template_files()

        if not args.user:
            parser.error('Missing user')

        if not args.password and not args.prompt_password:
            parser.error('Provide a password (-p or -P)')

        if not args.oess_url and not args.kytos_url:
            parser.error('Please provide a backend (-O or -K)')

        if args.add_evc and not args.source_file:
            parser.error('Missing Source File (option -f)')

        if args.add_range_evcs and not args.source_file:
            parser.error('Missing Source File (option -f)')

        if args.change_evc and not args.source_file:
            parser.error('Missing Source File (option -f)')

        if args.delete_evc and not args.source_file:
            parser.error('Missing Source File (option -f)')

        if args.move_evc and not args.source_file:
            parser.error('Missing Source File (option -f)')

        if args.move_evc and not args.move_from_nni:
            parser.error('Missing NNI name to move out (--move-from-nni)')

        if args.oess_url and not args.tenant:
            parser.error('Missing tenant (-t) param')

        if args.prompt_password:
            try:
                args.password = getpass.getpass()
                if not len(args.password):
                    raise ValueError
            except ValueError:
                parser.error('Password Not Provided.')
            except KeyboardInterrupt:
                print("")
                sys.exit(0)

        if args.has_uni_device and not args.list_evc:
            parser.error('--has-uni-device should be used with -L')

        if args.has_uni_interface and not args.list_evc:
            parser.error('--has-uni-interface should be used with -L')

        if args.has_uni_tag_value and not args.list_evc:
            parser.error('--has-uni-tag-value should be used with -L')

        if args.has_nni_name and not args.list_evc:
            parser.error('--has-nni-name should be used with -L')

        if args.has_nni_name_primary and not args.list_evc:
            parser.error('--has-nni-name-primary should be used with -L')

        if args.has_nni_name_backup and not args.list_evc:
            parser.error('--has-nni-name-backup should be used with -L')

        if args.has_nni_name:
            if args.has_nni_name_primary or args.has_nni_name_backup:
                msg = "if using --has-nni-name, don't use other NNI filter."
                parser.error(msg)

        self.assign_values(args)

    @property
    def verbose(self):
        """ Getter """
        return self._verbose

    @verbose.setter
    def verbose(self, verbose):
        """ Setter """
        self._verbose = verbose
        os.environ['EVC_MANAGER_QUIET_MODE'] = 'False'
        os.environ['EVC_MANAGER_VERBOSITY'] = self.verbose

    @property
    def quiet_mode(self):
        """ Getter """
        return self._quiet_mode

    @quiet_mode.setter
    def quiet_mode(self, quiet_mode):
        """ Setter """
        self._quiet_mode = quiet_mode
        if self.quiet_mode:
            os.environ['EVC_MANAGER_QUIET_MODE'] = 'True'
        else:
            os.environ['EVC_MANAGER_QUIET_MODE'] = 'False'

    @property
    def is_list(self):
        """ Getter """
        return self._is_list

    @is_list.setter
    def is_list(self, is_list):
        """ Setter """
        if is_list:
            self._is_list = True

    @property
    def is_add(self):
        """ Getter """
        return self._is_add

    @is_add.setter
    def is_add(self, is_add):
        """ Setter """
        if is_add:
            self._is_add = True
            self.read_file_content('add')

    @property
    def is_add_range(self):
        """ Getter """
        return self._is_add_range

    @is_add_range.setter
    def is_add_range(self, is_add_range):
        """ Setter """
        if is_add_range:
            self._is_add_range = True
            self.read_file_content('add_range')

    @property
    def is_change(self):
        """ Getter """
        return self._is_change

    @is_change.setter
    def is_change(self, is_change):
        """ Setter """
        if is_change:
            self._is_change = True
            self.read_file_content('change')

    @property
    def is_delete(self):
        """ Getter """
        return self._is_delete

    @is_delete.setter
    def is_delete(self, is_delete):
        """ Setter """
        if is_delete:
            self._is_delete = True
            self.read_file_content('delete')

    @property
    def is_move(self):
        """ Getter """
        return self._is_move

    @is_move.setter
    def is_move(self, is_move):
        """ Setter """
        if is_move:
            self._is_move = True
            self.read_file_content('move')

    @property
    def move_from_nni(self):
        """ Getter """
        return self._move_from_nni

    @move_from_nni.setter
    def move_from_nni(self, nni_name):
        """ Setter """
        if isinstance(nni_name, str):
            self._move_from_nni = nni_name

    @property
    def backend_url(self):
        """ Getter """
        return self._backend_url

    @backend_url.setter
    def backend_url(self, args):
        """ Setter """
        if args.oess_url:
            self._backend_url = args.oess_url
            self.is_oess = True
        elif args.kytos_url:
            self._backend_url = args.kytos_url
            self.is_kytos = True

    @property
    def output_format(self):
        """ Getter """
        return self._output_format

    @output_format.setter
    def output_format(self, args):
        """ Setter """
        if args.to_json:
            self._output_format = 'json'
        elif args.to_zabbix:
            self._output_format = 'zabbix'
        elif args.to_table:
            self._output_format = 'table'
            self.to_table = args.to_table
        elif args.gen_stats_per_nni:
            self._output_format = 'stats'
            self.gen_stats_per_nni = args.gen_stats_per_nni
        elif args.to_yaml_minimal:
            self._output_format = 'yaml_minimal'
        elif args.to_screen:
            self._output_format = 'screen'
        else:
            self._output_format = 'yaml'

    @property
    def has_uni_device(self):
        """ Getter """
        return self._has_uni_device

    @has_uni_device.setter
    def has_uni_device(self, device):
        """ Setter """
        if isinstance(device, str):
            self._has_uni_device = device
            self.has_uni_filters = True

    @property
    def has_uni_interface(self):
        """ Getter """
        return self._has_uni_interface

    @has_uni_interface.setter
    def has_uni_interface(self, interface):
        """ Setter """
        if isinstance(interface, str):
            self._has_uni_interface = interface.split(":")[0]
            self.has_uni_filters = True

    @property
    def has_uni_tag_value(self):
        """ Getter """
        return self._has_uni_tag_value

    @has_uni_tag_value.setter
    def has_uni_tag_value(self, tag_value):
        """ Setter """
        if isinstance(tag_value, str):
            self._has_uni_tag_value = int(tag_value)
            self.has_uni_filters = True

    @property
    def has_nni_name(self):
        """ Getter """
        return self._has_nni_name

    @has_nni_name.setter
    def has_nni_name(self, nni_name):
        """ Setter """
        if isinstance(nni_name, str) and len(nni_name) > 1:
            self._has_nni_name = nni_name
            self.has_nni_filters = True

    @property
    def has_nni_name_primary(self):
        """ Getter """
        return self._has_nni_name_primary

    @has_nni_name_primary.setter
    def has_nni_name_primary(self, nni_name):
        """ Setter """
        if isinstance(nni_name, str) and len(nni_name) > 1:
            self._has_nni_name_primary = nni_name
            self.has_nni_filters = True

    @property
    def has_nni_name_backup(self):
        """ Getter """
        return self._has_nni_name_backup

    @has_nni_name_backup.setter
    def has_nni_name_backup(self, nni_name):
        """ Setter """
        if isinstance(nni_name, str) and len(nni_name) > 1:
            self._has_nni_name_backup = nni_name
            self.has_nni_filters = True

    def assign_values(self, args):
        """ Assign values to attributes using CLI params """

        self.user = args.user
        self.password = args.password

        if args.tenant:
            self.tenant = args.tenant

        self.destination_file = args.destination_file
        self.source_file = args.source_file

        self.verbose = args.verbose
        self.quiet_mode = args.quiet

        self.is_list = args.list_evc
        self.is_add = args.add_evc
        self.is_add_range = args.add_range_evcs
        self.is_change = args.change_evc
        self.is_delete = args.delete_evc
        self.is_move = args.move_evc

        self.move_from_nni = args.move_from_nni

        self.backend_url = args
        self.output_format = args

        self.has_uni_device = args.has_uni_device
        self.has_uni_interface = args.has_uni_interface
        self.has_uni_tag_value = args.has_uni_tag_value

        self.has_nni_name = args.has_nni_name
        self.has_nni_name_primary = args.has_nni_name_primary
        self.has_nni_name_backup = args.has_nni_name_backup

    def read_file_content(self, action):
        """ Read file content in case it is add or delete """
        file_content = read_file(source_file=self.source_file)
        if action == file_content['action']:
            self.file_content = file_content['evcs']
        else:
            msg = "File %s has an incoherent action (%s)"
            msg += "with CLI option provided. Exiting now."
            raise ValueError(msg % (self.source_file, action))
