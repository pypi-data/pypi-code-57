from contextlib import contextmanager


@contextmanager
def auto_remove(removable):
    try:
        yield removable
    finally:
        removable.remove(force=True)

def progress_gen(bp, iter: str):
    for chunk in iter:
        yield chunk
        bp()
