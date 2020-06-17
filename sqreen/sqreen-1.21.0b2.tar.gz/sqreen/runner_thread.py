# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Sqreen Python agent thread composition
"""
import atexit
import json
import os
import random
import sys
import threading
import time
import traceback
from copy import copy
from logging import getLogger
from threading import Event, Thread

from .__about__ import __version__
from ._vendors.urllib3.exceptions import HTTPError  # type: ignore
from .actions import ActionStore
from .config import CONFIG
from .constants import CHANGELOG_URL, COMPATIBILITY_URL, STATUS_URL
from .deliverer import get_deliverer
from .exceptions import (
    InvalidApplicationName,
    UnsupportedFrameworkVersion,
    UnsupportedPythonVersion,
)
from .frameworks import debug
from .http_client import Urllib3Connection
from .instrumentation import Instrumentation
from .log import configure_root_logger
from .metrics import MetricsStore
from .remote_command import RemoteCommand
from .remote_exception import RemoteException
from .runner import (
    MAX_OBS_QUEUE_LENGTH,
    MAX_QUEUE_LENGTH,
    CappedQueue,
    Runner,
    RunnerSettings,
    RunnerStop,
    process_initial_commands,
)
from .runtime_infos import (
    RuntimeInfos,
    get_parent_cmdline,
    get_process_cmdline,
)
from .session import InvalidSession, InvalidToken, Session
from .signal_client import get_signal_client
from .utils import (
    configure_newrelics_ignore_exception,
    configure_raven_breadcrumbs,
)

RUNNER_THREAD = None
RUNNER_THREAD_PID = None
RUNNER_THREAD_RESTARTING = False
RUNNER_LOCK = threading.RLock()

# Instrumentation timeout, max time waiting for the runner thread to instrument the application
try:
    INSTRUMENTATION_TIMEOUT = int(os.getenv("SQREEN_INSTRUMENTATION_TIMEOUT", 6))
except ValueError:
    INSTRUMENTATION_TIMEOUT = 6

# Graceful timeout, max time waiting for the runner thread to exit before exiting
try:
    GRACEFUL_TIMEOUT = int(os.getenv("SQREEN_GRACEFUL_TIMEOUT", 5))
except ValueError:
    GRACEFUL_TIMEOUT = 5
GRACEFUL_FAIL_MSG = "Sqreen thread didn't exit after %s seconds"

LOGGER = getLogger(__name__)


def uwsgi_version_info():
    """Return uWSGI version tuple if run in uWSGI, None otherwise."""
    # Import must be delayed inside the function, because the uwsgi module is
    # not known by sqreen-start.
    try:
        import uwsgi  # type: ignore
    except ImportError:
        return None
    else:
        return uwsgi.version_info


def should_start_runner_thread():
    """This function contains the logic used to check if the thread
    should be restarted. Beware, this function *must not* call any hooks.
    """
    global RUNNER_THREAD
    global RUNNER_THREAD_PID

    runner_stopped = False
    if RUNNER_THREAD is not None \
            and RUNNER_THREAD.runner is not None \
            and RUNNER_THREAD.runner.stop is True:
        runner_stopped = True

    return RUNNER_THREAD_PID != os.getpid() and not runner_stopped


def before_hook_point():
    global RUNNER_THREAD
    global RUNNER_THREAD_PID
    global RUNNER_THREAD_RESTARTING

    # /!\ The order of execution in this function must not change
    # without a careful review. /!\
    if should_start_runner_thread():
        # It is cheap to first call should_start_runner_thread instead
        # of just locking everytime.
        with RUNNER_LOCK:
            # If we are in a recursive call, do nothing
            if RUNNER_THREAD_RESTARTING is True:
                LOGGER.debug("The runner thread is already restarting")
                return
            # If a concurrent thread has already started the thread, do nothing
            if not should_start_runner_thread():
                LOGGER.info("The runner thread has already been started")
                return
            # Else, restart the thread
            try:
                RUNNER_THREAD_RESTARTING = True
                runner = RUNNER_THREAD.replace()
                runner.start()

                RUNNER_THREAD = runner
                RUNNER_THREAD_PID = os.getpid()

                LOGGER.info(
                    "Sucessfully started runner thread for pid: %d", os.getpid()
                )
            finally:
                RUNNER_THREAD_RESTARTING = False


BLACKLISTED_PARENT_COMMANDS = (
    "ipython",
    "celery worker",
    "rq worker",
    "manage.py shell",
    "pshell",
)
BLACKLISTED_COMMANDS = BLACKLISTED_PARENT_COMMANDS + ("newrelic-admin",)


def get_app_name():
    """ Get the current application name. Return a string if the name is valid.
    Raise InvalidApplicationName otherwise.
    """
    config_app_name = CONFIG["APP_NAME"]
    if config_app_name is not None:
        app_name = config_app_name
    else:
        app_name = "python-application"

    try:
        if isinstance(app_name, bytes):
            app_name = app_name.decode("utf-8")
    except UnicodeDecodeError:
        raise InvalidApplicationName

    # Check the app name is not empty and does not contain
    # any invalid characters (ASCII control chars lower than 0x20)
    if not app_name or any([ord(c) < 0x20 for c in app_name]):
        raise InvalidApplicationName

    return app_name


def get_session(url, token, app_name=None, proxy_url=None):
    """ Create a connection with the endpoint URL and a session. Returns only
    the session.
    """
    LOGGER.warning(
        "Connection to %s%s",
        url,
        " using proxy %s" % proxy_url if proxy_url else "",
    )
    con = Urllib3Connection(url, proxy_url)
    session = Session(con, token, app_name)
    return session


def post_app_sqreen_exception(data):
    """Post a Sqreen exception happening at application level.
    This function does not need a session.

    This function is used to report instrumentation errors. It should never
    fail.
    """
    token = CONFIG["TOKEN"]
    if not token:
        return

    try:
        app_name = get_app_name()
        session = get_session(
            CONFIG["URL"], token, app_name, proxy_url=CONFIG["PROXY_URL"]
        )
        session.post_app_sqreen_exception(data)
    except Exception:
        pass


def start():
    # type: () -> None
    """ Start the background thread and start protection
    """
    # Check if the agent is not disabled first
    try:
        disabled = int(os.getenv("SQREEN_DISABLE", 0))
    except ValueError:
        disabled = 0

    # Configure logging
    configure_root_logger(CONFIG["LOG_LEVEL"], CONFIG["LOG_LOCATION"])

    # Retrieve the command used to launch the process
    command = get_process_cmdline()

    # Retrieve the parent command
    parent_command = get_parent_cmdline()

    # Check if we shouldn't launch ourselves
    for blacklisted_command in BLACKLISTED_COMMANDS:
        if blacklisted_command in command:
            LOGGER.debug(
                "Sqreen agent is disabled when running %s.",
                blacklisted_command,
            )
            return
    for blacklisted_parent_command in BLACKLISTED_PARENT_COMMANDS:
        if blacklisted_parent_command in parent_command:
            LOGGER.debug(
                "Sqreen agent is disabled when running %s.",
                blacklisted_parent_command,
            )
            return
    if hasattr(sys, "argv") and len(sys.argv) >= 2 and sys.argv[1] == "test":
        LOGGER.debug("Sqreen agent is disabled when running tests.")
        return

    if disabled:
        LOGGER.debug("Sqreen agent is disabled.")
        return

    try:
        runtime_infos = RuntimeInfos().all()
    except UnsupportedFrameworkVersion as exception:
        msg = (
            "%s version %s is not supported in this agent version.\n"
            "Sqreen agent is disabled, you're not protected.\n"
            "Documentation can be found at %s.\n"
            "Changelog can be found at %s."
        )
        LOGGER.critical(
            msg,
            exception.framework.title(),
            exception.version,
            COMPATIBILITY_URL,
            CHANGELOG_URL,
        )
        # Alter os.environ?
        return
    except UnsupportedPythonVersion as exception:
        msg = (
            "Python version %s is not supported in this agent version.\n"
            "Sqreen agent is disabled, you're not protected.\n"
            "Documentation can be found at %s.\n"
            "Changelog can be found at %s."
        )
        LOGGER.critical(
            msg, exception.python_version, COMPATIBILITY_URL, CHANGELOG_URL
        )
        return
    except Exception:
        msg = (
            "Runtime information about the system could not be retrieved.\n"
            "Sqreen agent is disabled, you're not protected.\n"
            "Documentation can be found at %s.\n"
        )
        LOGGER.critical(msg, COMPATIBILITY_URL)
        post_app_sqreen_exception(RemoteException.from_exc_info())
        return

    # Configure raven breadcrumbs at start
    configure_raven_breadcrumbs()

    # Ignore Sqreen Exception from APM NewRelics
    configure_newrelics_ignore_exception()

    global RUNNER_THREAD
    global RUNNER_THREAD_PID

    # Check for double instrumentation
    if RUNNER_THREAD is None:
        try:
            runner = RunnerThread(runtime_infos)
            runner.start()

            done = runner.unblock_main_thread.wait(INSTRUMENTATION_TIMEOUT)
            if done is not True:
                post_app_sqreen_exception(RemoteException(
                    "InstrumentationTimeout",
                    "Timeout during instrumentation",
                    exception_payload={
                        "runner_thread_started": runner.started,
                        "runner_thread_was_alive": runner.is_alive(),
                        "instrumentation_enabled": runner.instrumentation.enabled,
                        "runtime_infos": runtime_infos,
                    },
                    stack=runner.stacktrace,
                ).to_dict())

                LOGGER.critical(
                    "Sqreen could not instrument your application in less than %ds.\n"
                    "Please check your account is not expired and your application has network connectivity.\n"
                    "You can also check Sqreen status on %s.",
                    INSTRUMENTATION_TIMEOUT, STATUS_URL)

        except Exception:
            LOGGER.critical(
                "Sqreen thread has failed to start, you're not protected",
                exc_info=True,
            )
            return

        RUNNER_THREAD = runner
        RUNNER_THREAD_PID = os.getpid()


def get_initial_features(config_features, login_features):
    LOGGER.debug("Login features: %s", login_features)

    final_features = copy(login_features)

    if config_features:
        parsed_config_features = {}
        try:
            parsed_config_features = json.loads(config_features)
        except (ValueError, TypeError):
            LOGGER.warning(
                "Invalid config initial features %s",
                config_features,
                exc_info=True,
            )

        if parsed_config_features and isinstance(parsed_config_features, dict):
            msg = "Override login initial features with %s"
            LOGGER.warning(msg, parsed_config_features)

            final_features.update(parsed_config_features)

            LOGGER.warning("Final features %s", final_features)

    return final_features


def get_runner(
    config,
    login_result,
    session,
    queue,
    runtime_infos,
    observations_queue,
    instrumentation,
    settings,
):
    initial_features = get_initial_features(
        config["INITIAL_FEATURES"], login_result.get("features", {})
    )

    # Get a signal client if the feature is enabled
    use_signals = initial_features.get("use_signals", False)
    signal_client = get_signal_client(
        session=session,
        batch_size=initial_features.get("batch_size", 0),
        max_staleness=initial_features.get("max_staleness", 0)
    ) if use_signals else None

    # Get the right deliverer according to initial features
    deliverer = get_deliverer(
        initial_features.get("batch_size", 0),
        initial_features.get("max_staleness", 0),
        session,
        signal_client=signal_client,
    )
    remote_command = RemoteCommand.with_production_commands()
    action_store = ActionStore()
    metrics_store = MetricsStore()
    metrics_store.register_production_aggregators()
    metrics_store.register_default_metrics()

    # Setup the runner
    runner = Runner(
        queue,
        observations_queue,
        session,
        deliverer,
        remote_command,
        runtime_infos,
        instrumentation,
        action_store,
        metrics_store,
        settings,
        initial_features,
        signal_client=signal_client,
    )
    return runner


class RunnerThread(Thread):
    """ Class responsible for starting the runner and monitor it
    """

    name = "SqreenRunnerThread"

    def __init__(self, runtime_infos, queue=None, observations_queue=None,
                 instrumentation=None, settings=None):
        super(RunnerThread, self).__init__()
        self.daemon = True
        self.queue = queue or CappedQueue(MAX_QUEUE_LENGTH)
        self.observations_queue = observations_queue or CappedQueue(MAX_OBS_QUEUE_LENGTH)
        self.unblock_main_thread = Event()
        self.runtime_infos = runtime_infos
        self.instrumentation = instrumentation or Instrumentation(
            self.observations_queue, self.queue, before_hook_point
        )
        self.settings = settings or RunnerSettings()
        self.runner = None
        self.started = False

    @property
    def stacktrace(self):
        """Get the runner thread stack trace if it exists.
        """
        frame = sys._current_frames().get(self.ident, None)
        if frame is not None:
            return traceback.extract_stack(frame)

    def run(self):
        """ Launch the runner
        """
        self.started = True
        LOGGER.debug("Starting Sqreen %s", __version__)
        # FIXME this part should be more tested
        while True:
            session = None
            self.runner = None

            try:
                token = CONFIG["TOKEN"]
                if not token:
                    msg = (
                        "Sorry but we couldn't find your Sqreen token.\n"
                        "Your application is NOT currently protected by Sqreen.\n"
                        "\n"
                        "Have you filled your sqreen.ini?"
                    )
                    LOGGER.critical(msg)
                    self.unblock_main_thread.set()
                    return

                try:
                    app_name = get_app_name()
                except InvalidApplicationName:
                    msg = (
                        "Sorry but your application name seems invalid.\n"
                        "Your application is NOT currently protected by Sqreen.\n"
                        "\n"
                        "Please visit the following link: https://docs.sqreen.com/faq/org-token-migration/#application-name-limitations"
                    )
                    LOGGER.critical(msg)
                    self.unblock_main_thread.set()
                    return

                LOGGER.warning("Using token %r and application name %r", token, app_name)

                # Initiate HTTP connection to the backend and the session
                session = get_session(
                    CONFIG["URL"], token, app_name, proxy_url=CONFIG["PROXY_URL"]
                )

                runtime_infos = dict(self.runtime_infos)
                runtime_infos["various_infos"] = {
                    k: v
                    for k, v in runtime_infos.get("various_infos", {}).items()
                    if k != "dependencies"
                }
                try:
                    login_result = session.login(runtime_infos)
                except InvalidToken:
                    msg = (
                        "Sorry but your Sqreen token appears to be invalid.\n"
                        "Your application is NOT currently protected by Sqreen.\n"
                        "\n"
                        "Please check the token against the interface."
                    )
                    LOGGER.critical(msg)
                    self.unblock_main_thread.set()
                    return
                except HTTPError:
                    msg = (
                        "Sorry but Sqreen's backend appears to be unavailable.\n"
                        "Your application is NOT currently protected by Sqreen.\n"
                        "\n"
                        "Please check http://sqreen.status.io for outage.\n"
                        "\n"
                        "Otherwise, back.sqreen.io may be blocked by your server's network.\n"
                        "If necessary, you may tell Sqreen to connect over a proxy.\n"
                        "Please visit https://docs.sqreen.com/python/configuration/ for more details."
                    )
                    LOGGER.critical(msg)
                    self.unblock_main_thread.set()
                    return

                LOGGER.info("Login success")

                self.runner = get_runner(
                    CONFIG,
                    login_result,
                    session,
                    self.queue,
                    self.runtime_infos,
                    self.observations_queue,
                    self.instrumentation,
                    self.settings,
                )

                # Process the initial commands
                process_initial_commands(login_result, self.runner)

                retry = 3
                while True:
                    try:
                        # if we did not receive instrumentation_enable, try
                        # to get it faster before the MainThread stops waiting.
                        while not self.instrumentation.enabled and retry > 0:
                            retry -= 1
                            self._random_sleep(2.0)
                            self.runner.do_heartbeat()
                        self.unblock_main_thread.set()
                        self.runner.run()
                    except HTTPError:
                        LOGGER.exception(
                            "An HTTP error occurred, restarting runner"
                        )
                        try:
                            session.post_sqreen_exception(
                                RemoteException.from_exc_info().to_dict()
                            )
                        except HTTPError:
                            pass
                        self._random_sleep()
                    else:
                        # If the runner exits normally, return.
                        return
            except InvalidSession:
                LOGGER.info("Relaunching the session because it was dropped by the backend.")
                self._random_sleep()
            except Exception as exc:
                LOGGER.exception("An unexpected exception occurred")

                callback_payload = getattr(exc, "callback_payload", None)
                exception_payload = getattr(exc, "exception_payload", None)
                request_payload = getattr(exc, "request_payload", None)
                remote_exception = RemoteException.from_exc_info(
                    callback_payload=callback_payload,
                    exception_payload=exception_payload,
                    request_payload=request_payload,
                )

                if session is not None and session.is_connected():
                    try:
                        session.post_sqreen_exception(
                            remote_exception.to_dict()
                        )
                        session.logout()
                    except HTTPError:
                        LOGGER.exception("An HTTP error occurred while logout")
                    except Exception:
                        LOGGER.exception("Exception while logout")
                        return
                else:
                    post_app_sqreen_exception(remote_exception.to_dict())

                try:
                    self.instrumentation.deinstrument_all()
                except Exception:
                    # We did not managed to remove instrumentation, state is unclear:
                    # terminate thread
                    LOGGER.exception("Exception while trying to clean-up")
                    return

                self._random_sleep()

    def quick_exit(self):
        """Check for early exit."""
        if os.environ.get("SQREEN_SKIP_LOGOUT", False):
            return True
        # uWSGI 2.0.15 may segfault upon exiting.
        # See https://github.com/unbit/uwsgi/issues/1651.
        uwsgi_vers = uwsgi_version_info()
        if uwsgi_vers and uwsgi_vers >= (2, 0, 15):
            return True
        return self.settings.get_debug_flag() or debug.detect_debug_mode()

    def start(self):
        """Start the runner thread."""
        atexit.register(self.graceful_stop)
        return super(RunnerThread, self).start()

    def graceful_stop(self, force_quick_exit=False):
        """Gracefully stop the runner thread and wait for its termination."""
        self.queue.put(RunnerStop)

        if force_quick_exit or self.quick_exit():
            LOGGER.warning("Quick exit, don't logout")
            return

        try:
            self.join(GRACEFUL_TIMEOUT)
        except RuntimeError:
            logger = getLogger(__name__)
            logger.warning(GRACEFUL_FAIL_MSG, GRACEFUL_TIMEOUT)
        else:
            if self.isAlive():
                logger = getLogger(__name__)
                logger.warning(GRACEFUL_FAIL_MSG, GRACEFUL_TIMEOUT)

    def replace(self, **kwargs):
        """Create a new runner thread instance."""
        nkwargs = dict(
            queue=self.queue,
            observations_queue=self.observations_queue,
            instrumentation=self.instrumentation,
            settings=self.settings,
        )
        nkwargs.update(kwargs)
        return self.__class__(RuntimeInfos().all(), **nkwargs)

    @classmethod
    def _random_sleep(cls, max_delay=10.0):
        """Sleep for a random duration before trying again."""
        delay = random.uniform(0, max_delay)
        LOGGER.info("Sleeping %0.2fs before retry", delay)
        time.sleep(delay)
