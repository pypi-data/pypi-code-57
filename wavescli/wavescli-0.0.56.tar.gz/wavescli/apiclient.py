import requests
import yaml

__version__ = '0.0.1'


class ApiClient(object):

    def __init__(self, url, key, version='api'):

        if not url:
            raise RuntimeError('WAVES_URL environment variable not set')

        if not key:
            raise RuntimeError('API_KEY environment variable not set')

        self.waves_url = url
        self.api_key = key
        self.api_version = version
        self.session = requests.Session()
        self._workflow = None
        # login salvando token

    def workflow(self, identifier):
        url = self._build_url('workflows/{}'.format(identifier))
        response = requests.get(
            url,
            headers=self._get_headers(),
        )
        if not response.status_code == 200:
            return "Erro: {}: {}".format(response, response.content)
        self._workflow = response.json()
        self._execution = None
        return self

    def get_inputs(self):
        if self._execution:
            return self._execution['inputs']
        elif self._workflow:
            self._inputs = {}
            for item in self._workflow['definition']['inputs']:
                self._inputs[item['name']] = '' if item.get('required') else None
                if item.get('default'):
                    self._inputs[item['name']] = item.get('default')
            return self._inputs
        return {}

    def execution(self, identifier=None):
        if not identifier:
            self._execution = None
            self._inputs = None
            return self

        url = self._build_url('executions/{}'.format(identifier))
        response = requests.get(
            url,
            headers=self._get_headers(),
        )
        if not response.status_code == 200:
            return "Erro: {}: {}".format(response, response.content)

        self._execution = response.json()
        self._inputs = self._execution['inputs']
        self._workflow = self._execution['workflow']
        return self

    def create(self, inputs=None):
        if self._execution and not inputs:
            return self.run(
                workflow_identifier=self._workflow['identifier'],
                inputs=self._inputs,
            )

        elif self._workflow and inputs:
            return self.run(
                workflow_identifier=self._workflow['identifier'],
                inputs=inputs,
            )
        self._results = None
        return {
            "message": "Nothing to do",
        }

    def register_businesstask(self, btask_content):
        url = self._build_url('business-tasks')
        response = requests.post(
            url,
            headers=self._get_headers(),
            data=btask_content.encode('utf-8'))
        if not response.status_code == 201:
            return "Erro : {}: {}".format(response, response.content)
        return response.json()

    def publish_businesstask(self, btask_content):

        definition = yaml.load(btask_content, Loader=yaml.FullLoader)
        identifier = '{}@{}'.format(
            definition.get('name'), definition.get('version', 'latest'))

        url = self._build_url('business-tasks/{}/publish'.format(identifier))

        response = requests.put(
            url,
            headers=self._get_headers())

        if not response.status_code == 200:
            return "Erro : {}: {}".format(response, response.content)
        return response.json()

    def create_workflow(self, workflow_content):
        url = self._build_url('workflows')
        response = requests.post(
            url,
            headers=self._get_headers(),
            data=workflow_content.encode('utf-8'))
        if not response.status_code == 201:
            return "Erro : {}: {}".format(response, response.content)
        return response.json()

    def run(self, workflow_identifier, inputs):
        """
        Create a new execution for the workflow identifier
        """
        url = self._build_url('executions')
        new_execution = {
            "workflow_identifier": workflow_identifier,
            "inputs": inputs,
        }
        response = requests.post(
            url,
            headers=self._get_headers(content_type='application/json'),
            json=new_execution)

        if not response.status_code == 201:
            return "Erro : {}: {}".format(response, response.content)
        self._results = response.json()
        return self._results

    def list_workers(self):
        """
        list active workers
        """
        url = self._build_url('workers')
        response = requests.get(
            url,
            headers=self._get_headers(),
        )

        if not response.status_code == 200:
            return "Erro: {}: {}".format(response, response.content)
        return response.json()

    def _get_headers(self, content_type='application/x-yaml'):
        headers = {
            'User-Agent': 'wavescli/{}'.format(__version__),
            'Content-Type': content_type,
            'X-API-KEY': self.api_key
        }
        return headers

    def _build_url(self, endpoint):
        return '/'.join([self.waves_url, self.api_version, endpoint])


class ApiError(RuntimeError):

    def __init__(self, response):
        message = 'status={} data={}'.format(
            response.status_code, response.json())
        super(ApiError, self).__init__(message)
