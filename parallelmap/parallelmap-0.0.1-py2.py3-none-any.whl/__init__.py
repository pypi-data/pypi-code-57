#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/06/19 08:31:38
@Author  :   nicholas wu 
@Version :   1.0
@Contact :   nicholas_wu@aliyun.com
@License :    
@Desc    :   None
'''
from typing import List
import os
import pickle
import pandas as pd
from itertools import count
from multiprocessing import Manager, Pool, cpu_count
from tempfile import NamedTemporaryFile
from time import time

import dill
from pandarallel.pandarallel import get_workers_result
from parallelmap.wrappers.data_wrapper import DataWrapper

# By default, Pandarallel use all available CPUs
NB_WORKERS = cpu_count()

# Prefix and suffix for files used with Memory File System
PREFIX = "pandarallel_"
PREFIX_INPUT = PREFIX + "input_"
PREFIX_OUTPUT = PREFIX + "output_"
SUFFIX = ".pickle"

# Root of Memory File System
MEMORY_FS_ROOT = "/dev/shm"

NO_PROGRESS, PROGRESS_IN_WORKER, PROGRESS_IN_FUNC, PROGRESS_IN_FUNC_MUL = list(
    range(4))

INPUT_FILE_READ, PROGRESSION, VALUE, ERROR = list(range(4))

_func = None


def worker_init(func):
    global _func
    _func = func


def global_worker(x):
    return _func(x)

class ProgressState:
    last_put_iteration = None
    next_put_iteration = None
    last_put_time = None


def get_nb_workers(nb_workers):
    if not nb_workers:
        nb_workers = cpu_count()
    assert type(nb_workers) == int and nb_workers >= 1, "nb_workers type must be int and >= 1."
    return nb_workers


def normal_iterables(*iterables):
    lengths = [len(iterable) for iterable in iterables]
    assert len(set(lengths)) == 1, "iterables must have same shape."
    return tuple([pd.Series(data) for data in iterables])


def progress_pre_func(queue, index, counter, progression, state, time):
    """Send progress to the MASTER about every 250 ms.

    The estimation system is implemented to avoid to call time() to often,
    which is time consuming.
    """
    iteration = next(counter)

    if iteration == state.next_put_iteration:
        time_now = time()
        queue.put_nowait((progression, (index, iteration)))

        delta_t = time_now - state.last_put_time
        delta_i = iteration - state.last_put_iteration

        state.next_put_iteration += max(int((delta_i / delta_t) * 0.25), 1)
        state.last_put_iteration = iteration
        state.last_put_time = time_now


def progress_wrapper(progress_bar, queue, index, chunk_size):
    """Wrap the function to apply in a function which monitor the part of work already done.

    inline is used instead of traditional wrapping system to avoid unnecessary function call
    (and context switch) which is time consuming.
    """
    counter = count()
    state = ProgressState()
    state.last_put_iteration = 0
    state.next_put_iteration = max(chunk_size // 100, 1)
    state.last_put_time = time()

    def wrapper(func):
        if progress_bar:
            def wrapped_func(*args, **kwargs):
                progress_pre_func(queue=queue,
                                  index=index,
                                  counter=counter,
                                  progression=PROGRESSION,
                                  state=state,
                                  time=time,)
                res = func(*args, **kwargs)
                return res
            return wrapped_func
        return func

    return wrapper


def get_workers_args(
    use_memory_fs,
    nb_workers,
    progress_bar,
    chunks,
    worker_meta_args,
    queue,
    func,
    args,
    kwargs,
):
    """This function is run on the MASTER.

    If Memory File System is used:
    1. Create temporary files in Memory File System
    2. Dump chunked input files into Memory File System
       (So they can be read by workers)
    3. Break input data into several chunks
    4. Wrap the function to apply to display progress bars
    5. Dill the function to apply (to handle lambda functions)
    6. Return the function to be sent to workers and path of files
       in the Memory File System

    If Memory File System is not used, steps are the same except 1. and 2. which are
    skipped. For step 6., paths are not returned.
    """

    def dump_and_get_lenght(chunk, input_file):
        with open(input_file.name, "wb") as file:
            pickle.dump(chunk, file)

        return len(chunk)

    if use_memory_fs:
        input_files = create_temp_files(nb_workers)

        try:
            chunk_lengths = [
                dump_and_get_lenght(chunk, input_file)
                for chunk, input_file in zip(chunks, input_files)
            ]

            nb_chunks = len(chunk_lengths)
            output_files = create_temp_files(nb_chunks)

        except OSError:
            link = "https://stackoverflow.com/questions/58804022/how-to-resize-dev-shm"
            msg = " ".join(
                (
                    "It seems you use Memory File System and you don't have enough",
                    "available space in `dev/shm`. You can either call",
                    "pandarallel.initalize with `use_memory_fs=False`, or you can ",
                    "increase the size of `dev/shm` as described here:",
                    link,
                    ".",
                    " Please also remove all files beginning with 'pandarallel_' in the",
                    "`/dev/shm` directory. If you have troubles with your web browser,",
                    "these troubles should deseapper after cleaning `/dev/shm`.",
                )
            )
            raise OSError(msg)

        workers_args = [
            (
                input_file.name,
                output_file.name,
                index,
                worker_meta_args,
                queue,
                progress_bar == PROGRESS_IN_WORKER,
                dill.dumps(
                    progress_wrapper(
                        progress_bar >= PROGRESS_IN_FUNC, queue, index, chunk_length
                    )(func)
                ),
                args,
                kwargs,
            )
            for index, (input_file, output_file, chunk_length) in enumerate(
                zip(input_files, output_files, chunk_lengths)
            )
        ]

        return workers_args, chunk_lengths, input_files, output_files

    else:
        workers_args, chunk_lengths = zip(
            *[
                (
                    (
                        chunk,
                        index,
                        worker_meta_args,
                        queue,
                        progress_bar,
                        dill.dumps(
                            progress_wrapper(
                                progress_bar == PROGRESS_IN_FUNC,
                                queue,
                                index,
                                len(chunk[0]),
                            )(func)
                        ),
                        args,
                        kwargs,
                    ),
                    len(chunk[0]),
                )
                for index, chunk in enumerate(chunks)
            ]
        )
        return workers_args, chunk_lengths, [], []

def prepare_worker(use_memory_fs):
    def closure(function):
        def wrapper(worker_args):
            """This function runs on WORKERS.

            If Memory File System is used:
            1. Load all pickled files (previously dumped by the MASTER) in the
               Memory File System
            2. Undill the function to apply (for lambda functions)
            3. Tell to the MASTER the input file has been read (so the MASTER can remove it
               from the memory
            4. Apply the function
            5. Pickle the result in the Memory File System (so the Master can read it)
            6. Tell the master task is finished

            If Memory File System is not used, steps are the same except 1. and 5. which are
            skipped.
            """
            if use_memory_fs:
                (
                    input_file_path,
                    output_file_path,
                    index,
                    meta_args,
                    queue,
                    progress_bar,
                    dilled_func,
                    args,
                    kwargs,
                ) = worker_args

                try:
                    with open(input_file_path, "rb") as file:
                        data = pickle.load(file)
                        queue.put((INPUT_FILE_READ, index))

                    result = function(
                        dill.loads(dilled_func),
                        *data
                    )

                    with open(output_file_path, "wb") as file:
                        pickle.dump(result, file)

                    queue.put((VALUE, index))

                except Exception:
                    queue.put((ERROR, index))
                    raise
            else:
                (
                    data,
                    index,
                    meta_args,
                    queue,
                    progress_bar,
                    dilled_func,
                    args,
                    kwargs,
                ) = worker_args
                try:
                    result = function(
                        dill.loads(dilled_func), 
                        *data
                    )
                    queue.put((VALUE, index))

                    return result

                except Exception:
                    queue.put((ERROR, index))
                    raise

        return wrapper

    return closure

def parallelize(nb_requested_workers,
                use_memory_fs,
                progress_bar,
                get_chunks,
                worker,
                reduce,
                get_worker_meta_args=lambda _: dict(),
                get_reduce_meta_args=lambda _: dict()):
    """Master function.
    1. Split data into chunks
    2. Send chunks to workers
    3. Wait for the workers results (while displaying a progress bar if needed)
    4. One results are available, combine them
    5. Return combined results to the user
    """
    def closure(func, *iterables, **kwargs):
        chunks = get_chunks(
            nb_requested_workers, *iterables)

        manager = Manager()
        queue = manager.Queue()
        worker_meta_args = get_worker_meta_args(iterables)
        reduce_meta_args = get_reduce_meta_args(iterables)
        workers_args, chunk_lengths, input_files, output_files = get_workers_args(
            use_memory_fs,
            nb_requested_workers,
            progress_bar,
            chunks,
            worker_meta_args,
            queue,
            func,
            (),
            kwargs,
        )
        nb_workers = len(chunk_lengths)
        try:
            pool = Pool(
                nb_workers, worker_init, (prepare_worker(
                    use_memory_fs)(worker),),
            )
            map_result = pool.map_async(global_worker, workers_args)
            pool.close()
            results = get_workers_result(
                use_memory_fs,
                nb_workers,
                progress_bar,
                1,
                queue,
                chunk_lengths,
                input_files,
                output_files,
                map_result,
            )
            return reduce(results)

        finally:
            if use_memory_fs:
                for file in input_files + output_files:
                    file.close()

    return closure


def parallel_map(func, *iterables, **kwargs) -> List:
    nb_requested_workers = kwargs.get("nb_workers", NB_WORKERS)
    use_memory_fs = kwargs.get("use_memory_fs", False)
    progress_bar = kwargs.get("progress_bar", False)
    progress_in_func = PROGRESS_IN_FUNC * progress_bar
    get_chunks = DataWrapper.get_chunks
    worker = DataWrapper.worker
    reduce = DataWrapper.reduce
    paraller = parallelize(nb_requested_workers,
                           use_memory_fs,
                           progress_in_func,
                           get_chunks,
                           worker,
                           reduce
                           )
    iterables = normal_iterables(*iterables)
    return paraller(func, *iterables, **kwargs)
