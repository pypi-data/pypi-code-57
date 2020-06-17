"""Expose a wrapper class to manage a server subprocess."""

import random
import re
import string
import time
from pathlib import Path
from subprocess import STDOUT, Popen  # nosec
from typing import Any, Collection, Optional, Tuple

from ._java_utils import DEFAULT_JAR_PATH, get_java_path
from ._path_utils import get_atoti_home
from ._type_utils import Port

_LOGS_ROOT = get_atoti_home() / "logs"


def _create_log_directory() -> Path:
    """Create the directory that will contain the log file."""
    # Generate random string for unique file name.
    random_string = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    log_directory = _LOGS_ROOT / f"{str(int(time.time()))}_{random_string}"
    log_directory.mkdir(parents=True)
    return log_directory


class ServerSubprocess:
    """A wrapper class to start and manage an atoti server from Python."""

    def __init__(
        self,
        port: Optional[Port] = None,
        url_pattern: Optional[str] = None,
        max_memory: Optional[str] = None,
        java_args: Optional[Collection[str]] = None,
        **kwargs: Any,
    ):
        """Create and start the subprocess.

        Args:
            port: The port on which the server will be exposed.
            url_pattern: The URL pattern for the server.
            max_memory: The max memory of the process.
            java_args: Additional Java arguments
        """
        self.port = port
        self.url_pattern = url_pattern
        self.max_memory = max_memory
        self.java_args = java_args
        self._log_directory = _create_log_directory()
        (self._process, self.py4j_java_port) = self._start(**kwargs)

    def wait(self) -> None:
        """Wait for the process to terminate.

        This will prevent the Python process to exit unless the Py4J gateway is closed since,
        in that case, the atoti server will stop itself.
        """
        self._process.wait()

    def _start(self, **kwargs: Any) -> Tuple[Popen, Port]:
        """Start the atoti server.

        Returns:
            A tuple containing the server process and the Py4J java port.
        """
        if "jar_path" in kwargs:
            jar = Path(kwargs["jar_path"])
        else:
            jar = DEFAULT_JAR_PATH

        if not jar.exists():
            raise FileNotFoundError(f"""Missing built-in atoti JAR at: "{jar}".""")

        process = self._create_subprocess(jar)

        # Wait for it to start
        try:
            java_port = self._await_start()
        except Exception as ex:
            process.kill()
            raise ex

        # We're done
        return (process, java_port)

    def _create_subprocess(self, jar: Path) -> Popen:
        """Create and start the actual subprocess.

        Args:
            jar: The path to the atoti JAR.

        Returns:
            The created process.
        """
        program_args = [
            get_java_path(),
            "-jar",
        ]

        if self.port:
            program_args.append(f"-Dserver.port={self.port}")

        if self.url_pattern:
            program_args.append(f"-Dserver.url_pattern={self.url_pattern}")

        if self.max_memory:
            program_args.append(f"-Xmx{self.max_memory}")

        if self.java_args:
            for arg in self.java_args:
                program_args.append(f"{arg}")

        program_args.append(str(jar.absolute()))

        # Create and return the subprocess.
        # We allow the user to pass any argument to Java, even dangerous ones
        try:
            process = Popen(
                program_args, stderr=STDOUT, stdout=open(self.logs_path, "wt")
            )  # nosec
        except Exception as ex:
            # Raise an exception containing the logs' path for the user
            raise Exception(
                f"Could not start the session. You can check the logs at {self.logs_path}",
                ex,
            )

        return process

    def _await_start(self) -> Port:
        """Wait for the server to start and return the Py4J Java port."""
        period = 0.25
        timeout = 60
        attempt_count = round(timeout / period)
        # Wait for the process to start and log the Py4J port.
        for _attempt in range(1, attempt_count):  # pylint: disable=unused-variable
            # Look for the started line.
            try:
                for line in open(self.logs_path):
                    regex = "Py4J server started, listening for connections on port (?P<port>[0-9]+)"
                    match = re.search(regex, line.rstrip())
                    if match:
                        # Server should be ready.
                        return Port(int(match.group("port")))
            except FileNotFoundError:
                # The logs file has not yet been created.
                pass

            # The server is not ready yet.
            # Wait for a bit.
            time.sleep(period)

        # The inner loop did not return.
        # This means that the server could not be started correctly.
        raise Exception(
            "Could not start server. " + f"Please check the logs: {self.logs_path}"
        )

    @property
    def logs_path(self) -> Path:
        """Path to subprocess logs file."""
        return self._log_directory / "subprocess.log"
