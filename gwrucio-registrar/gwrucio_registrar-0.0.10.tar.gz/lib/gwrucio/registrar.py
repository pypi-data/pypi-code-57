# Copyright (C) 2020  James Alexander Clark <james.clark@ligo.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
registrar is a utility for registering IGWN files already on storage
"""

# pylint: disable=import-error,superfluous-parens
# NOTE: we need to pass explicit PFNs for registration, non-deterministically,
# in case the LFN2PFN algorithm relies on metadata which does not yet exist
# TODO: set up lfn2pfn for SFTs
# TODO: Make registrar run continuously / compare minimum-gps with most recent file
# TODO: Mode of running to just update metadata
#       - Find all files in a desired dataset (does not require diskcache_dump)
#       - Create ReplicaRegister from those files
#       - Call add_metadata()
#       - Trick is to figure out how to implement this without code duplication

import logging
import re
import sys
import os
import time
import threading
import traceback
from configparser import NoOptionError

import gwrucio.utils

from rucio.client.client import Client
import rucio.rse.rsemanager as rsemgr
from rucio.common.config import config_get
from rucio.common.exception import (DataIdentifierAlreadyExists,
                                    RSEBlacklisted, FileAlreadyExists)

# Frame/sft names follow https://dcc.ligo.org/T970130:
_IGWN_RE = \
    re.compile(r'([A-Z]+)-([A-Za-z0-9_]+)-([0-9]+)-([0-9]+).([A-Za-z]+)')
# Impose constraint on dataset names:
_DATASET_RE = re.compile(r'([A-Za-z0-9_]+)')

logging.basicConfig(
    stream=sys.stdout,
    level=getattr(
        logging,
        config_get('common',
                   'loglevel',
                   raise_exception=False,
                   default='DEBUG').upper()),
    format='%(asctime)s\t%(process)d\t%(levelname)s\t%(message)s')

GRACEFUL_STOP = threading.Event()


def stop():
    """
    Graceful exit
    """
    GRACEFUL_STOP.set()


class ReplicaSet:
    """
    List of DIDs and their attributes to be registered
    """

    def __init__(self, pathlist, scope, rse, common_metadata=None):
        """
        Constructor for the ReplicaSet class

        :param scope: Scope for replicas
        :type scope: str
        :param pathlist: list of file paths to register
        :type pathlist: list of strings
        :param rse: RSE to register replicas at
        :type rse: str
        :param metadata: common metadata to attach to each DID
        :type metadata: dict
        """

        self.scope = scope
        self.rse = rse

        self.__pathlist = pathlist
        self.__common_metadata = common_metadata
        self._replicas = self.replica_list()

    @property
    def replicas(self):
        """
        Return the replica list
        """
        return self._replicas

    @property
    def scope(self):
        """Return Scope replicas registered at"""
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Set scope for registration"""
        client = Client()
        if scope not in (vscope for vscope in client.list_scopes()):
            raise ValueError("Scope %s does not exist" % scope)
        self._scope = scope

    @property
    def rse(self):
        """Return RSE replicas registered at"""
        return self._rse

    @rse.setter
    def rse(self, rse):
        """Set RSE for registration"""
        client = Client()
        if rse not in [vrse['rse'] for vrse in client.list_rses()]:
            raise ValueError("RSE %s does not exist" % rse)
        self._rse = rse

    @property
    def size(self):
        """Get size of dataset"""
        return len(self._replicas)

    def replica_list(self):
        """
        Create a list of dictionaries of DID metadata

        :param pathlist: List of file paths
        :type pathlist: list of strings
        :param metadata: Dataset metadata configuration
        :type metadata: ConfigParser
        :returns: list of dictionaries with metadata
        """

        def _meta_dict(path):
            """
            Parse pfn name and add metadata
            """
            if self.__common_metadata:
                metadata = dict(self.__common_metadata)
            else:
                metadata = dict()

            # Parse LFN
            lfn = os.path.basename(path)
            metadata['obs'], metadata['datatype'], gps_start_time, \
                duration, metadata['extension'] = \
                _IGWN_RE.match(lfn).groups()

            metadata['gps-end-time'] = str(int(gps_start_time) + int(duration))
            metadata['gps-start-time'] = gps_start_time
            metadata['duration'] = duration

            return metadata

        replica_meta_list = map(_meta_dict, self.__pathlist)

        # Get RSE info to determin URI
        rse_info = rsemgr.get_rse_info(self.rse)

        # DIDs will be a list of dictionaries, each of which includes a
        # dictionary of IGWN metadata.  Note that the metadata must be added
        # separately to each did.
        return [{
            'scope': self.scope,
            'name': os.path.basename(path),
            'pfn': gwrucio.utils.get_pfn(rse_info, path),
            'meta': replica_meta,
        } for path, replica_meta in zip(self.__pathlist, replica_meta_list)]

    def reduce_replicas(self, logstr):
        """
        Reduce the DID list to unregistered DIDs
        """
        client = Client()
        replicas = [{
            'scope': self.scope,
            'name': replica['name']
        } for replica in self._replicas]

        logging.info("%s Checking for existing replicas", logstr)

        # Split into groups to avoid overloading database
        replica_groups = gwrucio.utils.grouper(replicas,
                                               int(len(replicas) / 100))

        total = 0
        found_replicas = list()
        for replica_group in replica_groups:
            logging.debug("%s Checking %d-%d of %d DIDs", logstr, total + 1,
                          len(replica_group) + total, len(replicas))
            total += len(replica_group)
            found_replicas = [
                replica['name']
                for replica in client.list_replicas(replica_group)
            ]
            logging.debug("%s Found %d existing replicas", logstr,
                          len(found_replicas))

            # Remove existing replicas
            self._replicas = [
                replica for replica in self._replicas
                if replica['name'] not in found_replicas
            ]
            logging.debug("%s %d replicas remain in list", logstr,
                          len(self._replicas))


