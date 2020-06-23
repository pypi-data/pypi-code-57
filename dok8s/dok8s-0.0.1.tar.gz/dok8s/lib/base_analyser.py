"""base_analyser
"""
import time
from typing import Any


class BaseAnalyser:
    """BaseAnalyser
    """

    def __init__(self):
        self._name = ""
        self._directory = None
        self._output = ""

    @property
    def name(self) -> str:
        """Getter for name attribute.

        If no name is set, use the module's name.

        Returns:
            The value of the name attribute.
        """
        if "".__eq__(self._name):
            return self.__module__.split(".")[-1].replace("_", "-")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Setter for name attribute.

        Args:
            value: The value to set the name attribute.
        """
        self._name = value

    @property
    def directory(self) -> str:
        """Getter for directory attribute.

        Returns:
            The value of the directory attribute.
        """
        return self._directory

    @directory.setter
    def directory(self, value: Any) -> None:
        """Setter for directory attribute.

        Args:
            value: The value to set the directory attribute.
        """
        self._directory = value

    @property
    def output(self) -> str:
        """Getter for output attribute.

        If no output is set, use a datetime stamp.

        Returns:
            The value of the output attribute.
        """
        if "".__eq__(self._output):
            return time.strftime("%Y%m%d-%H%M%S")
        return self._output

    @output.setter
    def output(self, value: str) -> None:
        """Setter for output attribute.

        Args:
            value: The value to set the output attribute.
        """
        self._output = value

    def _parse_data(self) -> Any:
        """Parsing function to construct data.

        Raises:
            NotImplementedError: If this method is used but not
                defined in the subcommand class.
        """
        raise NotImplementedError(
            f"Private Method: _parse_data is undefined for analyser {self.name}"
        )

    def analyse(self):
        """The lib entrypoint command.

        Raises:
            NotImplementedError: If this method is used but not
                defined in the subcommand class.
        """
        raise NotImplementedError(
            f"Method: analyse is undefined for analyser {self.name}"
        )
