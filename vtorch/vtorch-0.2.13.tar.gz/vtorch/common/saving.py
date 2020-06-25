import pickle
from typing import Any


def save_pickle(d: Any, file_path: str) -> None:
    with open(file_path, "wb") as fp:
        pickle.dump(d, fp, protocol=pickle.HIGHEST_PROTOCOL)
