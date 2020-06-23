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
"""Utilities for data registration.
"""

# Native
import os
import errno
import sys
import logging
from time import sleep
from configparser import NoOptionError
import gfal2

from ldr.diskcache import DiskCacheFile
# from rucio.rse.protocols.protocol import RSEDeterministicTranslation

logging.getLogger("gfal2").setLevel(logging.WARNING)

SUCCESS = 0
FAILURE = 1


def read_disk_cache(diskcache_dump, config):
    """
    Read ascii dump from ldas diskcache

    :param diskcache_dump: Path to ascii dump from diskcache
    :param config: configparser object with usual diskcache fields
    :type config: ConfigParser instance
    :returns: List of files
    """
    try:
        os.stat(diskcache_dump)
    except (IOError, OSError) as cache_error:
        logging.critical(cache_error)
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                diskcache_dump)

    minimum_gps = config.getint('data', 'minimum-gps')
    maximum_gps = config.getint('data', 'maximum-gps')
    regexp = config.get('data', 'regexp')
    try:
        extension = config.get('data', 'extension')
    except NoOptionError:
        extension = 'gwf'

    logging.info("Parsing diskcache %s", diskcache_dump)
    logging.info("regexp=%s, gps-start-time=%d, gps-end-time=%d", regexp,
                 minimum_gps, maximum_gps)

    pathlist = list(
        DiskCacheFile(diskcache_dump,
                      minimum_gps=minimum_gps,
                      maximum_gps=maximum_gps,
                      regexp=regexp,
                      extension=extension,
                      prune=True,
                      update_file_count=True).expand())

    if extension == 'sft':
        try:
            calibration = config.get('common-metadata', 'calibration')
        except NoOptionError:
            raise ValueError("Missing calibration info from [common-metadata]")
        logging.info("Reducing path list to calibration=%s", calibration)
        pathlist = [path for path in pathlist if calibration in path]

    return pathlist


def grouper(lst, nchunk):
    """
    Split a list into nchunks
    """
    for idx in range(0, nchunk):
        yield lst[idx::nchunk]


def gfal_md5(pfn, max_tries=5, sleep_time=5):
    """
    Compute the MD5 checksum of a file using GFAL2.

    :param pfn: Physical filename, including protocol and hostname
    :type pfn: str
    :param max_tries: Number of times to retry operation
    :type max_tries: int
    :sleep_time: Initial sleep period in seconds between access attempts.
    Each attempt doubles the previous sleep time.
    :returns: str. The MD5 checksum
    """
    ctxt = gfal2.creat_context()
    for ntries in range(max_tries):
        try:
            return ctxt.checksum(pfn, 'MD5')
        except gfal2.GError as gfalerr:
            logging.info(gfalerr)
            logging.info("GFAL checksum failure (attempt %d of %d)", ntries,
                         max_tries)
            logging.info("Sleeping for %d s", sleep_time)
            sleep(sleep_time)
            sleep_time *= 2

    logging.critical("File access failure for %s", pfn)
    sys.exit(FAILURE)


def gfal_adler32(pfn, max_tries=5, sleep_time=5):
    """
    Compute the Adler32 checksum of a file using GFAL2.

    :param pfn: Physical filename, including protocol and hostname
    :type pfn: str
    :param max_tries: Number of times to retry operation
    :type max_tries: int
    :sleep_time: Initial sleep period in seconds between access attempts.
    Each attempt doubles the previous sleep time.
    :returns: str. The adler32 checksum
    """
    ctxt = gfal2.creat_context()
    for ntries in range(max_tries):
        try:
            return ctxt.checksum(pfn, 'Adler32')
        except gfal2.GError as gfalerr:
            logging.info(gfalerr)
            logging.info("GFAL checksum failure (attempt %d of %d)", ntries,
                         max_tries)
            logging.info("Sleeping for %d s", sleep_time)
            sleep(sleep_time)
            sleep_time *= 2

    logging.critical("File access failure for %s", pfn)
    sys.exit(FAILURE)


def gfal_stat(pfn, max_tries=5, sleep_time=5):
    """
    Stat a file.

    :param pfn: Physical filename, including protocol and hostname
    :type pfn: str
    :param max_tries: Number of times to retry operation
    :type max_tries: int
    :sleep_time: Initial sleep period in seconds between access attempts.
    Each attempt doubles the previous sleep time.
    :returns: class gfal2.Stat. GFAL2 stat object.
    """
    ctxt = gfal2.creat_context()
    for ntries in range(max_tries):
        try:
            return ctxt.stat(pfn)
        except gfal2.GError as gfalerr:
            logging.info(gfalerr)
            logging.info("GFAL stat failure (attempt %d of %d)", ntries,
                         max_tries)
            logging.info("Sleeping for %d s", sleep_time)
            sleep(sleep_time)
            sleep_time *= 2

    logging.critical("File access failure for %s", pfn)
    sys.exit(FAILURE)
    return ctxt.stat(pfn)


def gfal_bytes(pfn):
    """
    Compute the size in bytes of a file.

    :param pfn: Physical filename, including protocol and hostname
    :type pfn: str
    :param max_tries: Number of times to retry operation
    :type max_tries: int
    :sleep_time: Initial sleep period in seconds between access attempts.
    Each attempt doubles the previous sleep time.
    :returns: int. The size in bytes
    """
    return gfal_stat(pfn).st_size


def get_pfn(rse_info, path):
    """
    Return the full PFN with URL at this RSE

    Parameters
    ----------
    rse_info : dict
        Protocol related RSE attributes.  See
        `rucio/lib/rucio/rse/rsemanager.py`.
    scope : str
        Scope for the LFN
    path : str
        Path to the LFN
    """

    # Strip out any double //
    path = path.replace('//', '/')

    protocol = rse_info['protocols'][0]
    schema = protocol['scheme']
    prefix = protocol['prefix']
    port = protocol['port']
    rucioserver = protocol['hostname']

    # Determine URI prefix from RSE configuration
    if schema == 'srm':
        prefix = protocol['extended_attributes']['web_service_path'] + prefix
    url = schema + '://' + rucioserver
    if port != 0:
        url += ':' + str(port)


#   if rse_info['deterministic']:
#       # Use the RSE's lfn2pfn algorithm
#       lfn2pfn_translator = RSEDeterministicTranslation(rse=rse_info['rse'])
#       determined_path = lfn2pfn_translator.path(scope=scope,
#                                                 name=os.path.basename(path))
#       determined_path = os.path.join(prefix, determined_path)
#
#       # Check this agrees
#       if determined_path != path:
#           logging.critical("Provided PFN: %s, Determined PFN: %s", path,
#                            determined_path)
#           raise ValueError("Provided PFN does not match lfn2pfn algorithm")
#
#       url += determined_path
#
#   else:
    if rse_info['rse'] in ['ICRR-STAGING']:
        path = path.replace('/gpfs', '')

    url += path

    return url
