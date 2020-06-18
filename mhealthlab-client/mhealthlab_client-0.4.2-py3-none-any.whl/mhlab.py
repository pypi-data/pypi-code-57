"""mHealth Lab client

Usage:
  mhlab download STUDY [--pid=<id_or_file>] [--decrypt=<pwd>] [--folder=<folder>]
  mhlab signaligner --folder=<folder> --pid=<pid> --sr=<sampling_rate> [--date_range=<date_range>]
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


def mhlab():
    ver = arus.dev._find_current_version('.', 'mhealthlab_client')
    arguments = docopt(__doc__, version=f'mHealth Lab Client {ver}')
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
