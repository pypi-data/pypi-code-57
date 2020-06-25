
import logging
from multiprocessing import cpu_count

from scipy.stats import ortho_group
import numpy as np
import pandas as pd

from workers import CopulaFinderWorkerPool
from db import get_kxy_db_engine


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO)
	logging.info('Creating the Queues')
	n_finders = cpu_count()

	logging.info('Generating the parameters')
	logging.info('Adding the parameters to the processing queue')

	worker_pool = None
	for d in range(2, 11):
		for i in range(10000):
			u = ortho_group.rvs(d)
			s = np.random.gamma(.7, 2., d)
			cov = np.dot(u.T, np.dot(np.diag(s), u))
			sd = np.sqrt(np.diag(cov))
			corr = ((cov / sd).T / sd).T

			if worker_pool is None:
				worker_pool = CopulaFinderWorkerPool(workers=cpu_count(), class_name='FullCopulaFinder')

			worker_pool.submit(corr)

	# Don't exit until we are done
	logging.info('Waiting for the work to be done')
	worker_pool.queue.join()

