# coding=utf-8
__version__ = "5.0.40"

import logging
import sys

logging.basicConfig()
dclogger = logging.getLogger("dt-challenges-runner")
dclogger.setLevel(logging.DEBUG)

enc = sys.getdefaultencoding()
from docker import __version__ as docker_version
from requests import __version__ as requests_version

vmsg = f"dt-challenges-runner {__version__} - encoding {enc} docker_py {docker_version} requests {requests_version}"
dclogger.info(vmsg)
from .runner import dt_challenges_evaluator

from .runner_local import runner_local_main
