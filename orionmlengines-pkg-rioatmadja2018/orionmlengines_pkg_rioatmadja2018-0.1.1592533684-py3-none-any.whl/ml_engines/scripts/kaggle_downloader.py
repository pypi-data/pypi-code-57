#!/usr/bin/env python
import requests
import subprocess
from typing import Dict, List
from datetime import datetime
import os

class Kaggle(object):
    def __init__(self):
        self.time_stamp: str = datetime.utcnow().isoformat()

    def load_orion_pkg(self, pypi_pkg: str, linux_academy_server: str) -> bool:
        """
        This function will retrieve credentials from Linux Academy and download custom package from PyPI repository, everytime the notebook is starting
        :pypi_pkg: given the custom package from ORION project
        :linux_academy: given dynamic IP Address from Linux Academy
        :return: a boolean installation status
        """
        if not pypi_pkg:
            raise ValueError(f"Missing required parameter: {pypi_pkg}")

        kaggle_ip: str = requests.get('https://ifconfig.me').text  # Record Kaggle IP
        user_agent: Dict = {'User-Agent': f'(KAGGLE_REQUEST_{kaggle_ip}_{self.time_stamp}) '}  # Record request from Kaggle Notebook
        pypi_creds: str = requests.get(f'http://{linux_academy_server}/data', headers=user_agent).text

        # save output
        with open(os.path.join(os.path.abspath('.'), '.pypirc'), 'w') as f:
            f.write(pypi_creds)
        f.close()

        # Install orionmlengines
        response: List[str] = [resp.decode('utf-8') for resp in
                               subprocess.Popen(pypi_pkg, shell=True, stdout=subprocess.PIPE).stdout.readlines()]
        return response.__len__() != 0