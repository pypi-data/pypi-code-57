"""
MIT License
Copyright (c) 2020 williamfzc
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from minadb import ADBDevice
from loguru import logger
import requests
import typing
import time
import psutil

__PROJECT_NAME__ = r"cort_client"
__AUTHOR__ = r"williamfzc"
__AUTHOR_EMAIL__ = r"fengzc@vip.qq.com"
__LICENSE__ = r"MIT"
__VERSION__ = r"0.2.0"


class CortJob(object):
    def __init__(self, product_name: str, user_name: str, cli: "_JobLayer", *_, **__):
        self.product_name = product_name
        self.user_name = user_name

        # from cli
        self.device = cli.device
        self.serial_no = cli.device.serial_no
        self.host = cli.host
        self.port = cli.port

        # build this job
        self.package_name = self.get_package_name()
        self.version_name = self.get_version_name()
        self.hash_name = self.get_hash_name()
        logger.info(
            f"job generated: {self.product_name} / {self.package_name} / {self.version_name} / {self.hash_name}"
        )

    def get_package_name(self) -> str:
        raise NotImplementedError

    def get_version_name(self) -> str:
        raise NotImplementedError

    def get_hash_name(self) -> str:
        raise NotImplementedError

    def start(self) -> psutil.Process:
        # todo: actually this method was designed for android. but what about other platforms?
        command = [
            "am",
            "instrument",
            "-w",
            "-r",
            # required
            "-e",
            "coverage",
            "true",
            "-e",
            "debug",
            "false",
            "-e",
            "class",
            f"{self.package_name}.CortInstrumentedTest",
            # optional
            # product name
            "-e",
            "productName",
            self.product_name,
            # package name
            "-e",
            "packageName",
            self.package_name,
            # version name
            "-e",
            "versionName",
            self.version_name,
            # hash name
            "-e",
            "hashName",
            self.hash_name,
            # user name
            "-e",
            "userName",
            self.user_name,
            # serial no
            "-e",
            "serialNo",
            self.serial_no,
            # host
            "-e",
            "host",
            self.host,
            # port
            "-e",
            "port",
            str(self.port),
            # file type (android things)
            "-e",
            "fileType",
            "ec",
            # step (period)
            "-e",
            "step",
            # todo: now locked
            str(5000),
            # runner
            f"{self.package_name}.test/{self.package_name}.CortTestRunner",
        ]
        logger.debug(f"job start with command: {command}")
        process = self.device.shell(command, no_wait=True)
        return psutil.Process(process.pid)
        # todo: test will never stop by default. need a cleanup here


class CortAPI(object):
    METHOD_GET = "GET"
    METHOD_POST = "POST"

    _METHOD_MAP = {METHOD_GET: requests.get, METHOD_POST: requests.post}
    # fill these
    method_name: typing.Union[METHOD_GET, METHOD_POST]
    path: str

    @property
    def method(self) -> typing.Callable[..., requests.Response]:
        return self._METHOD_MAP[self.method_name]


class ProviderArtifactAPI(CortAPI):
    method_name = CortAPI.METHOD_GET
    path = "/artifact"


class ProviderSessionSyncAPI(CortAPI):
    method_name = CortAPI.METHOD_POST
    path = "/session/sync"


class ProviderJobStatusAPI(CortAPI):
    method_name = CortAPI.METHOD_GET
    path = "/rq"


class ProviderSessionQueryAPI(CortAPI):
    method_name = CortAPI.METHOD_GET
    path = "/session/query"


class ProviderSessionNewAPI(CortAPI):
    method_name = CortAPI.METHOD_POST
    path = "/session/new"


class CortAPIError(BaseException):
    pass


class _BaseClient(object):
    def __init__(self, host: str, port: int, serial_no):
        # server
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"
        self.ver = "v1"
        # apis
        self.api_provider_artifact = ProviderArtifactAPI()
        self.api_provider_job_status = ProviderJobStatusAPI()
        self.api_provider_session_sync = ProviderSessionSyncAPI()
        self.api_provider_session_query = ProviderSessionQueryAPI()
        self.api_provider_session_new = ProviderSessionNewAPI()
        # local
        self.device: ADBDevice = ADBDevice(serial_no)

    def heartbeat(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/").ok
        except requests.exceptions.BaseHTTPError:
            return False

    def register_device(self, serial_no: str):
        self.device = ADBDevice(serial_no)

    def exec_api(self, api: CortAPI, *args, **kwargs) -> requests.Response:
        url = f"{self.base_url}/api/{self.ver}{api.path}"
        logger.debug(f"exec api: {url}")
        return api.method(url, *args, **kwargs)

    @staticmethod
    def handle_resp(resp: requests.Response) -> typing.Union[str, dict, list]:
        if resp.ok:
            return resp.json()
        raise CortAPIError(resp.text)


class _JobLayer(_BaseClient):
    class JobStatus(object):
        def __init__(self, status: str, result: dict):
            self.status = status
            self.result = result

        def ok(self) -> bool:
            return self.status == "finished"

        def __str__(self):
            return f"CortJobStatus: status={self.status}; result={self.result}"

        __repr__ = __str__

    def new_job(
        self,
        job_kls: typing.Type[CortJob],
        product_name: str,
        user_name: str,
        *args,
        **kwargs,
    ) -> CortJob:
        return job_kls(product_name, user_name, self, *args, **kwargs)

    def job_status(self, job_id: str) -> JobStatus:
        resp = self.exec_api(self.api_provider_job_status, params={"job_id": job_id})
        return self.JobStatus(**self.handle_resp(resp))

    def wait_job_until_done(self, job_id: str, step: int = 1) -> JobStatus:
        status = self.job_status(job_id)
        if not status.ok():
            time.sleep(step)
            return self.wait_job_until_done(job_id)
        return status


class _SessionLayer(_BaseClient):
    def sync_session(self, session_id: str, **kwargs) -> str:
        resp = self.exec_api(
            self.api_provider_session_sync, data={"session_id": session_id, **kwargs}
        )
        return self.handle_resp(resp)

    def query_session(self, **kwargs) -> dict:
        resp = self.exec_api(self.api_provider_session_query, params=kwargs)
        return self.handle_resp(resp)

    def new_session(self, **kwargs) -> str:
        resp = self.exec_api(self.api_provider_session_new, data=kwargs)
        return self.handle_resp(resp)


class _ArtifactLayer(_BaseClient):
    def query_artifact(self, **kwargs) -> typing.Union[list, dict]:
        resp = self.exec_api(self.api_provider_artifact, params=kwargs)
        return self.handle_resp(resp)


class CortClient(_JobLayer, _SessionLayer, _ArtifactLayer):
    pass
