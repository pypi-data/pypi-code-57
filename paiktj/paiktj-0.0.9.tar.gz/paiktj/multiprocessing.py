from multiprocessing import Pool
from tqdm import tqdm


def pool(func, iterable, processes, total=None, verbose=True):
    if verbose:
        with Pool(processes) as p:
            result = list(tqdm(
                p.imap(func, iterable),
                total=total
            ))
    else:
        with Pool(processes) as p:
            result = list(
                p.map(func, iterable),
            )
    return result
