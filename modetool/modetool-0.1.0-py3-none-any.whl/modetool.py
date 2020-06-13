import itertools
import multiprocessing
import os

from loguru import logger

from .archive import Archive, InvalidArchive


class MODETool:
    def __init__(self, input, output, regions, workers, sort):
        self.input = input
        self.output = output
        self.regions = regions
        self.workers = workers
        self.sort = sort
        self.pool = None

    def worker(self, path):
        try:
            archive = Archive(path)
            dest = os.path.join(self.output, archive.region if self.sort else str())

            if self.regions and archive.region not in self.regions:
                return

            logger.info(f"Extracting: {dest}/{archive.name}")
            archive.extract(dest=dest)
        except InvalidArchive:
            return

    def run(self):
        try:
            logger.info("Running")
            logger.info(
                f"input={self.input} output={self.output} regions={self.regions} workers={self.workers} sort={self.sort}"
            )
            pool = multiprocessing.Pool(self.workers)
            walk = os.walk(self.input)
            jobs = itertools.chain.from_iterable(
                (os.path.join(root, file) for file in files)
                for root, dirs, files in walk
            )

            pool.map(self.worker, jobs)
        except KeyboardInterrupt:
            logger.info("Shutting down workers")
            pool.terminate()
            pool.join()
