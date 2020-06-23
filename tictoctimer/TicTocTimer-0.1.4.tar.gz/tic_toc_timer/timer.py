from datetime import datetime, timedelta


class TicTocTimer(object):
    _timestamp_map: dict = None

    def __init__(self):
        """Create a new timer object, with its own collection of tic/toc
        name lables. To use the global timer you can import tic/toc methods.
        """
        super().__init__()
        self._timestamp_map = dict()

    def tic(self, name: str = "global") -> datetime:
        """Start measuring time under the specified name label.

        Args:
            name (str, optional): The label to measure time under. Defaults to "global".

        Returns:
            datetime: The time where we started measuring.
        """
        ts = datetime.now()
        self._timestamp_map[name] = ts
        return ts

    def toc(self, name: str = "global") -> timedelta:
        """Return the time difference between the current
        time and the last call to tic, under the specified name label.

        Args:
            name (str, optional): The label to measure time under. Defaults to "global".

        Returns:
            timedelta: The time difference since the last call to tic, or None.
        """
        if name not in self._timestamp_map:
            return None
        return datetime.now() - self._timestamp_map[name]


GLOBAL_TIMER = TicTocTimer()


def tic(name: str = "global") -> datetime:
    """Using the global timer, start measuring time under the specified name label.

    Args:
        name (str, optional): The label to measure time under. Defaults to "global".

    Returns:
        datetime: The time where we started measuring.
    """
    return GLOBAL_TIMER.tic(name)


def toc(name: str = "global") -> timedelta:
    """Using the global timer, return the time difference between the current
    time and the last call to tic, under the specified name label.

    Args:
        name (str, optional): The label to measure time under. Defaults to "global".

    Returns:
        timedelta: The time difference since the last call to tic, or None.
    """
    return GLOBAL_TIMER.toc(name)


if __name__ == "__main__":
    import pytest

    pytest.main(["-x", __file__[:-3] + "_test.py"])
