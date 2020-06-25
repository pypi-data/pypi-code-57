import pickle
from typing import Any


def load_pickle(file_path: str) -> Any:
    with open(file_path, "rb") as fp:
        return pickle.load(fp)
