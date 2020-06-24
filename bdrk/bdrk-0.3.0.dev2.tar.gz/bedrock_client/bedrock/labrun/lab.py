import base64
import codecs
import os
import os.path
import sys
from shutil import make_archive
from tempfile import TemporaryDirectory
from typing import Any, Mapping, Optional

import requests

CHUNK_SIZE_BYTES = 128
Utf8Decoder = codecs.getincrementaldecoder("utf-8")


class LabError(Exception):
    pass


def _remove_empty(map: Mapping) -> Mapping:
    return {k: v for k, v in map.items() if v}


def _upload_file(upload_url: str, filename: str) -> None:
    # For now, we just read into memory
    with open(filename, "rb") as f:
        filedata = f.read()

    rsp = requests.put(
        url=upload_url, data=filedata, headers={"Content-Type": "application/octet-stream"}
    )
    if rsp.status_code != 200:
        raise ConnectionError(f"Failed to upload to {upload_url}")


class LabRunner:
    def __init__(self, logger, api_domain: Optional[str] = None, api_token: Optional[str] = None):
        self.logger = logger
        api_domain = api_domain or os.environ.get("BEDROCK_API_DOMAIN") or "https://api.bdrk.ai"
        assert api_domain, "Bedrock API domain is undefined!"
        self.endpoint = f"{api_domain}/internal"
        self.token = api_token or os.environ.get("BEDROCK_API_TOKEN")
        assert self.token, "Bedrock access token is missing!"
        self.logger.debug("LabRunner instance created successfully")

    def _compress_and_upload(self, target_dir: str, upload_url: str) -> None:
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "archive")
            try:
                make_archive(base_name=filename, format="zip", root_dir=target_dir, base_dir="./")
            except Exception as ex:
                self.logger.exception(f"Error {ex} while making archive")
                raise ex
            try:
                _upload_file(upload_url=upload_url, filename=f"{filename}.zip")
                self.logger.debug(f"Uploaded {filename} to {upload_url}")
            except Exception as ex:
                raise LabError(f"Error {ex} while uploading file")
        self.logger.debug("Successfully compressed and uploaded file")

    def post_json(
        self,
        url: str,
        post_data: Mapping,
        run_token: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        self.logger.debug(f"Accessing {url}")
        if access_token:
            headers = {"content-type": "application/json", "X-Bedrock-Access-Token": access_token}
        elif run_token:
            headers = {"content-type": "application/json", "X-Bedrock-Api-Token": run_token}
        else:
            raise ValueError("Need at least one token")
        try:
            rsp = requests.post(url, headers=headers, json=post_data, timeout=30)
        except Exception as ex:
            self.logger.exception(f"Error {ex} while creating run: {post_data}")
            raise ex
        return rsp

    def _create_run(self, environment_id: str) -> Mapping:
        self.logger.debug("Creating run")
        url = f"{self.endpoint}/lab/run/"
        post_data = {"environment_id": environment_id}
        rsp = self.post_json(url=url, post_data=post_data, access_token=self.token)
        if not rsp or (rsp.status_code != 201):
            raise LabError(f"Failed to create lab run: {rsp}, {rsp.text}")
        data = rsp.json()
        run_id = data["entity_id"]
        self.logger.debug(f"Created lab run: id is {run_id}")
        return data

    def _submit_run(
        self,
        environment_id: str,
        download_url: str,
        config_file: str,
        config_file_path: str,
        run_token: str,
        script_parameters: Optional[Mapping[str, str]] = None,
        secrets: Optional[Mapping[str, str]] = None,
    ) -> Mapping:
        self.logger.debug("Submitting lab run")
        url = f"{self.endpoint}/lab/run/submit"
        post_data: Mapping[str, Any] = {
            "download_url": download_url,
            "config_file": config_file,
            "config_file_path": config_file_path,
            **({"script_parameters": script_parameters} if script_parameters else {}),
            **({"secrets": secrets} if secrets else {}),
        }
        rsp = self.post_json(url=url, post_data=post_data, run_token=run_token)
        if not rsp or (rsp.status_code != 202):
            raise LabError(f"Failed to submit lab run: {rsp}, {rsp.text}")
        return rsp.json()

    def stream_logs(self, run_id: str, step_id: str, run_token: str) -> None:
        self.logger.debug("Streaming logs")
        url = f"{self.endpoint}/lab/run/{run_id}/step/{step_id}/log"
        headers = {"X-Bedrock-Api-Token": run_token}
        decoder = Utf8Decoder(errors="replace")
        with requests.get(url, headers=headers, stream=True) as rsp:
            for chunk in rsp.iter_content(chunk_size=CHUNK_SIZE_BYTES):
                if chunk:
                    decoded = decoder.decode(chunk)
                    sys.stdout.write(decoded)
            self.logger.debug(f"Streaming logs done: status_code={rsp.status_code}")
        download_url = self._get_logs_url(run_id=run_id, step_id=step_id, run_token=run_token)
        print(f"\nDownload the logs here: {download_url}")

    def run(
        self,
        target_dir: str,
        environment_id: str,
        config_file_path: str,
        script_parameters: Optional[Mapping[str, str]] = None,
        secrets: Optional[Mapping[str, str]] = None,
    ) -> None:
        rsp_create = self._create_run(environment_id)
        run_id = rsp_create["entity_id"]
        upload_url = rsp_create["upload_url"]
        download_url = rsp_create["download_url"]
        run_token = rsp_create["run_token"]
        self._compress_and_upload(target_dir=target_dir, upload_url=upload_url)
        with open(os.path.join(target_dir, config_file_path)) as f:
            config_file = base64.b64encode(f.read().encode()).decode()
        rsp_submit = self._submit_run(
            environment_id=environment_id,
            download_url=download_url,
            config_file=config_file,
            config_file_path=config_file_path,
            run_token=run_token,
            script_parameters=script_parameters,
            secrets=secrets,
        )
        rsp_run_id = rsp_submit["entity_id"]
        assert rsp_run_id == run_id, f"ID mismatch: {rsp_run_id} vs {run_id}"

        print(f"\nLAB_RUN_ID\t{run_id}")
        print(f"LAB_RUN_TOKEN\t{run_token}\n")
        print(f"Run steps:\nName{' ' * 32}\tSTEP_ID")
        for step in rsp_submit["steps"]:
            truncated_name = step["name"] if len(step["name"]) < 32 else step["name"][:29] + "..."
            print(f"{truncated_name:32}\t{step['entity_id']}")
        print("\nTo get logs:")
        print("bdrk labrun logs ${LAB_RUN_ID} ${STEP_ID} ${LAB_RUN_TOKEN}")
        print("\nTo get artefact:")
        print("bdrk labrun artefact ${LAB_RUN_ID} ${LAB_RUN_TOKEN}\n")

    def _get_logs_url(self, run_id: str, step_id: str, run_token: str) -> str:
        url = f"{self.endpoint}/lab/run/{run_id}/step/{step_id}/log/download_url"
        headers = {"X-Bedrock-Api-Token": run_token}
        with requests.get(url, headers=headers) as rsp:
            if not rsp or (rsp.status_code != 200):
                self.logger.info(f"Failed to get logs: {rsp.status_code} {rsp.content.decode()}")
                raise ConnectionError(f"Failed to get download url for logs: {run_id}")
            return rsp.content.decode()

    def get_artefact_url(self, run_id: str, run_token: str) -> str:
        url = f"{self.endpoint}/lab/run/{run_id}/artefact/download_url"
        headers = {"X-Bedrock-Api-Token": run_token}
        with requests.get(url, headers=headers) as rsp:
            if not rsp or (rsp.status_code != 200):
                self.logger.info(
                    f"Failed to get artefact: {rsp.status_code} {rsp.content.decode()}"
                )
                raise ConnectionError(f"Failed to get download url for artefact: {run_id}")
            return rsp.content.decode()
