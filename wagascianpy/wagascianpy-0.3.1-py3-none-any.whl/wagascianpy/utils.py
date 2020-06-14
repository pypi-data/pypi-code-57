#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

import collections
import errno
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict

import ROOT
import paramiko
from scp import SCPClient
from six import string_types

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

import wagascianpy.environment

_DETECTORS = {'wallmrd_top_north': {"1": {"1": {"1-3": 32}}},
              'wallmrd_bottom_north': {"1": {"2": {"1-3": 32}}},
              'wallmrd_top_south': {"1": {"3": {"1-3": 32}}},
              'wallmrd_bottom_south': {"1": {"4": {"1-3": 32}}},
              'wagasci_top_upstream': {"2": {"1": {"1-20": 32}}},
              'wagasci_side_upstream': {"2": {"2": {"1-20": 32}}},
              'wagasci_top_downstream': {"2": {"3": {"1-20": 32}}},
              'wagasci_side_downstream': {"2": {"4": {"1-20": 32}}},
              'wallmrd_north': {"1": {"1": {"1-3": 32}, "2": {"1-3": 32}}},
              'wallmrd_south': {"1": {"3": {"1-3": 32}, "4": {"1-3": 32}}},
              'wagasci_upstream': {"2": {"1": {"1-20": 32}, "2": {"1-20": 32}}},
              'wagasci_downstream': {"2": {"3": {"1-20": 32}, "4": {"1-20": 32}}}}
_FULL_SETUP = "wallmrd_north|wallmrd_south|wagasci_upstream|wagasci_downstream"
_MAX_NCHIPS = 20
_DEFAULT_TIMEZONE = "Asia/Tokyo"


###############################################################################
#                                 copytree                                    #
###############################################################################

def copytree(src, dst, dif_topology=None, symlinks=False, ignore=None):
    """Copy run_root_dir folder into dst folder (it does not create the dst folder
    if it does not exist)

    """
    if os.path.exists(src) and os.path.isdir(src):
        if not os.listdir(src):
            raise ValueError('Directory "%s" is empty' % src)
    else:
        raise ValueError('Directory "%s" doesn\'t exist' % src)

    dif_list = []
    dif_counter = 0
    if dif_topology is not None:
        dif_list = sorted(list(dif_topology.keys()))
    for item in sorted(os.listdir(src)):
        source_file = os.path.join(src, item)
        destination_file = os.path.join(dst, item)
        if os.path.isdir(source_file):
            shutil.copytree(source_file, destination_file, symlinks, ignore)
        else:
            if dif_topology is not None and "ecal_dif" in source_file:
                destination_file = re.sub(r"_ecal_dif_[0-9]+.raw",
                                          "_ecal_dif_%s.raw" % (str(dif_list[dif_counter])),
                                          destination_file)
                dif_counter += 1
            shutil.copy2(source_file, destination_file)


###############################################################################
#                               renametree                                    #
###############################################################################

def renametree(run_root_dir, run_name, dif_topology):
    """Rename runs in folder according to topology

    """
    if not isinstance(dif_topology, dict):
        raise ValueError("DIF topology must be a dictionary!")

    if os.path.exists(run_root_dir) and os.path.isdir(run_root_dir):
        if not os.listdir(run_root_dir):
            raise ValueError('Directory "%s" is empty' % run_root_dir)
    else:
        raise ValueError('Directory "%s" doesn\'t exist' % run_root_dir)
    topology_dif_list = sorted(list(dif_topology.keys()))
    file_dif_list = []
    for file_name in sorted(wagascianpy.utils.find_files_with_ext(path=run_root_dir, extension='raw')):
        if "ecal_dif" in file_name:
            match = re.search(r"_ecal_dif_([0-9]+).raw", file_name)
            if match is not None:
                file_dif_list.append(match.group(1))
    if collections.Counter(topology_dif_list) == collections.Counter(file_dif_list):
        return
    if len(file_dif_list) != len(topology_dif_list):
        raise ValueError("Number of raw files ({}) is different from topology ({})".format(len(file_dif_list),
                                                                                           len(topology_dif_list)))
    dictionary = dict(zip(sorted(file_dif_list), sorted(topology_dif_list)))
    for file_dif_id, topology_dif_id in dictionary.items():
        old_file_name = "{}_ecal_dif_{}.raw".format(run_name, file_dif_id)
        tmp_file_name = "{}_ecal_dif_{}.raw.tmp".format(run_name, topology_dif_id)
        os.rename(os.path.join(run_root_dir, old_file_name), os.path.join(run_root_dir, tmp_file_name))
    for tmp_file_name in sorted(wagascianpy.utils.find_files_with_ext(path=run_root_dir, extension='tmp')):
        new_file_name = tmp_file_name.replace('.tmp', '')
        os.rename(os.path.join(run_root_dir, tmp_file_name), os.path.join(run_root_dir, new_file_name))


