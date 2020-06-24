import logging
import os
import platform
import uuid

from six.moves.urllib_parse import urlparse

import opentracing

import scopeagent
from scopeagent.agent.config import (
    load_native_app_config_file,
    load_scope_config_file,
    get_runner_configuration,
    get_tests_to_cache,
    get_stacktrace_configuration,
)
from .ci import get_ci_tags, get_repository_information
from .modules import get_installed_modules
from .git import detect_git_info
from .metadata import parse_env_dictionary, parse_env_list
from .utils import bool_getenv
from ..instrumentation import patch_all
from ..recorders.http import HTTPRecorder
from ..tracer import BasicTracer, tags

logger = logging.getLogger(__name__)
DEFAULT_API_ENDPOINT = 'https://app.scope.dev'


class AgentError(Exception):
    pass


class Agent:
    def __init__(
        self,
        dsn=None,
        api_key=None,
        api_endpoint=None,
        active_http_payloads=None,
        active_db_statement_values=None,
        extra_http_headers=None,
        code_path_enabled=None,
        repository=None,
        commit=None,
        service=None,
        branch=None,
        source_root=None,
        debug=None,
        dry_run=None,
        command=None,
        config_file_path=None,
        extra_metadata={},
    ):
        """
        Creates a new Scope agent instance (without installing it). All parameters are optional and will be autodetected
        from the environment where possible.

        :param dsn: short form for API key and API endpoint when sending data to the Scope backend
        :param api_key: the API key to use when sending data to the Scope backend
        :param api_endpoint: the API endpoint of the Scope instance where the data is going to be sent
        :param active_http_payloads: if set to True, http payloads are included
        :param active_db_statement_values: if set to True, database statements are included
        :param repository: the git repository URL of the service being instrumented
        :param commit: the commit hash being instrumented
        :param service: the name of the service being instrumented (defaults to `default`)
        :param branch: the branch being instrumented
        :param source_root: the absolute path to the root of the git repository in the local filesystem
        :param debug: if `true`, enables verbose debug logging
        :param dry_run: if `true`, avoids actually sending data to the backend
        :param command: command string used to launch the service being instrumented
        """

        git_info = detect_git_info()
        native_app_config_file = load_native_app_config_file()
        self.scope_yaml_config_file = load_scope_config_file(config_file_path)

        env_variable_metadata = parse_env_dictionary(os.getenv('SCOPE_METADATA'))
        config_file_metadata = self.scope_yaml_config_file.get('metadata') or {}

        self.dsn = dsn or os.getenv('SCOPE_DSN') or native_app_config_file.get('dsn')
        if self.dsn:
            url = urlparse(self.dsn)
            self.api_key = url.username
            self.api_endpoint = '{scheme}://{hostname}'.format(scheme=url.scheme, hostname=url.hostname)
        else:
            self.api_key = api_key or os.getenv('SCOPE_APIKEY') or native_app_config_file.get('apiKey')
            self.api_endpoint = (
                api_endpoint
                or os.getenv('SCOPE_API_ENDPOINT')
                or native_app_config_file.get('apiEndpoint')
                or DEFAULT_API_ENDPOINT
            )
        if active_http_payloads is None:
            self.active_http_payloads = bool_getenv(
                'SCOPE_INSTRUMENTATION_HTTP_PAYLOADS',
                self.scope_yaml_config_file.get('instrumentation', {}).get('http', {}).get('payloads') or False,
            )
        else:
            self.active_http_payloads = active_http_payloads

        if active_db_statement_values is None:
            self.active_db_statement_values = bool_getenv(
                'SCOPE_INSTRUMENTATION_DB_STATEMENT_VALUES',
                self.scope_yaml_config_file.get('instrumentation', {}).get('db', {}).get('statement_values') or False,
            )
        else:
            self.active_db_statement_values = active_db_statement_values

        if extra_http_headers is None:
            if 'SCOPE_INSTRUMENTATION_HTTP_HEADERS' in os.environ:
                self.extra_http_headers = parse_env_list(os.getenv('SCOPE_INSTRUMENTATION_HTTP_HEADERS'))
            else:
                self.extra_http_headers = (
                    self.scope_yaml_config_file.get('instrumentation', {}).get('http', {}).get('headers') or []
                )
        else:
            self.extra_http_headers = extra_http_headers

        if code_path_enabled is None:
            self.code_path_enabled = bool_getenv(
                'SCOPE_CODE_PATH_ENABLED', self.scope_yaml_config_file.get('code_path', {}).get('enabled') or False,
            )
        else:
            self.code_path_enabled = code_path_enabled

        ci_repository_information = get_repository_information()

        self.repository = (
            repository
            or os.getenv('SCOPE_REPOSITORY')
            or self.scope_yaml_config_file.get('repository')
            or ci_repository_information.get('repository')
            or git_info.get('repository')
        )
        self.commit = (
            commit
            or os.getenv('SCOPE_COMMIT_SHA')
            or self.scope_yaml_config_file.get('commit_sha')
            or ci_repository_information.get('commit')
            or git_info.get('commit')
        )
        self.service = service or os.getenv('SCOPE_SERVICE') or self.scope_yaml_config_file.get('service', 'default')
        self.branch = (
            branch
            or os.getenv('SCOPE_BRANCH')
            or self.scope_yaml_config_file.get('branch')
            or ci_repository_information.get('branch')
            or git_info.get('branch')
        )
        self.source_root = (
            source_root
            or os.getenv('SCOPE_SOURCE_ROOT')
            or self.scope_yaml_config_file.get('source_root')
            or ci_repository_information.get('source_root')
            or git_info.get('root')
            or os.getcwd()
        )

        if '~' in self.source_root:
            self.source_root = os.path.expanduser(self.source_root)

        if debug is None:
            debug = bool_getenv('SCOPE_DEBUG', False)

        if debug:
            logging.basicConfig()
            logging.getLogger('scopeagent').setLevel(logging.DEBUG)

        if dry_run is None:
            dry_run = bool_getenv('SCOPE_DRYRUN', False)

        self.dry_run = dry_run
        self.command = command or os.getenv('SCOPE_COMMAND')

        self.tracer = None
        self.agent_id = str(uuid.uuid4())

        self.extra_metadata = config_file_metadata or {}
        self.extra_metadata.update(extra_metadata)
        self.extra_metadata.update(env_variable_metadata)

        should_use_runner, fail_retries = get_runner_configuration(self.branch, self.scope_yaml_config_file)

        show_db_stacktrace, show_http_stacktrace = get_stacktrace_configuration(self.scope_yaml_config_file)

        self.runner_enabled = should_use_runner
        self.fail_retries = fail_retries
        self.tests_to_cache = []
        self.show_db_stacktrace = show_db_stacktrace
        self.show_http_stacktrace = show_http_stacktrace

    def _get_agent_capabilities(self):
        return {
            tags.CODE_PATH: self.code_path_enabled,
            tags.RUNNER_CACHE: self.runner_enabled,
            tags.RUNNER_RETRIES: self.runner_enabled and self.fail_retries > 0,
            tags.PROCESS_END: True,
        }

    def _get_instrumentation_mode(self, testing_mode=None, set_global_tracer=None, autoinstrument=None):
        # If one of the variables in the chain is not specified, we fall back to the following step:
        # testing_mode: agent.install input > SCOPE_TESTING_MODE env var > True
        # set_global_tracer: agent.install input > SCOPE_SET_GLOBAL_TRACER env var > scope.yml value > False
        # autoinstrument: agent.install input > SCOPE_INSTRUMENTATION_ENABLED env var > scope.yml value > True

        if testing_mode is None:
            if 'SCOPE_TESTING_MODE' in os.environ:
                testing_mode = bool_getenv('SCOPE_TESTING_MODE', True)
            else:
                testing_mode = self.scope_yaml_config_file.get('testing_mode', True)

        if set_global_tracer is None:
            if 'SCOPE_SET_GLOBAL_TRACER' in os.environ:
                set_global_tracer = os.getenv('SCOPE_SET_GLOBAL_TRACER')
            else:
                set_global_tracer = self.scope_yaml_config_file.get('tracer', {}).get('global', False)

        if autoinstrument is None:
            autoinstrument = os.getenv('SCOPE_INSTRUMENTATION_ENABLED')

        if autoinstrument is None:
            autoinstrument = self.scope_yaml_config_file.get('instrumentation', {}).get('enabled')

        if autoinstrument is None:
            autoinstrument = True

        return testing_mode, set_global_tracer, autoinstrument

    def install(self, testing_mode=None, set_global_tracer=None, autoinstrument=None):
        """
        Installs the tracer and instruments all libraries.

        :param testing_mode: whether the command launched is for running tests
        :param set_global_tracer: if `true`, sets the Scope tracer as the OpenTracing global tracer
        :param autoinstrument: if `true`, patches all supported libraries to enable instrumentation
        :return: None
        """
        if not self.api_key:
            raise AgentError('API key is required')
        if not self.api_endpoint:
            raise AgentError('API endpoint is required')

        testing_mode, set_global_tracer, autoinstrument = self._get_instrumentation_mode(
            testing_mode, set_global_tracer, autoinstrument
        )

        # Install tracer
        metadata = {
            tags.AGENT_ID: self.agent_id,
            tags.AGENT_VERSION: scopeagent.version,
            tags.AGENT_TYPE: 'python',
            tags.SOURCE_ROOT: self.source_root,
            tags.HOSTNAME: platform.node(),
            tags.PLATFORM_NAME: platform.system(),
            tags.PLATFORM_VERSION: platform.release(),
            tags.ARCHITECTURE: platform.machine(),
            tags.PYTHON_IMPLEMENTATION: platform.python_implementation(),
            tags.PYTHON_VERSION: platform.python_version(),
            tags.HTTP_PAYLOADS: self.active_http_payloads,
            tags.DB_STATEMENTS_INSTRUMENTATION: self.active_db_statement_values,
            tags.HTTP_HEADERS: self.extra_http_headers,
            tags.DEPENDENCIES: get_installed_modules(),
            tags.CODE_PATH_ENABLED: self.code_path_enabled,
            tags.CAPABILITIES: self._get_agent_capabilities(),
        }
        metadata.update(self.extra_metadata)
        if self.repository:
            metadata[tags.REPOSITORY] = self.repository
        if self.commit:
            metadata[tags.COMMIT] = self.commit
        if self.branch:
            metadata[tags.BRANCH] = self.branch
        if self.service:
            metadata[tags.SERVICE] = self.service
        if self.command:
            metadata[tags.COMMAND] = self.command
        metadata.update(get_ci_tags())
        logger.debug('metadata=%s', metadata)

        # If in testing mode, send health checks every second to track agent running status
        if testing_mode:
            logger.debug('Using a health check period of 1 second (testing mode)')
            period = 1
        else:
            logger.debug('Using a health check period of 1 minute (non testing mode)')
            period = 60

        metadata[tags.TESTING] = testing_mode

        if self.runner_enabled:
            self.tests_to_cache = get_tests_to_cache(
                self.repository, self.commit, self.service, self.api_endpoint, self.api_key, metadata
            )

        recorder = HTTPRecorder(
            test_only=True,
            testing_mode=testing_mode,
            api_key=self.api_key,
            api_endpoint=self.api_endpoint,
            metadata=metadata,
            period=period,
            dry_run=self.dry_run,
        )
        self.tracer = BasicTracer(recorder)
        scopeagent.global_agent = self

        self.tracer.runner_enabled = self.runner_enabled
        self.tracer.tests_to_cache = self.tests_to_cache
        self.tracer.fail_retries = self.fail_retries
        self.tracer.show_db_stacktrace = self.show_db_stacktrace
        self.tracer.show_http_stacktrace = self.show_http_stacktrace
        self.tracer.active_db_statement_values = self.active_db_statement_values

        # Register as opentracing global tracer if configured to do so
        if set_global_tracer:
            logger.debug('Using Scope Agent tracer as global tracer (opentracing.tracer)')
            opentracing.tracer = self.tracer

        # Patch all supported libraries
        if autoinstrument:
            logger.debug('Auto instrumentation is enabled')
            patch_all(tracer=self.tracer)
        else:
            logger.debug('Auto instrumentation is disabled')
