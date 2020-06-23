"""Convenience classes/functions for Driverless AI Python client."""

import abc
import ast
import enum
import sys
import time
from typing import Any, IO, List, Sequence, Union

import tabulate

from driverlessai import _core


class GUILink(str):
    """Renders clickable link in notebooks but otherwise behaves the same as ``str``."""

    def _repr_html_(self) -> str:
        link = self.__str__()
        html = (
            "<pre>"
            f"<a href='{link}' rel='noopener noreferrer' target='_blank'>{link}</a>"
            "</pre>"
        )
        return html


class JobStatus(enum.IntEnum):
    FINISHING = -2
    RUNNING = -1
    COMPLETE = 0
    CANCELLED = 1
    FAILED = 2
    ABORTED = 3
    ABORTED_RESTART = 4

    def __init__(self, status: int) -> None:
        self.message = {
            -2: "Finishing",
            -1: "Running",
            0: "Complete",
            1: "Cancelled",
            2: "Failed",
            3: "Aborted",
            4: "Aborted (by restart)",
        }[status]


class ServerJob(abc.ABC):
    """Monitor a job on the Driverless AI server.

    Attributes:
        key: unique ID
    """

    def __init__(self, client: "_core.Client", key: str) -> None:
        self._client = client
        self._info = None  # type: Any
        self.key = key
        self._update()

    def is_complete(self) -> bool:
        """Return True if job completed successfully."""
        return is_server_job_complete(self._status())

    def is_running(self) -> bool:
        """Return True if job is running or finishing."""
        return is_server_job_running(self._status())

    def _status(self) -> JobStatus:
        self._update()
        return JobStatus(self._info.status)

    @abc.abstractmethod
    def _update(self) -> None:
        """Updates the self._info variable with info from server."""
        raise NotImplementedError

    def _wait(self, silent: bool = False) -> None:
        status_update = StatusUpdate()
        while self.is_running():
            time.sleep(1)
            if not silent:
                status_update.display(self.status(verbose=2))
        status_update.end()
        if not self.is_complete():
            raise RuntimeError(
                self._client._backend._format_server_error(self._info.error)
            )

    @abc.abstractmethod
    def result(self, silent: bool = False) -> Any:
        """Wait for job to complete.

        Args:
            silent: if True, don't display status updates
        """
        raise NotImplementedError

    def status(self, verbose: int = 0) -> str:
        """Return job status string.

        Args:
            verbose:
                - 0: short description
                - 1: short description with progress percentage
                - 2: detailed description with progress percentage
        """
        status = self._status()
        if verbose == 1:
            return f"{status.message} {self._info.progress:.2%}"
        if verbose == 2:
            if status == JobStatus.FAILED:
                message = self._info.error
            else:
                message = self._info.message.split("\n")[0]
            return f"{status.message} {self._info.progress:.2%} - {message}"
        return status.message


class ServerJobs:
    """Monitor multiple jobs on the Driverless AI server.

    Attributes:
        jobs: list of ServerJob objects
    """

    def __init__(self, client: "_core.Client", jobs: Sequence["ServerJob"]) -> None:
        self._client = client
        self.jobs = jobs

    def is_complete(self) -> bool:
        """Return True if all jobs completed successfully."""
        for job in self.jobs:
            if not job.is_complete():
                return False
        return True

    def is_running(self) -> bool:
        """Return True if one or more jobs is running or finishing."""
        for job in self.jobs:
            if job.is_running():
                return True
        return False

    def result(self, silent: bool = False) -> Any:
        """Wait for all jobs to complete.

        Args:
            silent: if True, don't display status updates
        """
        return [job.result(silent) for job in self.jobs]

    def status(self, verbose: int = 0) -> List[str]:
        """Returns list of job status strings.

        Args:
            verbose:
                - 0: short description
                - 1: short description with progress percentage
                - 2: detailed description with progress percentage
        """
        return [job.status(verbose) for job in self.jobs]


class StatusUpdate:
    def __init__(self, stdout: IO = sys.stdout) -> None:
        self._needs_end = False
        self._prev_message_len = 0
        self.stdout = stdout

    def _overwrite_line(self, old_line_len: int, new_line: str) -> None:
        """Delete a printed line and write another line in its place.

        Args:
            old_line_len: length of line to be overwritten
            new_line: line to be printed
        """
        self.stdout.write("\r")
        self.stdout.write(" " * old_line_len)
        self.stdout.write("\r")
        self.stdout.write(new_line)
        self.stdout.flush()

    def display(self, message: str) -> None:
        """Display status message on the current line."""
        self._overwrite_line(self._prev_message_len, message)
        self._prev_message_len = len(message)
        self._needs_end = True

    def end(self) -> None:
        """Move to new line."""
        if self._needs_end:
            self.stdout.write("\n")


class Table:
    """Table that pretty prints.

    Attributes:
        data (List[List[Any]]): table data
        headers (List[str]): table headers
    """

    def __init__(self, data: List[List[Any]], headers: List[str]) -> None:
        self.data = data
        self.headers = headers

    def __str__(self) -> str:
        return tabulate.tabulate(self.data, headers=self.headers, tablefmt="presto")

    def _repr_html_(self) -> str:
        return tabulate.tabulate(self.data, headers=self.headers, tablefmt="html")


def is_number(string: str) -> bool:
    try:
        float(string)
        return True
    except Exception:
        return False


def is_server_job_complete(server_job_status: Union[int, JobStatus]) -> bool:
    return server_job_status == JobStatus.COMPLETE


def is_server_job_running(server_job_status: Union[int, JobStatus]) -> bool:
    return server_job_status in [JobStatus.FINISHING, JobStatus.RUNNING]


def try_eval(value: Any) -> Any:
    try:
        return ast.literal_eval(value)
    except Exception:
        return value
