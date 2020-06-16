"""
Module implementing a driver for jobs issued by the intra
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
        return f"{info['module_id']}-{info['activity_id']}-{sanitize_for_filename(info['stage'])}-{info['group_id']}"
    else:
        return f"{info['module_id']}-{info['activity_id']}-{info['group_id']}"


def _identify_job_environment(info: Dict[str, Any]) -> str:
    if "stage" in info:
        return f"{info['module_id']}-{info['activity_id']}-{sanitize_for_filename(info['stage'])}"
    else:
        return f"{info['module_id']}-{info['activity_id']}"


class IntraValidationDriver(Driver):
    def __init__(self, logger: Logger, root_dir: str, config: Dict[str, Any]):
        self.logger = logger
        self.root_dir = root_dir
        self.config = config

    @staticmethod
    def create(logger: Logger, root_directory: str, config: Dict[str, Any]) -> 'Driver':
        return IntraValidationDriver(logger, root_directory, config)

    def extract_job_information(self, body: Dict[str, Any]) -> Dict[str, Any]:
        info = {}
        _, module_id, _, activity_id = body["files_path"].split("/")
        info["module_id"] = int(module_id)
        info["activity_id"] = int(activity_id)
        info["group_id"] = body["result"]["group_id"]
        info["leader"] = body["result"]["leader"]
        info["stage"] = body["result"]["stage"]
        info["stage_end"] = body["tokens"]["stage_end"]
        info["request_date"] = body["date"]
        info["job_name"] = _identify_job(info)
        info["job_environment"] = _identify_job_environment(info)
        return info

    def _download_from_intra(self, moulinette_directory, info):
        session = EtnaSession(
            username=self.config["intra_user"],
            password=self.config["intra_password"],
            request_retries=10,
            retry_on_statuses=(500, 502, 504)
        )

        intra_moulinette_dir = "resources/moulinette/"
        files = session.get_activity_stage_files_list(info["module_id"], info["activity_id"], info["stage"])

        files = map(lambda x: (x["rel_path"], x["rel_path"].rsplit(f"/stages/{info['stage']}/", maxsplit=1)[1]), files)
        files = filter(lambda x: x[1].startswith(intra_moulinette_dir), files)

        os.mkdir(moulinette_directory)

        for dist_path, local in files:
            local = os.path.relpath(local, intra_moulinette_dir)
            dirname = os.path.dirname(local)
            if not os.path.exists(f"{moulinette_directory}/{dirname}"):
                os.makedirs(f"{moulinette_directory}/{dirname}")
            data = session.download_file_from_activity(info["module_id"], info["activity_id"], dist_path)
            with open(f"{moulinette_directory}/{local}", "wb") as f:
                f.write(data)

    def retrieve_moulinette(self, info: Dict[str, Any]) -> str:
        sanitized_req_date = sanitize_for_filename(info["request_date"])

        moulinette_directory = f"{self.root_dir}/{_identify_job_environment(info)}-{sanitized_req_date}"

        if os.path.exists(moulinette_directory):
            self.logger.info(f"Reusing cached moulinette from {info['request_date']}")
            return moulinette_directory
        try:
            self.logger.info(f"Downloading the moulinette from the intranet...")
            self._download_from_intra(moulinette_directory, info)
        except Exception:
            shutil.rmtree(moulinette_directory, ignore_errors=True)
            raise

        return moulinette_directory

    def format_result(self, body: Dict[str, Any], job_feedback: Dict[str, Any]) -> Dict[str, Any]:
        job_results = job_feedback["results"]

        feedback_messages = []
        for result in job_results:
            for _, requirement_message, _ in filter(lambda req: not req[0], result["requirements"]):
                feedback_messages.append(f"requirement failed: {requirement_message}")
            if result["assertion_failure"] is not None:
                feedback_messages.append(f"assertion failed: {result['assertion_failure']}")

        result_template = body["result"]
        if len(feedback_messages) > 0:
            result_template["output"] = "KO:\n" + "".join(feedback_messages)
            result_template["status"] = 1
        else:
            result_template["output"] = "OK"
            result_template["status"] = 0
        return result_template
