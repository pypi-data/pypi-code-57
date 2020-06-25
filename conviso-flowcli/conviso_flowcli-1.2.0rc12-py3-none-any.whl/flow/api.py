import requests
import json
from urllib.parse import urljoin
from os import SEEK_SET

PRODUCTION_API_URL = "https://app.conviso.com.br"
STAGING_API_URL = "https://homologa.conviso.com.br"
DEVELOPMENT_API_URL = "http://localhost:3000"
DEFAULT_API_URL = PRODUCTION_API_URL


class RequestsSession(requests.Session):

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)

        return super().request(
            method, url, *args, **kwargs
        )

class FlowAPIException(Exception):
    pass

class DeployNotFoundException(FlowAPIException):
    pass


class Deploys(object):
    DIFF_CONTENT_FILE_NAME = 'diff_content.txt'
    DIFF_CONTENT_MIME_TYPE = 'text/plain'
    ENDPOINT = '/api/v3/deploys'
    LIST_BY_PROJECT_ENPOINT ="api/v2/deploys/deploys_by_project_api_code"

    def __init__(self, client):
        self.client = client

    def create(self, project_code, **kargs):
        current_version = kargs.get('current_version')
        previous_version = kargs.get('previous_version')
        diff_content = kargs.get('diff_content')

        files = {
            'api_code': (None, project_code),

            'deploy[current_version][commit]': (None, current_version.get('commit')),
            'deploy[current_version][tag]': (None, current_version.get('tag')),

            'deploy[previous_version][commit]': (None, previous_version.get('commit')),
            'deploy[previous_version][tag]': (None, previous_version.get('tag')),
        }

        if diff_content:
            self._assert_filepointer_is_at_beginning(diff_content)
            diff_content_args = (
                self.DIFF_CONTENT_FILE_NAME,
                diff_content,
                self.DIFF_CONTENT_MIME_TYPE,
            )

            files.update({
                'deploy[diff_content]': diff_content_args,
            })

        session = self.client.requests_session
        response = session.post(self.ENDPOINT, files=files)

        response.raise_for_status()
        return response.json()


    def list(self, project_code, current_tag=None):
        data = {
            'api_code': project_code,
        }

        if current_tag:
            data.update({
                'current_tag': current_tag
            })

        session = self.client.requests_session
        response = session.get(self.LIST_BY_PROJECT_ENPOINT, json=data)
        response.raise_for_status()

        return {
            "deploys": response.json()
        }


    def get(self, project_code, current_tag):
        if not current_tag:
            raise ValueError(
                "current_tag is required and must be not empty"
            )

        list_result = self.list(project_code, current_tag)

        try:
            deploys = list_result.get('deploys')
            return deploys[0]
        except IndexError as e:
            raise DeployNotFoundException(
                "Deploy for current_tag[%s] not found" % current_tag
            ) from e

    def exists(self, project_code, current_tag):
        try:
            deploy = self.get(project_code, current_tag)
        except DeployNotFoundException:
            return False

        return True

    def get_latest(self, project_code):
        get_latest_endpoint = "%s/last" % self.ENDPOINT
        request_data = {
            'api_code': project_code
        }

        session = self.client.requests_session
        response = session.get(get_latest_endpoint, json=request_data)
        try:
            response.raise_for_status()
            deploy = response.json()

            if not deploy:
                raise DeployNotFoundException()

            return deploy
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise DeployNotFoundException() from error


    @staticmethod
    def _assert_filepointer_is_at_beginning(diff_content):
        is_seekable = lambda f: hasattr(f, 'seekable') and f.seekable()

        if is_seekable(diff_content):
            diff_content.seek(SEEK_SET)

class FindingReportLoader(object):
    ISSUES_FIELD = 'issues'

    def __init__(self, findings_reports, max_issues=25):
        self.max_issues = max_issues
        self._generator = self._create_generator(self, findings_reports)

    def read(self):
        return self._generator


    @classmethod
    def _create_generator(cls, loader, findings_reports):
        for report in findings_reports:
            report_data = json.load(report)
            issues = report_data.get(cls.ISSUES_FIELD, [])

            while True:
                first_n_issues, issues = (
                    issues[:loader.max_issues],
                    issues[loader.max_issues:]
                )

                if first_n_issues:
                    yield first_n_issues
                else:
                    break


class Findings(object):
    ENDPOINT = '/findings'
    REPORT_TYPE_FIELD = 'type'

    def __init__(self, client):
        self.client = client

    def create(self, project_code, commit_refs, finding_report_file, **kwargs):
        finding_report = json.load(finding_report_file)

        self.__inject_dynamic_finding_report_fields(
            finding_report, commit_refs, **kwargs
        )

        data = {
            'flow_project_id': project_code,
            'report': finding_report,
        }

        session = self.client.requests_session
        response = session.post(self.ENDPOINT, json=data)
        response.raise_for_status()

    @classmethod
    def __inject_dynamic_finding_report_fields(
        cls, finding_report, commit_refs, **kwargs
    ):
        report_dynamic_injected_fields = {}

        report_dynamic_injected_fields.update({
            'code_version': commit_refs
        })

        default_report_type = kwargs.get('default_report_type')

        if default_report_type and cls.REPORT_TYPE_FIELD not in finding_report:
            report_dynamic_injected_fields.update({
                cls.REPORT_TYPE_FIELD: default_report_type
            })

        finding_report.update(report_dynamic_injected_fields)


class DockerRegistry(object):
    SAST_ENDPOINT = '/auth/sast'

    def __init__(self, client):
        self.client = client

    def get_sast_token(self):
        session = self.client.requests_session
        response = session.get(self.SAST_ENDPOINT)
        response.raise_for_status()
        return response.text


class Client(object):

    def __init__(self, url=STAGING_API_URL, key=None, insecure=False):
        self.url = url
        self.insecure = insecure
        self.key = key

    @property
    def requests_session(self):
        session = RequestsSession(self.url)
        session.verify = not self.insecure
        session.headers.update({
            'x-api-key': self.key
        })

        return session

    @property
    def deploys(self):
        return Deploys(self)

    @property
    def findings(self):
        return Findings(self)

    @property
    def docker_registry(self):
        return DockerRegistry(self)

# TODO: Create Custom handle
# requests.exceptions.ConnectionError
# requests.exceptions.SSLError
# requests.exceptions.HTTPError
