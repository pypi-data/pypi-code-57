import gc
import logging
import time
from multiprocessing import Process, Manager
from threading import Thread

import numpy as np

from optimizers import FullSpearmanMaxEntCopulaOptimizer


class FullCopulaFinder(Process):
	''' 
	The role of a finder is to consume model parameters from a queue.
	'''
	def __init__(self, parameters_queue):
		logging.info("Creating a copula finder worker.")
		super(FullCopulaFinder, self).__init__()
		self.daemon = True
		self.parameters_queue = parameters_queue
		self.d = None

	def run(self):
		keep_trying = True
		logging.info("Starting to find copulas...")
		while keep_trying:
			while not self.parameters_queue.empty():
				keep_trying = False
				corr = self.parameters_queue.get()
				d = corr.shape[0]

				if self.d is None:
					self.d = d

				if self.d != d:
					logging.info('Received a different n_var: terminating process')
					self.parameters_queue.put(corr)
					self.terminate()

				logging.info('Processing parameter batch %s' % str(corr))
				m = FullSpearmanMaxEntCopulaOptimizer(spearman_correlation_matrix=corr, \
					record_copulas=True, optimize=True)

				self.parameters_queue.task_done()
				gc.collect()

			time.sleep(0.01)



class CopulaFinderWorkerPool(object):
    """
    Class for worker pool with builtin queue
    """

    def __init__(self, workers=15, class_name='FullCopulaFinder'):
        self.num_workers = workers
        self.class_name = class_name
        m = Manager()
        self.queue = m.Queue()
        self.workers = [self._init_worker() for _ in range(self.num_workers)]
        self.watcher_thread = Thread(target=self._watch_workers)
        self.watcher_thread.start()


    def _init_worker(self):
        worker = eval(self.class_name)(self.queue)
        worker.start()
        return worker


    def _watch_workers(self):
        while True:
            time.sleep(2.)
            logging.info('Queue Size: %s' % self.queue.qsize())
            for idx in range(self.num_workers):
                if idx > len(self.workers) - 1:
                    logging.warning("Adding a new worker...")
                    self.workers += [self._init_worker()]
                elif not self.workers[idx].is_alive():
                    logging.warning("Dead worker detected, Adding a new worker...")
                    self.workers[idx] = self._init_worker()

    def submit(self, args):
        """
        Adds the named params dict as a work item to worker queue
        :param kwargs: all the named params for this work item
        """
        self.queue.put(args, block=False)




