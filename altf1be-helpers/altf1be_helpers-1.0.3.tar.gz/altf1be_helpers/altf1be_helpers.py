# -*- coding: utf-8 -*-

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests
import logging
from datetime import timedelta, datetime
from pathlib import Path
from os import path

from dateutil.tz import tzutc
from dateutil.parser import parse

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import glob
import sys
import re
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All"
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

# constants
MISSING_LIBRARY = -1

logging.getLogger("urllib3").setLevel(logging.WARNING)

class AltF1BeHelpers:

    @staticmethod
    def parse_requirements(filename):
        """ Load requirements from a pip requirements file 

        Useful to feed the setup.py when you want to deploy a library on pypi
        """

        lineiter = (line.strip() for line in open(filename))
        return [line for line in lineiter if line and not line.startswith("#")]

        requirements = parse_requirements(os.path.join(
            os.path.dirname(__file__), 'requirements.txt')
        )
        logging.info(f"requirements.txt: {requirements}")

    @staticmethod
    def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @staticmethod
    def hide_secrets_from_url(url):
        text_to_hide = url[url.find('appid=')+6:url.find('&lat=')]
        result = url.replace(text_to_hide, 'HIDDEN_DATA')
        return result

    @staticmethod
    def date_utc(s):
        """Used to set time zone of values in a Pandas DataFrame

        """
        return parse(s, tzinfos=tzutc)

    @staticmethod
    def valid_time(string):
        """
            extract HH-MM-SS from a filename similar to /kaggle/input/2020-06-11_00-08-41-sca-tork-easycube-site.json
        """
        #print(f'string: {string}')
        try:
            mat = re.findall(
                r"([0-2][0-3]|[0-1][0-9])-([0-5][0-9])-([0-5][0-9])",
                string
            )  # HH:MM:SS
            if mat is not None:
                return ':'.join(mat[1])
            else:
                print('else')
                return None
        except ValueError:
            print("ValueError error:", sys.exc_info())
        print('None')
        return None

    @staticmethod
    def valid_date(string):
        """
            extract YYYY-MM-SS from a filename similar to /kaggle/input/2020-06-11_00-08-41-sca-tork-easycube-site.json
        """
        #print(f'string: {string}')
        try:
            mat = re.match(
                r'(?:(?:19|20)\d\d)-(?:11|12|10|0?[1-9])-(?:11|12|10|0?[1-9])', string
            )  # YYY-MM-DD
            if mat is not None:
                return mat.group()
        except ValueError:
            print("ValueError error:", sys.exc_info())
        return None

    @staticmethod
    def count_files_in_dir(directory):

        def unique(list1):

            # insert the list to the set
            list_set = set(list1)
            # convert the set to the list
            unique_list = (list(list_set))
            for x in unique_list:
                pass  # print(x)
            return unique_list

        filenames = glob.glob(
            directory,
            recursive=True
        )
        files_count = len(filenames)

        filenames_list = list()
        filenames_set = set()
        for filename in filenames:
            filenames_list.append(os.path.basename(filename))
            filenames_set.add(os.path.basename(filename))

        print(f"len(filenames_list): {len(filenames_list)}")
        print(f"len(filenames_set): {len(filenames_set)}")
        print(f"directory: {directory}")
        print(f"files_count: {files_count}")

    @staticmethod
    def is_interactive():
        # return True if running on Kaggle
        try:
            return 'runtime' in get_ipython().config.IPKernelApp.connection_file
        except NameError:
            if (path.exists('/kaggle/working')):
                return True
            else:
                return False

    @staticmethod
    def unicode_to_ascii(a):
        """
        remove accents and apostrophes
        """
        try:
            import unidecode
        except ModuleNotFoundError:
            print(f"unidecode library is missing in you environment. Install unidecode or use conda or venv to set the right environment")
            exit(MISSING_LIBRARY)
        # def remove_accents_apostrophe(a):
        a = unidecode.unidecode(a)  # remove accent
        a = a.replace("'", '')  # remove apostrophe
        return a

    @staticmethod
    def input_directory(directories=[]) -> str:
        input_directory = '/kaggle/input'
        if AltF1BeHelpers.is_interactive():
            input_directory = os.path.join(
                input_directory, os.path.sep.join(directories))
        else:
            input_directory = os.path.join(os.path.abspath(
                os.getcwd()), os.path.sep.join(directories)) # TODO: revise all codes. former code was this "output_directory", "data",

        return input_directory

    @staticmethod
    def output_directory(directories=[]) -> str:
        output_directory = '/kaggle/working'
        if AltF1BeHelpers.is_interactive():
            output_directory = os.path.join(
                output_directory, os.path.sep.join(directories)
            )
        else:
            output_directory = os.path.join(os.path.abspath(
                os.getcwd()), "output_directory", "data", os.path.sep.join(directories)
            )

        Path(output_directory).mkdir(
            parents=True,
            exist_ok=True
        )
        return output_directory

    @staticmethod
    def create_append_log_file(filename):
        """ create or append a log file stored in current_dir/logs/{filename}

        """

        filepath_log = os.path.join(
            AltF1BeHelpers.output_directory(
                ['logs']
            ),
            filename
        )
        msg = f"The log file is stored here: {filepath_log}"
        print(msg)
        logging.info(msg)
        
        return filepath_log

    @staticmethod
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)


if __name__ == "__main__":

    text = "éè à iïî où &é'(§è!çàaQwxs $ µ `"
    print(
        f"unicode_to_ascii(text): '{text}' becomes '{AltF1BeHelpers.unicode_to_ascii(text)}'"
    )
    print(
        f"is_interactive(): {AltF1BeHelpers.is_interactive()}"
    )

    for single_date in AltF1BeHelpers.daterange(
        datetime.now() - timedelta(2),
        datetime.now() - timedelta(0)
    ):
        print(f'daterange(): {single_date.strftime("%Y-%m-%d")}')

    url = "/data/2.5/uvi/history?appid=secret_api_key&lat=lat&lon=lon&cnt=cnt&start=start_date&end=end_date"

    print(
        f'{AltF1BeHelpers.hide_secrets_from_url(url=url)}'
    )

    print(
        f'parse_requirements : {AltF1BeHelpers.parse_requirements("requirements.txt")}'
    )

log_filename = AltF1BeHelpers.create_append_log_file(f"{os.path.basename(__file__)}.log")

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO
)