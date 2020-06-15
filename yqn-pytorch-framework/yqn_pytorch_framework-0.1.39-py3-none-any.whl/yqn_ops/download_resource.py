import argparse

import errno
import os

import sys
import yaml
from termcolor import colored

from yqn_common.download_file import download_url_to_file
from yqn_common.helper import set_logger

APP_DEC = """                                                                           
YYYYYYY       YYYYYYY          QQQQQQQQQ           NNNNNNNN        NNNNNNNN
Y:::::Y       Y:::::Y        QQ:::::::::QQ         N:::::::N       N::::::N
Y:::::Y       Y:::::Y      QQ:::::::::::::QQ       N::::::::N      N::::::N
Y::::::Y     Y::::::Y     Q:::::::QQQ:::::::Q      N:::::::::N     N::::::N
YYY:::::Y   Y:::::YYY     Q::::::O   Q::::::Q      N::::::::::N    N::::::N
   Y:::::Y Y:::::Y        Q:::::O     Q:::::Q      N:::::::::::N   N::::::N
    Y:::::Y:::::Y         Q:::::O     Q:::::Q      N:::::::N::::N  N::::::N
     Y:::::::::Y          Q:::::O     Q:::::Q      N::::::N N::::N N::::::N
      Y:::::::Y           Q:::::O     Q:::::Q      N::::::N  N::::N:::::::N
       Y:::::Y            Q:::::O     Q:::::Q      N::::::N   N:::::::::::N
       Y:::::Y            Q:::::O  QQQQ:::::Q      N::::::N    N::::::::::N
       Y:::::Y            Q::::::O Q::::::::Q      N::::::N     N:::::::::N
       Y:::::Y            Q:::::::QQ::::::::Q      N::::::N      N::::::::N
    YYYY:::::YYYY          QQ::::::::::::::Q       N::::::N       N:::::::N
    Y:::::::::::Y            QQ:::::::::::Q        N::::::N        N::::::N
    YYYYYYYYYYYYY              QQQQQQQQ::::QQ      NNNNNNNN         NNNNNNN
                                       Q:::::Q                             
                                        QQQQQQ                             
                                                                           
"""


def capitalize(name):
    return name.capitalize()


def get_args_parser():
    from yqn_ops import __version__
    parser = argparse.ArgumentParser(description='download model from config_file')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-e', '--env', type=str, required=True, default='local', help='local/online')
    parser.add_argument('-f', '--file', type=str, default='', help='custom file path')
    parser.add_argument('-F', '--force', action="store_true", default=False, help='remove exist files')
    return parser


def download_dir(logger, file_url, dist_dir, oss_crc, remove_force):
    try:
        os.makedirs(os.path.dirname(dist_dir))
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Directory already exists, ignore.
            pass
        else:
            # Unexpected OSError, re-raise.
            raise

    # parts = urlparse(file_url)
    # filename = os.path.basename(parts.path)
    if remove_force and os.path.exists(dist_dir):
        os.remove(dist_dir)
    cached_file = dist_dir
    if not os.path.exists(cached_file):
        # sys.stderr.write('Downloading: "{}" to {}\n'.format(file_url, cached_file))
        logger.info('Downloading: "{}" to {}\n'.format(file_url, cached_file))
        download_url_to_file(file_url, cached_file, crc=oss_crc)


def parse_command(logger, parser_fn=get_args_parser, printed=True):
    root_project_dir = './'
    args = parser_fn().parse_args()
    if printed:
        param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])
        print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))

    if len(args.file) > 0 and args.file != '-' and os.path.exists(args.file):
        config_file_path = args.file
    else:
        config_file_path = os.path.join(root_project_dir, 'model_url_config_' + args.env + '.yml')
    with open(config_file_path) as file:
        documents = yaml.full_load(file)
        for document in documents:
            if not document['local_path'].endswith(".trt"):
                download_dir(logger, document['file_url'], document['local_path'], document['crc'], args.force)
            else:
                print("Ignore TensorRT : ", document['local_path'])


def main():
    print(APP_DEC)
    """
    下载oss模型到本地
    """

    logger = set_logger(colored("DownloadModels", 'red'), True)
    parse_command(logger)


if __name__ == "__main__":
    main()
