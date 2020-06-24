from pathlib import Path

with open(Path(__file__).parent.parent.joinpath("VERSION")) as f:
    __version__ = f.readline()

# Importing modules from this repository
from _0_wrappers import backtest_visualizer


if __name__ == '__main__':
    raise ImportError(
        "This module is not supposed to be called directly."
        "Please import the functions that you need and execute these imported"
        "functions."
    )
