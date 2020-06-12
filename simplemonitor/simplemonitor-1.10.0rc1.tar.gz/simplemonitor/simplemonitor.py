# coding=utf-8
"""Execution logic for SimpleMonitor."""

import copy
import logging
import os
import pickle  # nosec
import signal
import sys
import time
from pathlib import Path
from socket import gethostname
from typing import Any, Dict, List, Optional, Union

from .Alerters.alerter import Alerter
from .Alerters.alerter import all_types as all_alerter_types
from .Alerters.alerter import get_class as get_alerter_class
from .Loggers.logger import Logger
from .Loggers.logger import all_types as all_logger_types
from .Loggers.logger import get_class as get_logger_class
from .Loggers.network import Listener
from .Monitors.monitor import Monitor
from .Monitors.monitor import all_types as all_monitor_types
from .Monitors.monitor import get_class as get_monitor_class
from .util import get_config_dict
from .util.envconfig import EnvironmentAwareConfigParser

module_logger = logging.getLogger("simplemonitor")


class SimpleMonitor:
    """A fairly simple monitor."""

    def __init__(
        self,
        config_file: Union[str, Path],
        *,
        hup_file: Optional[Path] = None,
        no_network: bool = False,
        max_loops: int = -1,
        heartbeat: bool = True,
        one_shot: bool = False
    ) -> None:
        """Main class turn on."""
        if isinstance(config_file, str):
            self._config_file = Path(config_file)
        elif isinstance(config_file, Path):
            self._config_file = config_file
        else:
            raise ValueError("config_file must be str or Path")

        self.monitors = {}  # type: Dict[str, Monitor]
        self.failed = []  # type: List[str]
        self.still_failing = []  # type: List[str]
        self.skipped = []  # type: List[str]
        self.warning = []  # type: List[str]
        self.remote_monitors = {}  # type: Dict[str, Dict[str, Monitor]]

        self.loggers = {}  # type: Dict[str, Logger]
        self.alerters = {}  # type: Dict[str, Alerter]

        self._hup_file = hup_file
        self._need_hup = False
        self._hup_timestamp = None  # type: Optional[float]
        self._no_network = no_network
        self._remote_listening_thread = None  # type: Optional[Listener]
        self._max_loops = max_loops
        self.heartbeat = heartbeat
        self.one_shot = one_shot
        self.pidfile = None  # type: Optional[str]

        self._setup_signals()
        self._load_config()

    def _load_config(self) -> None:
        """Load config, monitors, alerters and loggers."""

        config = EnvironmentAwareConfigParser()
        if not self._config_file.exists():
            raise RuntimeError(
                "Configuration file {} does not exist".format(self._config_file)
            )
        config.read(self._config_file)

        self._allow_pickle = config.getboolean("monitor", "allow_pickle", fallback=True)
        self.interval = config.getint("monitor", "interval")
        self.pidfile = config.get("monitor", "pidfile", fallback=None)
        hup_file = config.get("monitor", "hup_file", fallback=None)
        if hup_file is not None:
            self._hup_file = Path(hup_file)
            module_logger.info(
                "Watching modification time of %s; increase it to trigger a config reload",
                hup_file,
            )
            self._check_hup_file()

        if (
            not self._no_network
            and config.get("monitor", "remote", fallback="0") == "1"
        ):
            self._network = True
            self._remote_port = int(config.get("monitor", "remote_port"))
            self._network_key = config.get("monitor", "key", fallback=None)
            self._network_bind_host = config.get("monitor", "bind_host", fallback="")
        else:
            self._network = False

        monitors_file = Path(config.get("monitor", "monitors", fallback="monitors.ini"))
        self._load_monitors(monitors_file)
        count = self.count_monitors()
        if count == 0:
            module_logger.critical("No monitors loaded :(")
        self._load_loggers(config)
        self._load_alerters(config)
        if not self._verify_dependencies():
            raise RuntimeError("Broken dependency configuration")
        if not self.verify_alerting():
            module_logger.critical("No alerters defined and no remote logger found")
        if self._network:
            self._start_network_thread()

    def _start_network_thread(self) -> None:
        if self._network:
            if not self._allow_pickle:
                allowing_pickle = "not "
            else:
                allowing_pickle = ""
            module_logger.info(
                "Starting remote listener thread (%sallowing pickle data)",
                allowing_pickle,
            )
            self._remote_listening_thread = Listener(
                self,
                self._remote_port,
                self._network_key,
                allow_pickle=self._allow_pickle,
                bind_host=self._network_bind_host,
            )
            self._remote_listening_thread.daemon = True
            self._remote_listening_thread.start()
        else:
            if self._remote_listening_thread:
                self._remote_listening_thread.running = False

    def _stop_network_thread(self) -> None:
        if self._network and self._remote_listening_thread:
            self._remote_listening_thread.running = False
            module_logger.info("Waiting for listener thread to exit")
            self._remote_listening_thread.join(0)

    def _load_monitors(self, filename: Union[Path, str]) -> None:
        """Load all the monitors from the config file."""
        if isinstance(filename, str):
            filename = Path(filename)
        elif not isinstance(filename, Path):
            raise ValueError("filename must be str or Path")
        if not filename.exists():
            raise RuntimeError(
                "Monitors config file {} does not exist".format(filename)
            )
        module_logger.info("Loading monitor config from %s", filename)
        config = EnvironmentAwareConfigParser()
        config.read(filename)
        monitors = config.sections()
        if "defaults" in monitors:
            default_config = get_config_dict(config, "defaults")
            monitors.remove("defaults")
        else:
            default_config = {}

        myhostname = gethostname().lower()

        module_logger.info("=== Loading monitors")
        for this_monitor in monitors:
            if config.has_option(this_monitor, "runon"):
                if myhostname != config.get(this_monitor, "runon").lower():
                    module_logger.warning(
                        "Ignoring monitor %s because it's only for host %s",
                        this_monitor,
                        config.get(this_monitor, "runon"),
                    )
                    continue
            monitor_type = config.get(this_monitor, "type")
            new_monitor = None
            config_options = default_config.copy()
            config_options.update(get_config_dict(config, this_monitor))
            if self.has_monitor(this_monitor):
                if self.monitors[this_monitor].monitor_type == config_options["type"]:
                    module_logger.info(
                        "Updating configuration for monitor %s", this_monitor
                    )
                    self.update_monitor_config(this_monitor, config_options)
                else:
                    module_logger.error(
                        "Cannot update monitor %s from type %s to type %s. "
                        "Keeping original config for this monitor.",
                        this_monitor,
                        self.monitors[this_monitor].monitor_type,
                        config_options["type"],
                    )
                continue

            try:
                cls = get_monitor_class(monitor_type)
            except KeyError:
                module_logger.error(
                    "Unknown monitor type %s; valid types are: %s",
                    monitor_type,
                    ", ".join(all_monitor_types()),
                )
                continue
            new_monitor = cls(this_monitor, config_options)
            # new_monitor.set_mon_refs(m)

            module_logger.info(
                "Adding %s monitor %s: %s", monitor_type, this_monitor, new_monitor
            )
            self.add_monitor(this_monitor, new_monitor)

        for monitor in self.monitors.values():
            monitor.set_mon_refs(self.monitors)
            monitor.post_config_setup()
        self.prune_monitors(monitors)
        module_logger.info("--- Loaded %d monitors", self.count_monitors())

    def _load_loggers(self, config: EnvironmentAwareConfigParser) -> None:
        """Load the loggers listed in the config object."""

        if config.has_option("reporting", "loggers"):
            loggers = config.get("reporting", "loggers").split(",")
        else:
            loggers = []

        module_logger.info("=== Loading loggers")
        for config_logger in loggers:
            logger_type = config.get(config_logger, "type")
            config_options = get_config_dict(config, config_logger)
            config_options["_name"] = config_logger
            if self.has_logger(config_logger):
                if self.loggers[config_logger].logger_type == config_options["type"]:
                    module_logger.info(
                        "Updating configuration for logger %s", config_logger
                    )
                    self.update_logger_config(config_logger, config_options)
                else:
                    module_logger.error(
                        "Cannot update logger %s from type %s to type %s. "
                        "Keeping original config for this logger.",
                        config_logger,
                        self.loggers[config_logger].logger_type,
                        config_options["type"],
                    )
                continue
            try:
                logger_cls = get_logger_class(logger_type)
            except KeyError:
                module_logger.error(
                    "Unknown logger type %s; valid types are: %s",
                    logger_type,
                    ", ".join(all_logger_types()),
                )
                continue
            new_logger = logger_cls(config_options)  # type: Logger
            new_logger.set_global_info(
                {"interval": config.getint("monitor", "interval")}
            )
            module_logger.info(
                "Adding %s logger %s: %s", logger_type, config_logger, new_logger
            )
            self.add_logger(config_logger, new_logger)
            del new_logger
        self.prune_loggers(loggers)
        module_logger.info("--- Loaded %d loggers", len(self.loggers))

    def _load_alerters(self, config: EnvironmentAwareConfigParser) -> None:
        """Load the alerters listed in the config object."""
        if config.has_option("reporting", "alerters"):
            alerters = config.get("reporting", "alerters").split(",")
        else:
            alerters = []

        module_logger.info("=== Loading alerters")
        for this_alerter in alerters:
            alerter_type = config.get(this_alerter, "type")
            config_options = get_config_dict(config, this_alerter)
            if self.has_alerter(this_alerter):
                if self.alerters[this_alerter].alerter_type == config_options["type"]:
                    module_logger.info(
                        "Updating configuration for alerter %s", this_alerter
                    )
                    self.update_alerter_config(this_alerter, config_options)
                else:
                    module_logger.error(
                        "Cannot update alerter %s from type %s to type %s. "
                        "Keeping original config for this alerter.",
                        this_alerter,
                        self.alerters[this_alerter].alerter_type,
                        config_options["type"],
                    )
                continue
            try:
                alerter_cls = get_alerter_class(alerter_type)
            except KeyError:
                module_logger.error(
                    "Unknown alerter type %s; valid types are: %s",
                    alerter_type,
                    ", ".join(all_alerter_types()),
                )
                continue
            new_alerter = alerter_cls(config_options)
            module_logger.info("Adding %s alerter %s", alerter_type, this_alerter)
            new_alerter.name = this_alerter
            self.add_alerter(this_alerter, new_alerter)
            del new_alerter
        self.prune_alerters(alerters)
        module_logger.info("--- Loaded %d alerters", len(self.alerters))

    def _setup_signals(self) -> None:
        """Set up the SIGHUP handler."""
        _message = (
            "Unable to trap SIGHUP... maybe it doesn't exist on this platform. "
            "Set 'hup_file' in config and touch that file to trigger a config reload."
        )
        try:
            signal.signal(signal.SIGHUP, self._handle_sighup)
        except ValueError:  # pragma: no cover
            module_logger.warning(_message)
        except AttributeError:  # pragma: no cover
            module_logger.warning(_message)

    def _handle_sighup(self, *_: Any) -> None:
        """Receive SIGHUP and process it."""
        module_logger.warning("Received SIGHUP")
        self._need_hup = True

    def _check_hup_file(self) -> bool:
        """Check a file's timestamp, and if it's newer than last time, treat it
        the same as receiving SIGHUP so that a reload is triggered. This allows
        config reloading on platforms which don't support the signal (i.e.
        Windows)"""
        if self._hup_file is None:
            return False
        try:
            statinfo = os.stat(self._hup_file)
        except IOError:
            module_logger.debug(
                "Could not call stat() on path %s for file-based HUP", self._hup_file
            )
            return False
        modification_time = statinfo.st_mtime
        if self._hup_timestamp is None:
            self._hup_timestamp = modification_time
            return True
        if modification_time > self._hup_timestamp:
            self._hup_timestamp = modification_time
            return True
        return False

    def _create_pid_file(self) -> None:
        if self.pidfile:
            my_pid = os.getpid()
            try:
                with open(self.pidfile, "w") as file_handle:
                    file_handle.write("%d\n" % my_pid)
            except IOError:
                module_logger.error("Couldn't write to pidfile!")
                self.pidfile = None

    def _remove_pid_file(self) -> None:
        if self.pidfile:
            try:
                os.unlink(self.pidfile)
            except OSError:
                module_logger.error("Couldn't remove pidfile!")

    def add_monitor(self, name: str, monitor: Monitor) -> None:
        """Add a monitor."""
        self.monitors[name] = monitor

    def update_monitor_config(self, name: str, config_options: dict) -> None:
        """Update the configuration for a monitor."""
        self.monitors[name].__init__(name, config_options)  # type: ignore

    def update_logger_config(self, name: str, config_options: dict) -> None:
        """Update the configration for a logger."""
        self.loggers[name].__init__(config_options)  # type: ignore

    def update_alerter_config(self, name: str, config_options: dict) -> None:
        """Update the configuration for an alerter."""
        self.alerters[name].__init__(config_options)  # type: ignore

    def has_monitor(self, monitor: str) -> bool:
        """Check if a montitor is known."""
        return monitor in self.monitors.keys()

    def has_logger(self, logger: str) -> bool:
        """Check if a logger is known."""
        return logger in self.loggers.keys()

    def has_alerter(self, alerter: str) -> bool:
        """Check if an alerter is known."""
        return alerter in self.alerters.keys()

    def reset_monitors(self) -> None:
        """Clear all all monitors' dependency info back to default."""
        for key in list(self.monitors.keys()):
            self.monitors[key].reset_dependencies()

    def _verify_dependencies(self) -> bool:
        """Check if all monitors have valid dependencies."""
        ok = True
        monitors = self.monitors.keys()
        for key, monitor in self.monitors.items():
            for dependency in monitor.dependencies:
                if dependency not in monitors:
                    module_logger.critical(
                        "Configuration error: dependency %s of monitor %s is not defined!",
                        dependency,
                        key,
                    )
                    ok = False
        return ok

    def verify_alerting(self) -> bool:
        """Sanity check the configuration to see if we have at least an
        alerter, or network logging."""
        sane = True
        if len(self.alerters) == 0:
            for _, logger in self.loggers.items():
                if logger.logger_type == "network":
                    break
            else:
                sane = False
        return sane

    def sort_joblist(self, joblist: List[str]) -> List[str]:
        """Order a list of monitors so that compound monitors are at the end"""
        new_list = []  # type: List[str]
        late_list = []  # type: List[str]
        for monitor in joblist:
            if self.monitors[monitor].monitor_type in ["compound"]:
                late_list.append(monitor)
            else:
                new_list.append(monitor)
        new_list.extend(late_list)
        return new_list

    def run_tests(self) -> None:
        """Run the tests for all the monitors."""
        self.reset_monitors()

        joblist = list(self.monitors.keys())
        joblist = self.sort_joblist(joblist)
        failed = []  # type: List[str]

        not_run = False

        while joblist:
            new_joblist = []  # type: List[str]
            module_logger.debug("Starting loop with joblist %s", joblist)
            for monitor in joblist:
                module_logger.debug("Trying monitor: %s", monitor)
                if self.monitors[monitor].remaining_dependencies:
                    # this monitor has outstanding deps, put it on the new joblist for next loop
                    new_joblist.append(monitor)
                    module_logger.debug(
                        "Added %s to new joblist, is now %s", monitor, new_joblist
                    )
                    for dep in self.monitors[monitor].remaining_dependencies:
                        module_logger.debug(
                            "considering %s's dependency %s (failed monitors: %s)",
                            monitor,
                            dep,
                            failed,
                        )
                        if dep in failed:
                            # oh wait, actually one of its deps failed, so
                            # we'll never be able to run it
                            module_logger.info(
                                "Doesn't look like %s worked, skipping %s", dep, monitor
                            )
                            failed.append(monitor)
                            self.monitors[monitor].record_skip(dep)
                            try:
                                new_joblist.remove(monitor)
                            except ValueError:
                                module_logger.exception(
                                    "Exception caught while trying to remove monitor %s "
                                    "with failed deps from new joblist.",
                                    monitor,
                                )
                                module_logger.debug(
                                    "new_joblist is currently: %s", new_joblist
                                )
                            break
                    continue
                try:
                    if self.monitors[monitor].should_run():
                        not_run = False
                        start_time = time.time()
                        self.monitors[monitor].run_test()
                        end_time = time.time()
                        self.monitors[monitor].last_run_duration = int(
                            end_time - start_time
                        )
                    else:
                        not_run = True
                        self.monitors[monitor].record_skip(None)
                        module_logger.info("Not run: %s", monitor)
                except Exception as exception:
                    module_logger.exception(
                        "Monitor %s threw exception during run_test()", monitor
                    )
                    self.monitors[monitor].record_fail(
                        "Unhandled exception: {}".format(exception)
                    )
                if self.monitors[monitor].error_count > 0:
                    if self.monitors[monitor].virtual_fail_count() == 0:
                        module_logger.warning(
                            "monitor failed but within tolerance: %s", monitor
                        )
                    else:
                        module_logger.error(
                            "monitor failed: %s (%s)",
                            monitor,
                            self.monitors[monitor].last_result,
                        )
                    failed.append(monitor)
                else:
                    if not not_run:
                        module_logger.info("monitor passed: %s", monitor)
                    for monitor2 in joblist:
                        self.monitors[monitor2].dependency_succeeded(monitor)
            joblist = copy.copy(new_joblist)

    def log_result(self, logger: Logger) -> None:
        """Use the given logger object to log our state."""
        logger.check_dependencies(self.failed + self.still_failing + self.skipped)
        with logger:
            for key, monitor in self.monitors.items():
                if monitor.group in logger.groups:
                    logger.save_result2(key, monitor)
                else:
                    module_logger.debug(
                        "not logging for %s due to group mismatch (monitor in group %s, "
                        "logger has groups %s",
                        key,
                        monitor.group,
                        logger.groups,
                    )
            try:
                for host_monitors in self.remote_monitors.values():
                    for (name, monitor) in host_monitors.items():
                        logger.save_result2(name, monitor)
            except Exception:  # pragma: no cover
                module_logger.exception("exception while logging remote monitors")

    def do_alert(self, alerter: Alerter) -> None:
        """Use the given alerter object to send an alert, if needed."""
        alerter.check_dependencies(self.failed + self.still_failing + self.skipped)
        for key in list(self.monitors.keys()):
            this_monitor = self.monitors[key]  # type: Monitor
            # Don't generate alerts for monitors which want it done remotely
            if this_monitor.remote_alerting:
                module_logger.debug(
                    "skipping alert for monitor %s as it wants remote alerting", key
                )
                continue
            try:
                if this_monitor.group in alerter.groups:
                    # Only notifications for services that have it enabled
                    if this_monitor.notify:
                        module_logger.debug("notifying alerter %s", alerter.name)
                        alerter.send_alert(key, self.monitors[key])
                    else:
                        module_logger.warning(
                            "monitor %s has notifications disabled", key
                        )
                else:
                    module_logger.info(
                        "skipping alerter %s as monitor %s is not in group %s",
                        alerter.name,
                        this_monitor.name,
                        alerter.groups,
                    )
            except Exception:  # pragma: no cover
                module_logger.exception("exception caught while alerting for %s", key)
        for host_monitors in self.remote_monitors.values():
            for (name, monitor) in host_monitors.items():
                try:
                    if monitor.remote_alerting:
                        alerter.send_alert(name, monitor)
                    else:
                        module_logger.debug(
                            "not alerting for monitor %s as it doesn't want remote alerts",
                            name,
                        )
                except Exception:  # pragma: no cover
                    module_logger.exception(
                        "exception caught while alerting for remote monitor %s", name
                    )

    def count_monitors(self) -> int:
        """Gets the number of monitors we have defined."""
        return len(self.monitors)

    def add_alerter(self, name: str, alerter: Alerter) -> None:
        """Add an alerter."""
        if isinstance(alerter, Alerter):
            self.alerters[name] = alerter
        else:
            module_logger.critical(
                "Failed to add alerter because it is not the right type"
            )

    def add_logger(self, name: str, logger: Logger) -> None:
        """Add a logger."""
        if isinstance(logger, Logger):
            self.loggers[name] = logger
        else:
            module_logger.critical(
                "Failed to add logger because it is not the right type"
            )

    def prune_monitors(self, retain: List[str]) -> None:
        """Remove monitors which are in our list but not in the list passed to us.

        Used to tidy up after a config reload (which may have removed monitors)"""
        delete_list = []
        for monitor in self.monitors:
            if monitor not in retain:
                module_logger.info("Removing monitor %s", monitor)
                delete_list.append(monitor)
        for monitor in delete_list:
            del self.monitors[monitor]
        if not self._verify_dependencies():
            module_logger.critical(
                "Broken dependencies after pruning monitors, aborting!"
            )
            sys.exit(1)

    def prune_alerters(self, retain: List[str]) -> None:
        """Remove alerters which are in our list but not in the list passed to us.

        Used to tidy up after a config reload (which may have removed alerters)"""
        delete_list = []
        for alerter in self.alerters:
            if alerter not in retain:
                module_logger.info("Removing alerter %s", alerter)
                delete_list.append(alerter)
        for alerter in delete_list:
            del self.alerters[alerter]

    def prune_loggers(self, retain: List[str]) -> None:
        """Remove loggers which are in our list but not in the list passed to us.

        Used to tidy up after a config reload (which may have removed logger)"""
        delete_list = []
        for logger in self.loggers:
            if logger not in retain:
                module_logger.info("Removing logger %s", logger)
                delete_list.append(logger)
        for logger in delete_list:
            del self.loggers[logger]

    def do_alerts(self) -> None:
        """Run the alert process for each alerter."""
        for alerter in self.alerters.values():
            self.do_alert(alerter)

    def do_recovery(self) -> None:
        """Attempt recovery for each monitor."""
        for monitor in self.monitors.values():
            monitor.attempt_recover()

    def do_recovered(self) -> None:
        """Run the recovered action for each monitor."""
        for monitor in self.monitors.values():
            monitor.run_recovered()

    def hup_loggers(self) -> None:
        """Inform each logger they need to HUP."""
        for logger in self.loggers.values():
            logger.hup()

    def do_logs(self) -> None:
        """Log result for each logger."""
        for logger in self.loggers.values():
            self.log_result(logger)

    def update_remote_monitor(self, data: Any, hostname: str) -> None:
        """Process a list of monitors received from a remote host."""
        seen_monitors = []  # type: List[str]
        if hostname not in self.remote_monitors:
            self.remote_monitors[hostname] = {}
        for (name, state) in data.items():
            module_logger.info("updating remote monitor %s", name)
            if isinstance(state, dict):
                try:
                    remote_monitor = get_monitor_class(
                        state["cls_type"]
                    ).from_python_dict(state["data"])
                    self.remote_monitors[hostname][name] = remote_monitor
                    seen_monitors.append(name)
                except KeyError:
                    module_logger.exception(
                        "Could not add remote monitor from host %s; "
                        "possibly a monitor type we don't know?",
                        hostname,
                    )
            elif self._allow_pickle:
                # Fallback for old remote monitors
                try:
                    remote_monitor = pickle.loads(state)  # nosec
                except pickle.UnpicklingError:
                    module_logger.critical("Could not unpickle monitor %s", name)
                else:
                    self.remote_monitors[hostname][name] = remote_monitor
                    seen_monitors.append(name)
            else:
                module_logger.critical(
                    "Could not deserialize state of monitor %s. "
                    "If the remote host uses an old version of "
                    "simplemonitor, you need to set allow_pickle = true "
                    "in the [monitor] section.",
                    name,
                )
        self._trim_remote_monitors(hostname, seen_monitors)

    def _trim_remote_monitors(self, hostname: str, seen_monitors: List[str]) -> None:
        """Remove remote monitors for a host which aren't in the given list."""
        host_monitors = self.remote_monitors[hostname]
        forget_monitors = []
        for name in host_monitors.keys():
            if name not in seen_monitors:
                module_logger.info(
                    "forgetting remote monitor %s from host %s", name, hostname
                )
                forget_monitors.append(name)
        for name in forget_monitors:
            del self.remote_monitors[hostname][name]

    def run_loop(self) -> None:
        """Run the complete monitor loop once."""
        module_logger.debug("Running tests")
        self.run_tests()
        module_logger.debug("Running recovery")
        self.do_recovery()
        self.do_recovered()
        module_logger.debug("Running alerts")
        self.do_alerts()
        module_logger.debug("Running logs")
        self.do_logs()
        module_logger.debug("Loop complete")

    def run(self) -> None:
        self._create_pid_file()
        module_logger.info(
            "=== Starting... (loop runs every %ds) Hit ^C to stop", self.interval
        )
        loop = True
        loops = self._max_loops
        heartbeat = True
        while loop:
            try:
                if loops > 0:
                    loops -= 1
                    if loops == 0:
                        module_logger.warning(
                            "Ran out of loop counter, will stop after this one"
                        )
                        loop = False
                if self._need_hup or self._check_hup_file():
                    try:
                        module_logger.warning("Reloading configuration")
                        self._load_config()
                        self.hup_loggers()
                        self._need_hup = False
                    except Exception:
                        module_logger.exception("Error while reloading configuration")
                        sys.exit(1)
                self.run_loop()

                if (
                    module_logger.level in ["error", "critical", "warn"]
                    and self.heartbeat
                ):
                    heartbeat = not heartbeat
                    if heartbeat:
                        sys.stdout.write(".")
                        sys.stdout.flush()
            except KeyboardInterrupt:
                module_logger.info("Received ^C")
                loop = False
            except Exception:
                module_logger.exception("Caught unhandled exception during main loop")
            if loop and self._network:
                if (
                    self._remote_listening_thread
                    and not self._remote_listening_thread.is_alive()
                ):
                    module_logger.error("Listener thread died :(")
                    self._start_network_thread()
            if self.one_shot:
                break

            try:
                if loop:
                    time.sleep(self.interval)
            except Exception:
                module_logger.info("Quitting")
                loop = False

        self._stop_network_thread()
        self._remove_pid_file()
