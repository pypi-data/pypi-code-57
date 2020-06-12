import logging
import warnings

import numpy as np
from scipy.optimize import minimize

from db import get_session_factory, SpearmanCopulaDensityModel
from z import FullSpearmanZMC
from decorators import hits_api_first


class FullSpearmanMaxEntCopulaOptimizer(object):
	'''
	Distribution with minimum KL-divergence (maximum entropy) relative to the uniform distribution, 
	given the full Spearman rank correlation matrix, and with marginals approximately uniform 
	(same first n_moments moments as the standard uniform).
	'''
	def __init__(self, spearman_correlation_matrix=None, verbose=True, n_moments=2, record_copulas=False, optimize=True):
		assert spearman_correlation_matrix is not None, 'The spearman correlation matrix should be provided'
		assert spearman_correlation_matrix.shape[0] == spearman_correlation_matrix.shape[1], \
			'The spearman correlation matrix should be square'
		self.n_var = spearman_correlation_matrix.shape[0]
		self.n_moments = n_moments
		self.session_factory = get_session_factory()
		self.record_copulas = record_copulas
		self.corr = spearman_correlation_matrix
		self.constraints_values = FullSpearmanZMC.spearman_corr_to_theta(spearman_correlation_matrix, \
			n_moments=self.n_moments)
		self.optimize(verbose=verbose)


	@property
	def initial_theta(self):
		x0 = np.zeros_like(self.constraints_values)
		m = FullSpearmanMaxEntCopulaOptimizer(spearman_correlation_matrix=self.corr[:-1, :-1])
		x0[:self.n_var-1] = m.theta[:self.n_var-1]
		marker = self.n_var-1
		shift = self.n_var
		
		for idx, i in enumerate(reversed(range(1, self.n_var+1))):
			x0[shift:shift+i-1] = m.theta[marker:marker+i-1]
			marker += i-1
			shift += i
		
		return x0


	@hits_api_first
	def optimize(self, verbose=True):
		'''
		Learn the parameters of the minimum KL-divergence (maximum entropy)
	    relative to the uniform distribution, under constraints self.constraints.
		'''
		scale = 100.
		def f(theta):
			''' Squared norm of the difference between the linear constraints and their targets. '''
			z = FullSpearmanZMC(theta, self.n_var)
			e = z.gradient_log - self.constraints_values
			w = z.constraints_scales
			e = e * w

			if z.is_copula and self.record_copulas:
				d = z.as_dict.copy()
				c = SpearmanCopulaDensityModel(**d)
				try:
					db_session = self.session_factory()
					existing_copula = db_session.query(SpearmanCopulaDensityModel).filter_by(\
						model_id_md5=z.as_dict['model_id_md5']).first()
					if existing_copula:
						logging.info('Skipping previously recorded copula %s.' % (str(z.as_dict)))

					else:
						logging.info('Recording copula %s.' % (str(d)))
						db_session.add(c)
						db_session.commit()
						logging.info('Done recording copula %s.' % (str(d)))

				except:
					logging.exception("Failed to commit %s " % (str(d)))
					db_session.rollback()

				finally:
					if db_session:
						self.session_factory.remove()

			return scale*0.5*np.dot(e, e)


		def grad_f(theta):
			''' Gradient of the squared norm of the difference between the linear constraints and their targets. '''
			z = FullSpearmanZMC(theta, self.n_var)
			e = z.gradient_log - self.constraints_values
			w = z.constraints_scales
			e = e * (w**2)
			J = z.hessian_log

			return scale*np.dot(J, e)


		res = minimize(f, self.initial_theta, jac=grad_f)
		self.set_theta(res['x'])

		if verbose:
			logging.info(res)

		return res


	def set_theta(self, theta):
		'''
		Update distribution parameters
		'''
		self.theta = theta
		self.z = FullSpearmanZMC(self.theta, self.n_var)


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO)
	corr = np.array([[1.0, -0.378, 0.01], [-0.378, 1.0, 0.1], [0.01, 0.1, 1.0]])
	m = FullSpearmanMaxEntCopulaOptimizer(spearman_correlation_matrix=corr, record_copulas=True)



