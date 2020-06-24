import json
import logging
import os
from os.path import expanduser

import urllib3
import yaml
import certifi

from .utils import bool_getenv
from .metadata import parse_env_list, parse_env_number
from .modules import get_installed_modules
import scopeagent

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


SCOPE_NATIVE_APP_CONFIG_PATH = expanduser('~/.scope/config.json')
SCOPE_CONFIG_PATH = './scope.yml'
logger = logging.getLogger(__name__)


# We can't use default parameters or @mock.patch won't work
def load_native_app_config_file(path=None):
    """Attempts to read the API endpoint and API key from the native Scope app configuration file."""
    path = path or SCOPE_NATIVE_APP_CONFIG_PATH
    try:
        with open(str(path), 'r') as config_file:
            config = json.load(config_file)
            try:
                if 'currentProfile' not in config:
                    return {}
                current_profile = config['currentProfile']
                profile = config['profiles'][current_profile]
                logger.debug('autodetected config profile: %s', profile)
                return profile
            # ** TODO ** raise original exception
            except KeyError:
                raise Exception('Invalid format in Scope configuration file at %s' % path)
    except FileNotFoundError:
        return {}


# We can't use default parameters or @mock.patch won't work
def load_scope_config_file(path=None):
    """Attempts to read the configuration file scope.yml"""
    path = path or SCOPE_CONFIG_PATH
    try:
        with open(str(path), 'r') as config_file:
            try:
                config = yaml.load(config_file, Loader=yaml.FullLoader)
                return config
            except yaml.YAMLError:
                raise Exception('Invalid format in scope.yml configuration file at %s' % path)
    except FileNotFoundError:
        return {'scope': {}}


def get_runner_configuration(current_branch, scope_yaml_config_file):
    should_use_runner = bool_getenv(
        'SCOPE_RUNNER_ENABLED', scope_yaml_config_file.get('runner', {}).get('enabled') or False,
    )
    runner_fail_retries = 0
    if should_use_runner:
        if 'SCOPE_RUNNER_FAIL_RETRIES' in os.environ:
            runner_fail_retries = parse_env_number(os.getenv('SCOPE_RUNNER_FAIL_RETRIES'))
        else:
            runner_fail_retries = scope_yaml_config_file.get('runner', {}).get('fail_retries', 0)

        if 'SCOPE_RUNNER_INCLUDE_BRANCHES' in os.environ:
            runner_include_branches = parse_env_list(os.getenv('SCOPE_RUNNER_INCLUDE_BRANCHES'))
        else:
            runner_include_branches = scope_yaml_config_file.get('runner', {}).get('include_branches') or []
        if len(runner_include_branches):
            should_use_runner = current_branch in runner_include_branches
        else:
            if 'SCOPE_RUNNER_EXCLUDE_BRANCHES' in os.environ:
                runner_exclude_branches = parse_env_list(os.getenv('SCOPE_RUNNER_EXCLUDE_BRANCHES'))
            else:
                runner_exclude_branches = scope_yaml_config_file.get('runner', {}).get('exclude_branches') or []
            if len(runner_exclude_branches):
                should_use_runner = current_branch not in runner_exclude_branches

    return (should_use_runner, runner_fail_retries)


def get_tests_to_cache(repository, commit, service, api_endpoint, api_key, metadata):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    config_request_data = {
        'repository': repository,
        'commit': commit,
        'service': service,
        'dependencies': get_installed_modules(),
    }
    config_request_data.update(metadata)
    encoded_config_request_data = json.dumps(config_request_data).encode('utf-8')
    try:
        response = http.request(
            'POST',
            '{api_endpoint}/api/agent/config'.format(api_endpoint=api_endpoint),
            headers={
                'X-Scope-ApiKey': api_key,
                'X-User-Agent': 'scope-agent-python/{agent_version}'.format(agent_version=scopeagent.version),
                'Content-Type': 'application/json',
            },
            body=encoded_config_request_data,
        )
        list_of_tests = json.loads(response.data.decode('utf-8'))['cached']
        return {(test['test_suite'], test['test_name']) for test in list_of_tests}

    except (urllib3.exceptions.HTTPError, JSONDecodeError, UnicodeDecodeError, KeyError):
        return {}


def get_stacktrace_configuration(scope_yaml_config_file):
    db_stacktrace = False
    http_stacktrace = False
    if 'SCOPE_INSTRUMENTATION_DB_STACKTRACE' in os.environ:
        db_stacktrace = bool_getenv('SCOPE_INSTRUMENTATION_DB_STACKTRACE', False)
    else:
        try:
            db_stacktrace = scope_yaml_config_file['instrumentation']['db']['stacktrace']
        except KeyError:
            pass

    if 'SCOPE_INSTRUMENTATION_HTTP_STACKTRACE' in os.environ:
        http_stacktrace = bool_getenv('SCOPE_INSTRUMENTATION_HTTP_STACKTRACE', False)
    else:
        try:
            http_stacktrace = scope_yaml_config_file['instrumentation']['http']['stacktrace']
        except KeyError:
            pass

    return db_stacktrace, http_stacktrace