###############################################################################
#                              static_vars                                    #
###############################################################################

def static_vars(**kwargs):
    """Static variables inside function for Python"""

    def decorate(func):
        """Decorator for static_vars"""
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate


###############################################################################
#                                  mkdir_p                                    #
###############################################################################

def mkdir_p(path):
    """Create a directory recursively. If the directory already exists, do
    nothing

    """
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


###############################################################################
#                                 join_threads                                #
###############################################################################

def join_threads(threads):
    """ Join all the threads in the list *threads*"""
    for thread in threads:
        result = thread.join()
        if result not in [0, -1]:
            print("Error number : %s" % result)
            exit(result)


###############################################################################
#                                limit_threads                                #
###############################################################################

def limit_threads(threads, max_threads):
    """Limit the number of simultaneuously running threads"""
    while len(threads) > max_threads:
        result = threads[0].join()
        if result not in [0, -1]:
            print("Error number : %s" % result)
            exit(result)
        threads.pop(0)


###############################################################################
#                                 join_chains                                 #
###############################################################################

def join_chains(chains_for_each_run):
    """ Join all the threads in the list *threads*"""
    for run_name, chain_for_each_dif in chains_for_each_run.items():
        for dif_id, chain in chain_for_each_dif.items():
            print("JOIN DIF {} : LINK ID {} : THREAD ID {}".format(dif_id, id(chain.link), id(chain.thread)))
            result = chain.thread.join()
            if result not in [0, -1]:
                raise RuntimeError("RUN {} DIF {} : Error code {}".format(run_name, dif_id, result))


###############################################################################
#                                limit_chains                                #
###############################################################################

def limit_chains(chains_for_each_run, max_threads):
    """Limit the number of simultaneuously running threads"""
    num_threads = 0
    for chain_for_each_dif in chains_for_each_run.values():
        for chain in chain_for_each_dif.values():
            if chain.thread.is_alive():
                num_threads += 1
    for run_name, chain_for_each_dif in sorted(chains_for_each_run.items()):
        for dif_id, chain in sorted(chain_for_each_dif.items()):
            if num_threads <= max_threads:
                return
            if chain.thread.is_alive():
                result = chain.thread.join()
                num_threads -= 1
                if result not in [0, -1]:
                    raise RuntimeError("RUN {} DIF {} : Error code {}".format(run_name, dif_id, result))


###############################################################################
#                read GDCC to DIF topology mapping file                       #
###############################################################################

def read_dif_mapping(mapping_file):
    """ Read the *mapping_file* containing the DIF/GDCC mapping

    # Assuming the following DIF - GDCC mapping as default:
    #
    # GDCC 1 port   -   DIF ID
    # 1                 0
    # 2                 1
    # 3                 2
    # 4                 3
    # GDCC 2 port   -   DIF ID
    # 1                 4
    # 2                 5
    # 3                 6
    # 4                 7
    """
    try:
        with open(mapping_file) as json_file:
            dif_mapping = json.load(json_file)
    except (IOError, ValueError) as exception:
        print('"%s" mapping not found or invalid. Using default mapping : %s'
              % (mapping_file, str(exception)))
        dif_mapping = json.loads(
            '{"1":{"1":0,"2":1,"3":2,"4":3,"5":8,"6":9,"7":10}'
            ',"2":{"1":4,"2":5,"3":6,"4":7,"5":11,"6":12,"7":13}}')
    return dif_mapping