class ReplicaRegister(ReplicaSet):
    """
    Register a set of replicas
    """

    def __init__(self, *args, dataset=None):
        """
        Constructor for the ReplicaRegister class: extends the ReplicaSet to
        add registration methods
        """
        super(ReplicaRegister, self).__init__(*args)
        self._client = Client()
        if dataset:
            self.dataset = dataset
        self.__metadata = False

    @property
    def dataset(self):
        """Return datase replicas registered in"""
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """
        Sets the dataset files will be attached to.

        Name must be underscore-separated alpha-numeric characters

        Checks dataset exists and creates it if not.  A rule is added at this
        RSE if write-access is allowed.
        """
        matched = re.match(_DATASET_RE, dataset)
        if not bool(matched):
            raise ValueError("Dataset name %s does not follow %s" %
                             (dataset, _DATASET_RE))

        # Check dataset exists and create it if not
        # - Adds a rule if the RSE allows it
        logging.info("Adding dataset %s", dataset)
        try:
            self._client.add_dataset(scope=self.scope,
                                     name=dataset,
                                     rules=[{
                                         'account': self._client.account,
                                         'copies': 1,
                                         'rse_expression': self.rse,
                                         'grouping': 'DATASET',
                                         'lifetime': None
                                     }])
        except RSEBlacklisted:
            logging.info(
                'RSE write blacklisted on %s, not adding rule for dataset %s',
                self.rse, dataset)
            self._client.add_dataset(scope=self.scope, name=dataset)
        except DataIdentifierAlreadyExists:
            logging.info("Dataset %s already exists", dataset)

        # Set value of dataset
        self._dataset = dataset

    def add_replicas(self, logstr):
        """
        Add the replicas to the rucio database
        """
        logging.info('%s Adding replicas', logstr)

        def compute_metadata(replica):
            """Retrieve metadata for an individual replica"""
            replica['bytes'] = gwrucio.utils.gfal_bytes(replica['pfn'])
            replica['adler32'] = gwrucio.utils.gfal_adler32(replica['pfn'])
            replica['md5'] = gwrucio.utils.gfal_md5(replica['pfn'])
            return replica

        for rdx, replica in enumerate(self.replicas):
            logging.debug("%s Working on file %i/%i (%s)", logstr, rdx + 1,
                          self.size, replica['pfn'])
            compute_metadata(replica)

        self._client.add_replicas(rse=self.rse,
                                  files=self.replicas,
                                  ignore_availability=True)

        # Attach to dataset
        logging.info('%s Attaching replicas to %s', logstr, self.dataset)
        dids = [{
            'scope': self.scope,
            'name': replica['name']
        } for replica in self.replicas]
        for did in dids:
            try:
                self._client.attach_dids(scope=self.scope,
                                         name=self.dataset,
                                         dids=[did])
            except FileAlreadyExists:
                logging.debug('%s already attached', did['name'])
        logging.debug('%s Replicas attached', logstr)

    def add_did_meta(self, logstr):
        """
        Add generic did metadata for queries
        """
        logging.debug("%s Adding DID metadata", logstr)

        _ = [
            self._client.add_did_meta(scope=self.scope,
                                      name=replica['name'],
                                      meta=replica['meta'])
            for replica in self.replicas
        ]


