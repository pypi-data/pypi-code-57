"""
Module implementing a driver for jobs issued by La Mancha
"""

from etna_api import EtnaSession
from logging import Logger
import os
import shutil
from typing import Any, Dict

from rocinante.driver import Driver
from rocinante.utils import sanitize_for_filename


def _identify_job(info: Dict[str, Any]) -> str:
    if "stage" in info:
        x = f"{info['module_id']}-{info['activity_id']}-{sanitize_for_filename(info['stage'])}-{info['group_id']}"
    else:
        x = f"{info['module_id']}-{info['activity_id']}-{info['group_id']}"
    return f"{x}-{info['name']}"


class LaManchaDriver(Driver):
    def __init__(self, logger: Logger, root_directory: str, config: Dict[str, Any]):
        self.logger = logger
        self.root_directory = root_directory
        self.config = config

    @staticmethod
    def create(logger: Logger, root_directory: str, config: Dict[str, Any]) -> 'Driver':
        os.makedirs(root_directory, exist_ok=True)
        return LaManchaDriver(logger, root_directory, config)

    def extract_job_information(self, body: Dict[str, Any]) -> Dict[str, Any]:
        info = body.copy()
        info["job_name"] = _identify_job(info)
        info["job_environment"] = info["name"]
        return info

    def retrieve_moulinette(self, info: Dict[str, Any]) -> str:
        return f"/home/doom/ETNA/rocinante/test"

    def format_result(self, body: Dict[str, Any], job_feedback: Dict[str, Any]) -> Dict[str, Any]:
        return job_feedback