###############################################################################
#                  read GDCC MAC addresses mapping file                       #
###############################################################################

def read_mac_mapping(mapping_file):
    """ Read the *mapping_file* containing the GDCC to MAC address mapping

    # Assuming the following GDCC MAC mapping as default:
    #
    # GDCC 1
    # 00:0A:35:01:FE:06
    # GDCC 2
    # 00:0A:35:01:FE:01
    """
    try:
        with open(mapping_file) as json_file:
            mac_mapping_inv = json.load(json_file)
            mac_mapping = {value: key for key, value in
                           mac_mapping_inv.items()}
    except (IOError, ValueError) as exception:
        print('"%s" mapping file not found or invalid. '
              'Using default mapping : %s' % (mapping_file, str(exception)))
        mac_mapping = {"1": "00:0A:35:01:FE:06", "2": "00:0A:35:01:FE:01"}
    return mac_mapping


###############################################################################
#                            parse_topology_string                            #
###############################################################################

def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for key in merge_dct:
        if (key in dct and isinstance(dct[key], dict)
                and isinstance(merge_dct[key], Mapping)):
            dict_merge(dct[key], merge_dct[key])
        else:
            dct[key] = merge_dct[key]


###############################################################################
#                                 get_net_if                                  #
###############################################################################

def get_net_if():
    """Return the name of the network interface connected to the
    192.168.10.0/24 LAN"""
    gdcc_pc_dev = None
    get_dev_command = "ip -o addr show"
    process = subprocess.Popen(get_dev_command.split(), stdout=subprocess.PIPE)
    ps_output, error = process.communicate()
    if error:
        raise ValueError("Error when looking for network interface : %s" % error)
    for line in ps_output.strip().decode().splitlines():
        if re.search("192.168.10", line):
            fields = line.strip().split()
            gdcc_pc_dev = fields[1]
            break
    if gdcc_pc_dev is None:
        print("could not find a network interface connected "
              "to the 192.168.10.0 LAN")
        gdcc_pc_dev = "eth0"
    return gdcc_pc_dev


###############################################################################
#                            list_dir_with_integer                            #
###############################################################################

def list_dir_with_integer(path):
    """List all directories containing an integer.

    Args:
        path: path to a directories containing other directories

    Return:
        list of tuples named 'dir_with_integer'. Each tuple contains
        two elements:
            - num eger
            - num_dir : directory name

    """
    if not os.path.exists(path) or not os.path.isdir(path):
        raise ValueError("Directory does not exists : %s" % path)
    dir_list = os.listdir(path)
    if not dir_list:
        raise ValueError("Empty directory : %s" % path)
    nums_re = re.compile(r"\d+")
    dir_with_integer = collections.namedtuple('dir_with_integer', 'num num_dir')
    result = []
    for directory in dir_list:
        if bool(nums_re.search(directory)):
            result.append(dir_with_integer(nums_re.search(directory).group(0),
                                           directory))
    return sorted(result)


###############################################################################
#                              find_first_match                               #
###############################################################################