def registrar(didset=None,
              thread_info=None,
              add_files=True,
              reduce_replicas=False):
    """
    Register a dataset
    """
    try:
        prepend_str = 'Thread [%i/%i] :' % thread_info
        logging.info("%s Getting metadata for %d files", prepend_str,
                     didset.size)
        # Reduce list to unregistered files
        if reduce_replicas:
            didset.reduce_replicas(prepend_str)
        if add_files:
            didset.add_replicas(prepend_str)
        didset.add_did_meta(prepend_str)
    # pylint: disable=broad-except
    except Exception:
        logging.critical('%s %s', prepend_str, str(traceback.format_exc()))


def run(diskcache_dump, config, rse, reduce_replicas=False, threads=1):
    """
    Principal operations

    1. Identify input files
    2. Parse file metadata and create collections of DIDs
    3. Compute file metadata and register for each set of DIDs

    """

    # Start timer
    global_start_time = time.time()

    try:
        extension = config.get('data', 'extension')
    except NoOptionError:
        extension = 'gwf'

    # Get files to register
    filepaths = gwrucio.utils.read_disk_cache(diskcache_dump, config)
    logging.info("Found %d matching files", len(filepaths))

    # Parse configuration
    try:
        dataset = config.get('global', 'dataset')
    except NoOptionError:
        dataset = None

    try:
        did_metadata = dict(config['common-metadata'])
    except NoOptionError:
        logging.warning('No common metadata will be applied to these DIDs')
        did_metadata = dict()

    # Ensure we only have useful threads
    if threads > len(filepaths):
        threads = len(filepaths)

    # Generate replica sets for each thread
    didsets = (ReplicaRegister(filegroup,
                               config.get('global', 'scope'),
                               rse,
                               did_metadata,
                               dataset=dataset)
               for filegroup in gwrucio.utils.grouper(filepaths, threads))

    # Initialise threads
    threads = [
        threading.Thread(target=registrar,
                         kwargs={
                             'didset': didset,
                             'thread_info': (idx + 1, threads),
                             'reduce_replicas': reduce_replicas
                         }) for idx, didset in enumerate(didsets)
    ]

    # Start threads
    _ = [thread.start() for thread in threads]
    logging.info('waiting for interrupts')

    # Wait for interrupts
    while threads:
        threads = [
            thread.join(timeout=3.14) for thread in threads
            if thread and thread.isAlive()
        ]

    # Stop timer
    logging.info("total uptime: %-0.4f sec.",
                 (time.time() - global_start_time))
