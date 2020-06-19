__all__ = ["map_async", "starmap_async"]
__version__ = "1.2"

import importlib
import itertools
import multiprocessing
import multiprocessing.pool as mp
from typing import Sized


# gensim.utils.chunkize_serial
def chunkize_serial(iterable, chunksize):
    """
    Return elements from the iterable in `chunksize`-ed lists. The last returned
    element may be smaller (if length of collection is not divisible by `chunksize`).
    >>> print(list(grouper(range(10), 3)))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    it = iter(iterable)
    while True:
        wrapped_chunk = [list(itertools.islice(it, int(chunksize)))]
        if not wrapped_chunk[0]:
            break
        # memory opt: wrap the chunk and then pop(),
        # to avoid leaving behind a dangling reference
        yield wrapped_chunk.pop()


# gensim.utils.InputQueue
class InputQueue(multiprocessing.Process):

    def __init__(self, q, corpus, chunksize, maxsize):
        super(InputQueue, self).__init__()
        self.q = q
        self.maxsize = maxsize
        self.corpus = corpus
        self.chunksize = chunksize

    def run(self):
        it = iter(self.corpus)
        while True:
            chunk = itertools.islice(it, self.chunksize)
            wrapped_chunk = [list(chunk)]

            if not wrapped_chunk[0]:
                self.q.put(None, block=True)
                break

            try:
                qsize = self.q.qsize()
            except NotImplementedError:
                qsize = '?'
            self.q.put(wrapped_chunk.pop(), block=True)


# gensim.utils.chunkize
def chunkize(corpus, chunksize, maxsize=0):
    """
    Split a stream of values into smaller chunks.
    Each chunk is of length `chunksize`, except the last one which may be smaller.
    A once-only input stream (`corpus` from a generator) is ok, chunking is done
    efficiently via itertools.
    If `maxsize > 1`, don't wait idly in between successive chunk `yields`, but
    rather keep filling a short queue (of size at most `maxsize`) with forthcoming
    chunks in advance. This is realized by starting a separate process, and is
    meant to reduce I/O delays, which can be significant when `corpus` comes
    from a slow medium (like harddisk).
    If `maxsize==0`, don't fool around with parallelism and simply yield the chunksize
    via `chunkize_serial()` (no I/O optimizations).
    >>> for chunk in chunkize(range(10), 4): print(chunk)
    [0, 1, 2, 3]
    [4, 5, 6, 7]
    [8, 9]
    """
    assert chunksize > 0

    if maxsize > 0:
        q = multiprocessing.Queue(maxsize=maxsize)
        worker = InputQueue(q, corpus, chunksize, maxsize=maxsize)
        worker.daemon = True
        worker.start()
        while True:
            chunk = [q.get(block=True)]
            if chunk[0] is None:
                break
            yield chunk.pop()
    else:
        for chunk in chunkize_serial(corpus, chunksize):
            yield chunk


def map_async(func, iterable, processes=None, scale=10, show_progress=False,
              desc=None, starmap=False):
    """
    Apply function `func` on all items in an iterable with multiple processes.

    A pool of processes are dispatched initially, then they are destroyed after the
    job is done.

    Normally, tracking a multi-process progress can cause race conditions, and thus
    it's tricky to implement. A work-around is to chunk the entire sequence into smaller
    manageable pieces, and then apply multi-processing on each chunk piece, allowing
    the progress to be monitored. The chunking algorithm is extracted from `gensim.utils`,
    which was originally developed for various data processing pipelines, such as
    wikipedia preprocessing etc.

    Arguments:
      func: (callable) a function that takes each item in the iterable and returns
        a corresponding transformation
      iterable: (iterator-like object) an object that supports `__iter__`
      processes: (int, optional) number of processes to be dispatched.
        Defaults to the number of cpu cores.
      scale: (int) size of each chunk with respect to the number of processes
        (i.e. chunk_size = scale * processes)
      show_progress: (bool) if enabled, a `tqdm` progress bar will be displayed
        (run `pip install tqdm` if not installed)
      desc: (str, optional) description to be displayed on the progress bar.
      starmap: (bool) whether to use `starmap` instead of `map`.

    Returns:
      A list of transformed items (as long as the input iterable)

    Example:
      >>> from map_async import map_async
      >>> square = lambda x: x ** 2
      >>> map_async(square, range(10))
      [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
      >>> map_async(square, range(10), show_progress=True)
      100%|█████████████████████████████████████████| 1/1 [00:00<00:00,  9.79it/s]
      [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    """
    if processes is None:
        processes = multiprocessing.cpu_count()
    size = len(iterable) if isinstance(iterable, Sized) else None
    chunks = chunkize(iterable, processes * scale, maxsize=size)
    pool = mp.Pool(processes)
    map_func = pool.map if not starmap else pool.starmap
    ret = []
    progress = None
    if show_progress:
        tqdm = importlib.import_module("tqdm")
        progress = tqdm.tqdm(chunks, desc=desc, total=size)
    for chunk in chunks:
        items = map_func(func, chunk)
        ret.extend(items)
        if progress is not None:
            progress.update(len(items))
    return ret


def starmap_async(*args, **kwargs):
    return map_async(*args, starmap=True, **kwargs)
