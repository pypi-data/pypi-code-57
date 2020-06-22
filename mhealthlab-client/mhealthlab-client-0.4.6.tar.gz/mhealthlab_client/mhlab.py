"""mHealth Lab client

Usage:
  mhlab download STUDY [--pid=<id_or_file>] [--decrypt=<pwd>] [--folder=<folder>] [--debug]
  mhlab signaligner --folder=<folder> --pid=<pid> --sr=<sampling_rate> [--date_range=<date_range>] [--debug]
  mhlab --help
  mhlab --version

Arguments:
  STUDY                                     Study name. It should match the folder name used to store datasets on the server.

Options:
  -h, --help                                Show help message
  -v, --version                             Show program version
  -p <pid>, --pid <pid>                     The participant ID or a txt file with list of participant IDs each on a separate line
  -d <pwd>, --decrypt <pwd>                 Use <pwd> to decrypt the downloaded files.
  -f <folder>, --folder <folder>            Local folder for downloaded dataset.
  -s <sampling_rate>, --sr <sampling_rate>  The sampling rate of the converted sensor file in Actigraph csv format used for signaligner.
  --date_range <date_range>                 The start and stop date of the data to be converted. E.g., "--date_range=2020-06-01,2020-06-10", "--date_range=2020-06-01", or "--date_range=,2020-06-10".
"""

from docopt import docopt
from .main import Client
from .android_watch import AndroidWatch
from loguru import logger
import os
import arus
import sys
from outdated import check_outdated
import pkg_resources


def mhlab():
    ver = pkg_resources.get_distribution("mhealthlab-client").version
    print('\n')
    print(f'mHealth Lab Client {ver}\n')
    check_client_outdated(ver)
    arguments = docopt(__doc__, version=f'mHealth Lab Client {ver}')
    if arguments['--debug']:
        logger.remove()
        logger.add(sys.stderr, level='DEBUG')
    else:
        logger.remove()
        logger.add(sys.stderr, level='INFO')
    logger.debug(arguments)
    if arguments['download']:
        study_name = arguments['STUDY']
        pwd = str.encode(
            arguments['--decrypt']) if arguments['--decrypt'] is not None else None
        to = arguments['--folder'] or './' + study_name
        if arguments['--pid'] is None:
            pid = None
        else:
            pid = arguments['--pid']
            if os.path.exists(pid):
                pid = Client.extract_participant_list(pid)
        logger.add(to + "/mhlab_download.log", rotation="500 MB")
        if pid is None:
            download_all(study_name, to, pwd)
        elif type(pid) is list:
            download_by_participant_list(study_name, pid, to, pwd)
        else:
            download_by_participant(study_name, pid, to, pwd)
    elif arguments['signaligner']:
        to = arguments['--folder']
        sr = int(arguments['--sr'])
        pid = arguments['--pid']
        date_range = arguments['--date_range'].split(
            ',') if arguments['--date_range'] is not None else None
        convert_sensor_files(to, pid, sr, date_range)


def check_client_outdated(ver):
    is_outdated, latest_version = check_outdated(
        'mhealthlab-client', ver)
    arus_ver = pkg_resources.get_distribution("arus").version
    is_arus_outdated, latest_arus_version = check_outdated('arus', arus_ver)
    if is_outdated:
        logger.warning(
            f'The client version {ver} is outdated. The latest version is {latest_version}')
        logger.warning(
            f'Please run "pip install -U mhealthlab-client" or "pip3 install -U mhealthlab-client" to update.')
        exit(1)

    if is_arus_outdated:
        logger.warning(
            f'The client core dependency arus {arus_ver} is outdated. The latest version is {latest_arus_version}')
        logger.warning(
            f'Please run "pip install -U arus" or "pip3 install -U arus" to update.')
        exit(1)


def download_all(study_name, to, pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect()
    client.download_all(study_name, to, pwd)


def download_by_participant(study_name, pid, to, pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect()
    client.download_by_participant(study_name, pid, to, pwd)


def download_by_participant_list(study_name, pids, to, pwd):
    client = Client()
    if not client.validate_study_name(study_name):
        exit(1)
    client.connect()
    for pid in pids:
        logger.info("Download data for {}".format(pid))
        client.download_by_participant(study_name, pid, to, pwd)


def convert_sensor_files(to, pid, sr, date_range):
    watch = AndroidWatch(to, pid)
    watch.convert_to_actigraph(date_range=date_range, sr=sr)


if __name__ == '__main__':
    mhlab()