def find_first_match(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


###############################################################################
#                              find_files_with_ext                            #
###############################################################################

def find_files_with_ext(path, extension):
    file_list = []
    for root, _, files in os.walk(path):
        for file_name in files:
            if file_name.lower().endswith('.%s' % extension.strip('.')):
                file_list.append(os.path.join(root, file_name))
    return file_list


###############################################################################
#                                extract_dif_id                               #
###############################################################################


def extract_dif_id(path):
    file_name = os.path.basename(path)
    try:
        dif_id = int(re.search(r'_ecal_dif_([\d]+)', file_name).group(1))
    except (IndexError, AttributeError):
        dif_id = None
    return dif_id


###############################################################################
#                            extract_raw_tree_name                            #
###############################################################################

def extract_raw_tree_name(tfile):
    if isinstance(tfile, string_types):
        tfile = ROOT.TFile(tfile)
    if tfile.GetListOfKeys().Contains("raw"):
        return "raw"
    else:
        tree_name = "tree_dif_%s" % extract_dif_id(tfile.GetName())
        if tfile.GetListOfKeys().Contains(tree_name):
            return tree_name
        else:
            raise AttributeError("TTree not found in TFile %s" % tfile.GetName())


###############################################################################
#                            parse_topology_string                            #
###############################################################################

def parse_topology_string(topology_string):
    """parse topology string containing detector names"""
    if topology_string == "full_setup":
        topology_string = _FULL_SETUP
    have_detector_labels = False
    topology_new = {}
    for detector, detector_topology in _DETECTORS.items():
        if detector in topology_string:
            have_detector_labels = True
            dict_merge(topology_new, detector_topology)
    if have_detector_labels:
        topology_old = topology_new.copy()
        topology_new.clear()
    else:
        topology_old = json.loads(topology_string)
        topology_new.clear()
    for gdcc, dif_map in topology_old.items():
        topology_new[gdcc] = {}
        for dif, asu_map_old in dif_map.items():
            asu_key = next(iter(asu_map_old))
            asu_map_new = {}
            if "-" in asu_key:
                asu_list = asu_key.split("-")
                if len(asu_list) != 2:
                    raise ValueError("chip range is invalid : %s" % asu_key)
                n_channels = asu_map_old[asu_key]
                try:
                    first_asu = int(asu_list[0])
                    last_asu = int(asu_list[1])
                except ValueError:
                    raise ValueError("chip range is invalid : %s" % asu_key)
                if first_asu == last_asu or first_asu != 1 or \
                        first_asu is None or last_asu is None or \
                        last_asu - first_asu >= _MAX_NCHIPS:
                    raise ValueError("chip range is invalid : %s" % asu_key)
                for asu in range(first_asu, last_asu + 1, 1):
                    asu_map_new[str(asu)] = n_channels
            else:
                asu_map_new = asu_map_old
            topology_new[gdcc][dif] = asu_map_new
    return json.dumps(topology_new)


###############################################################################
#                            change_directory (Cd)                            #
###############################################################################

class Cd(object):
    """Context manager for changing the current working directory"""

    def __init__(self, new_path):
        self.saved_path = None
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


###############################################################################
#                                    which                                    #
###############################################################################

def which(program):
    """ python implementation of the which bash command"""

    def _is_exe(file_path):
        """Check if file is executable or not"""
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if _is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if _is_exe(exe_file):
                return exe_file
    return None


###############################################################################
#                              run_borg_cmd                                   #
###############################################################################

def run_borg_cmd(cmdlist, check_progress=False):
    """ Run a borg command"""

    # Uncomment to debug borg
    # print(cmdlist)

    try:
        environment = dict(os.environ)
        environment["BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK"] = "yes"
        if check_progress:
            return subprocess.Popen(cmdlist,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    env=environment)
        else:
            stdout = subprocess.check_output(cmdlist,
                                             shell=True,
                                             stderr=subprocess.STDOUT,
                                             env=environment)

    except subprocess.CalledProcessError as exception:
        if exception.output:
            print(exception.output)
            for line in exception.output.splitlines():
                json_out = json.loads(line)
                if json_out['levelname'] in [u'WARNING', u'ERROR', u'CRITICAL']:
                    raise RuntimeError(json_out['message'])
        raise RuntimeError("failed to execute command %s" % (str(cmdlist)))

    return str(stdout.decode())


###############################################################################
#                             create_ssh_client                               #
###############################################################################

def _create_ssh_client(hostname):
    client = paramiko.SSHClient()
    paramiko.transport.banner_timeout = 300

    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh_config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as filename:
            ssh_config.parse(filename)
    else:
        print("SSH configuration file not found at %s" % user_config_file)

    cfg = {'hostname': hostname}

    user_config = ssh_config.lookup(cfg['hostname'])
    for ssh_cfg_name, paramiko_cfg_name in {'hostname': 'hostname',
                                            'user': 'username',
                                            'port': 'port'}.items():
        if ssh_cfg_name in user_config:
            cfg[paramiko_cfg_name] = user_config[ssh_cfg_name]

    if 'proxycommand' in user_config:
        cfg['sock'] = paramiko.ProxyCommand(user_config['proxycommand'])

    if 'identityfile' in user_config:
        cfg['key_filename'] = os.path.expanduser(user_config['identityfile'][0])
        if not os.path.exists(cfg['key_filename']):
            raise Exception("Specified IdentityFile " + cfg['key_filename'] + " for " +
                            hostname + " in ~/.ssh/config not existing anymore.")
    print("SSH configuration : %s" % cfg)
    client.connect(**cfg)
    return client


###############################################################################
#                                   scp_put                                   #
###############################################################################

def scp_put(hostname, src_path, dst_path):
    """ Copy from local to remote using SCP """
    ssh = _create_ssh_client(hostname)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(src_path, dst_path)


###############################################################################
#                                   scp_get                                   #
###############################################################################

def scp_get(hostname, src_path, dst_path):
    """ Copy from remote to local using SCP """
    ssh = _create_ssh_client(hostname)
    src_filename = os.path.basename(src_path)
    dst_filename = os.path.basename(dst_path)
    dst_dirname = os.path.dirname(dst_path)
    with Cd(dst_dirname):
        with SCPClient(ssh.get_transport()) as scpclient:
            scpclient.get(src_path)
        print("Renaming %s into %s" % (os.path.join(dst_dirname, src_filename),
                                       os.path.join(dst_dirname, dst_filename)))
        os.rename(os.path.join(dst_dirname, src_filename),
                  os.path.join(dst_dirname, dst_filename))
    if not os.path.exists(dst_path):
        raise Exception("Failed to scp from %s:%s to %s" % (hostname, src_path, dst_path))


###############################################################################
#                                 silentremove                                #
###############################################################################

def silentremove(filename):
    """Remove file quietly"""
    try:
        os.remove(filename)
    except (OSError, IOError) as error:
        if error.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


###############################################################################
#                             silentremovedirs                                #
###############################################################################

def silentremovedirs(dirname):
    """Remove directory quietly"""
    shutil.rmtree(dirname, ignore_errors=True)


###############################################################################
#                          acqconfigxml_file_finder                           #
###############################################################################

def acqconfigxml_file_finder(run_root_dir, run_name):
    env = wagascianpy.environment.WagasciEnvironment()
    env["WAGASCI_LIB"] = env['WAGASCI_MAINDIR'] + "/lib"
    path1 = os.path.join(run_root_dir, run_name + ".xml")
    path2 = os.path.join(run_root_dir, os.path.basename(env['WAGASCI_ACQCONFIGDIR']),
                         env['WAGASCI_ACQCONFIGXML'])
    path3 = os.path.join(run_root_dir, env['WAGASCI_ACQCONFIGXML'])
    if os.path.exists(path1):
        acqconfigxml = path1
    elif os.path.exists(path2):
        acqconfigxml = path2
    elif os.path.exists(path3):
        acqconfigxml = path3
    else:
        raise EnvironmentError("XML acquisition configuration file not found")
    return acqconfigxml


###############################################################################
#                                   sha256sum                                 #
###############################################################################

# Python program to find SHA256 hexadecimal hash string of a file
def sha256sum(filename):
    with open(filename, "rb") as f:
        filebyte = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(filebyte).hexdigest()
        return readable_hash


###############################################################################
#                                  utf8_decorator                             #
###############################################################################

def utf8_decorator(func):
    """ decorator for encoding utf8 on all unicode arguments """

    def wrapper(*args, **kwargs):
        """ function wrapper """
        new_args = (x.encode('utf-8') if isinstance(x, string_types) else x for x in args)
        new_kwargs = {k: v.encode('utf-8') if isinstance(v, string_types) else v for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)

    return wrapper


###############################################################################
#                                  Get arguments                              #
###############################################################################

def get_arguments_ordered_dict(function):
    if sys.version_info.major >= 3:
        args = OrderedDict([(key, None) for key in inspect.getfullargspec(function).args[1:]])
    else:
        # noinspection PyDeprecation
        args = OrderedDict([(key, None) for key in inspect.getargspec(function).args[1:]])
    return args
