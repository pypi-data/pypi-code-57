from contextlib import contextmanager
import sys
from typing import List


@contextmanager
def augment_syspath(paths: List[str]):
    old_path = sys.path.copy()
    sys.path += paths
    try:
        yield
    finally:
        sys.path = old_path
