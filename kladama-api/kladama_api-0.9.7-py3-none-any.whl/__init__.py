import requests
import re
from kladama.helpers import *
from kladama.queries import *
from kladama.entities import *
from kladama.operations import *


class Environment:

    def __init__(self, api_url_base):
        self._api_url_base = api_url_base

    def get_url_from(self, path):
        return '{0}{1}'.format(self._api_url_base, path)


class Environments:

    @property
    def dev(self):
        return Environment('http://localhost')

    @property
    def prod(self):
        return Environment('https://kladama.com')

    @property
    def sandbox(self):
        return Environment('https://kladama.com')


class Session:

    def __init__(self, env, api_token):
        self._env = env
        self._api_token = api_token

    @property
    def env(self):
        return self._env

    @property
    def api_token(self):
        return self._api_token


class Error:

    def __init__(self, code, message: str):
        self._code = code
        self._message = message

    @property
    def code(self):
        return self._code

    @property
    def message(self) -> str:
        return self._message

    def __str__(self):
        return '{0}: {1}'.format(self.code, self.message)


class Success:

    def __init__(self, result):
        self._result = result

    @property
    def result(self):
        return self._result


def authenticate(env, api_token):
    return Session(env, api_token)


class Context:

    def __init__(self, session):
        self._session = session

    @property
    def env(self):
        return self.session.env

    @property
    def session(self):
        return self._session

    def get(self, query):
        if isinstance(query, HelperBase):
            return self._get_helper_response(query)

        if isinstance(query, BinaryDataQuery):
            return self._get_binary_data(query)

        if isinstance(query, SimpleResultsQuery):
            return self._get_first_entity(query)

        return self._get_entities(query)

    def execute(self, operation_builder: OperationBuilder):
        operation = operation_builder.build()
        url = self.env.get_url_from(operation.url_path)

        if isinstance(operation, PostOperation):
            return self._web_post(url, operation.post_obj)

        if isinstance(operation, PutOperation):
            return self._web_put(url, operation.put_obj)

        if isinstance(operation, DeleteOperation):
            return self._web_delete(url)

        return Error(400, 'Operation not defined')

    # private methods

    @staticmethod
    def _is_successfully_response(response):
        return 200 <= response.status_code < 300

    def _get_web_headers(self):
        api_token = self.session.api_token
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(api_token)
        }

    def _web_get(self, url):
        headers = self._get_web_headers()

        response = requests.get(url, headers)
        if self._is_successfully_response(response):
            return response

        return Error(response.status_code, response.content.decode('utf-8'))

    def _web_get_with_content(self, url, content):
        headers = self._get_web_headers()

        response = requests.get(url, headers, data=json.dumps(content))
        if self._is_successfully_response(response):
            return response

        return Error(response.status_code, response.content.decode('utf-8'))

    def _web_delete(self, url):
        headers = self._get_web_headers()

        response = requests.delete(url, headers=headers)
        if self._is_successfully_response(response):
            return Success(None)

        return Error(response.status_code, response.content.decode('utf-8'))

    def _web_post(self, url, data):
        headers = self._get_web_headers()

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if self._is_successfully_response(response):
            return Success(json.loads(response.content.decode('utf-8')))

        return Error(response.status_code, response.content.decode('utf-8'))

    def _web_put(self, url, data):
        headers = self._get_web_headers()

        response = requests.put(url, headers=headers, data=json.dumps(data))
        if self._is_successfully_response(response):
            return Success(json.loads(response.content.decode('utf-8')))

        return Error(response.status_code, response.content.decode('utf-8'))

    def _web_get_json(self, api_url):
        response = self._web_get(api_url)
        if isinstance(response, Error):
            return response

        return json.loads(response.content.decode('utf-8'))

    def _web_get_json_with_content(self, api_url, content):
        response = self._web_get_with_content(api_url, content)
        if isinstance(response, Error):
            return response

        return json.loads(response.content.decode('utf-8'))

    def _get_root_obj(self, query):
        url = self.env.get_url_from(query.url_path)
        json_obj = query.entity_meta.json_obj

        response = self._web_get_json(url)
        if isinstance(response, Error):
            return response

        embedded_key = '_embedded'
        if embedded_key in response and json_obj in response[embedded_key]:
            return response[embedded_key][json_obj]

        return []

    def _get_helper_response(self, helper: HelperBase):
        url = self.env.get_url_from(helper.url_path)
        json_obj = helper.obj

        response = self._web_get_json_with_content(url, json_obj)
        if isinstance(response, Error):
            return response

        return response

    def _get_entities(self, query):
        root_obj = self._get_root_obj(query)
        if isinstance(root_obj, Error):
            return root_obj

        entity_class = query.entity_meta.entity_class
        entity_list = []
        for entity in root_obj:
            entity_list.append(entity_class(entity))

        return entity_list

    def _get_first_entity(self, query):
        entity_list = self._get_entities(query)
        if isinstance(entity_list, Error):
            return entity_list

        if len(entity_list) > 0:
            return entity_list[0]

        return None

    def _get_binary_data(self, query: BinaryDataQuery):
        url = self.env.get_url_from(query.url_path)
        response = self._web_get(url)
        if isinstance(response, Error):
            return response

        filename_match = re.match('.* filename=(.*)', response.headers['Content-disposition'], re.M|re.I)
        return BinaryData({
            'name': filename_match.group(1),
            'content': response.content
        })


# Accessories

class Query:

    @property
    def aoi(self):
        return AreaOfInterestQuery()

    @property
    def phenom(self):
        return PhenomenaQuery()

    @property
    def org(self):
        return OrganizationQuery()

    @property
    def schedule(self):
        return ScheduleQuery()

    @property
    def subsc(self):
        return SubscriptionQuery()

    @property
    def src(self):
        return SourceQuery()

    @property
    def user(self):
        return UserQuery()

    @property
    def var(self):
        return VariableQuery()


class Operations:

    @property
    def add_aoi(self):
        return CreateAreaOfInterestBuilder()

    @property
    def check_schedule(self):
        return CheckScheduleBuilder()

    @property
    def clear_schedule(self):
        return ClearScheduleBuilder()

    @property
    def delete_aoi(self):
        return DeleteAreaOfInterestBuilder()

    @property
    def periodic_subsc(self):
        return CreatePeriodicSubscriptionBuilder()

    @property
    def re_schedule(self):
        return ReScheduleBuilder()

    @property
    def unsubscribe(self):
        return DeleteSubscriptionBuilder()


class Helpers:

    @staticmethod
    def check_aoi(aoi_obj):
        return CheckAoiHelper(aoi_obj)

