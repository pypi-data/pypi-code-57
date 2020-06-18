
from functools import wraps
import logging
import json

import numpy as np
import pandas as pd

from db import get_kxy_db_engine, get_session_factory, SpearmanCopulaDensityModel
from z import FullSpearmanZMC



def hits_api_first(method):
	'''
	The decorator seeks to get the reesult of the intended computation remotely first, 
	before attempting to run the computation locally.
	'''
	KXY_DB_ENGINE = get_kxy_db_engine()
	SESSION_FACTORY = get_session_factory()
	@wraps(method)
	def wrapper(*args, **kw):
		obj = args[0]

		if obj.__class__.__name__ == 'FullSpearmanMaxEntCopulaOptimizer' and method.__name__ == 'optimize':
			ordered_corr = FullSpearmanZMC.order_corr(obj.corr)
			db_session = SESSION_FACTORY()
			n_existing_copula = db_session.query(SpearmanCopulaDensityModel).filter_by(
				ordered_spearman_corr_matrix={i: list(ordered_corr[i]) for i in range(len(ordered_corr))}).count()

			if n_existing_copula and n_existing_copula > 1:
				existing_copula = db_session.query(SpearmanCopulaDensityModel).filter_by(
					ordered_spearman_corr_matrix={i: list(ordered_corr[i]) for i in range(len(ordered_corr))}).first()

				if existing_copula:
					logging.info('Found result from API for spearman correlation matrix %s ' % str(ordered_corr))
					logging.info('Setting cached result')
					z = FullSpearmanZMC.from_parameters_dict(existing_copula.theta, \
						existing_copula.d, n_moments=existing_copula.n_moments)

					obj.set_theta(z.theta)
					logging.info('Done setting cached result')
					return {'x': obj.theta}


		# Else run the method
		return method(*args, **kw)

	return wrapper


