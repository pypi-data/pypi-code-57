
import hashlib
import threading
sampling_lock = threading.Lock()
from functools import lru_cache
import os
from time import time

import numpy as np
import numexpr as ne

from utils import cached_property

gU, gD, gM = None, None, None

class FullSpearmanZMC(object):
	'''
	'''
	def __init__(self, *args, **kwargs):
		self.theta = args[0]
		self.n_var = args[1] # Should be an int
		self.n_moments = kwargs.get('n_moments', 2)
		assert self.n_moments == 2, 'n_moments>2 not yet supported'
		assert len(self.theta) == self.n_moments * self.n_var + self.n_var * (self.n_var-1)//2
		self.random_state = np.random.RandomState(os.getpid())


	@cached_property
	def model_id(self):
		return ['d=%d' % self.n_var, 'n_moments=%d' % self.n_moments, 'theta=(%s)' % ','.join(['%.6f' % _ for _ in self.theta])]


	@cached_property
	def model_id_md5(self):
		return hashlib.md5(str(self.model_id).encode()).hexdigest()


	@property
	def theta_quad(self):
		'''
		Form the matrix A = a_ij such that a_ij is the coefficient of u_iu_j in the 
		'''
		res = np.zeros((self.n_var, self.n_var))
		shift = self.n_var
		for idx, i in enumerate(reversed(range(1, self.n_var+1))):
			res[idx, idx:idx+i] = self.theta[shift:shift+i]
			shift += i
		res = 0.5*(res + res.T)

		return res


	@property
	def theta_lin(self):
		'''
		First order coefficients (i.e. coefficient of u_i)
		'''
		return self.theta[:self.n_var]


	@cached_property
	def log_integrand_samples(self):
		''' 
		Generate samples from \theta^T * \phi(u)
		'''
		global gU, gM, gD

		if gU is None or gD != self.n_var or gM != self.n_moments:
			# Uniform samples
			U = self.random_state.rand(10000000, self.n_var)
			gU = U
			gM = self.n_moments
			gD = self.n_var

		else:
			U = gU

		# First order terms
		ret = np.dot(U, self.theta_lin)

		# Second order terms
		ret += np.sum(U*np.dot(self.theta_quad, U.T).T, axis=1)

		return ret, U


	@property
	def samples(self):
		''' 
		Generate samples from the variable exp(\theta^T * \phi(u)).
		'''
		samples_ = np.clip(self.log_integrand_samples[0], -500.0, 500.0)
		samples_ = ne.evaluate('exp(samples_)')  # np.exp()

		return samples_


	@property
	def gradient_samples(self):
		'''
		Generate samples from the variable \phi(u)[i] * exp(\theta^T * \phi(u)).
		'''
		U = self.log_integrand_samples[1]
		res = np.zeros((U.shape[0], self.theta.shape[0]))

		for i in range(self.n_var):
			res[:, i] = self.samples * U[:, i]

		shift = self.n_var
		for i, ni in enumerate(reversed(range(1, self.n_var+1))):
			for j in range(i, self.n_var):
				res[:, shift] = self.samples * U[:, i] * U[:, j]
				shift += 1

		return res


	@cached_property
	def samples_selector(self):
		return np.isfinite(self.samples)


	@cached_property
	def n_samples(self):
		return self.samples[self.samples_selector].shape[0]


	@cached_property
	def value(self):
		''' 
		Evaluate Z(theta) using Monte Carlo.
			Z(theta) = Avg(self.samples)
		'''
		return self.samples[self.samples_selector].mean()


	@cached_property
	def entropy(self):
		return np.log(self.value) - np.dot(self.gradient_log, self.theta)


	@cached_property
	def gradient_log(self):
		''' 
		Evaluate grad log Z(theta). 
		'''
		return self.gradient_samples[self.samples_selector].mean(axis=0)/self.value


	@cached_property
	def hessian_log(self):
		'''
		Evaluate the Hessian of log Z(theta). 
		'''
		DS = self.gradient_samples[self.samples_selector]
		D = DS.T / self.samples[self.samples_selector]
		res = (np.dot(D, DS)/self.n_samples)
		res /= self.value
		res -= np.outer(self.gradient_log, self.gradient_log)

		return res


	@cached_property
	def moment_constraints(self):
		'''
		Dictionary u_i^j: E[u_i^j]
		'''
		res = {'u_%d' % (i+1): self.gradient_log[i] for i in range(self.n_var)}
		shift = self.n_var
		for i, ni in enumerate(reversed(range(1, self.n_var+1))):
			res['u_%d^2' % (i+1)] = self.gradient_log[shift]
			shift += ni

		return res


	@cached_property
	def is_copula(self):
		'''
		Return False if and only if this is not the normalizing constant of a copula.
		'''
		if np.any(np.abs(self.gradient_log[:self.n_var]-0.5) > 0.001):
			return False

		shift = self.n_var
		for i, ni in enumerate(reversed(range(1, self.n_var+1))):
			if abs(self.gradient_log[shift]-1./3.) > 0.001:
				return False
			shift += ni

		return True


	@staticmethod
	def from_parameters_dict(theta, n_var, n_moments=2):
		'''
		Create an instance from saved parameters.
		'''
		theta = np.array(theta)
		return FullSpearmanZMC(theta, n_var, n_moments=n_moments)


	@cached_property
	def spearman_corr_matrix(self):
		'''
		Spearman correlation matrix. 
		rho_ij = 12E[u_ij]-3
		'''
		res = np.zeros((self.n_var, self.n_var))
		shift = self.n_var
		for i, ni in enumerate(reversed(range(1, self.n_var+1))):
			res[i, i:] = self.gradient_log[shift:shift+ni]
			res[i:, i] = self.gradient_log[shift:shift+ni]
			shift += ni

		res = 12.*res-3.0

		return res


	@staticmethod
	def spearman_corr_to_theta(corr, n_moments=2):
		'''
		'''
		n_var = corr.shape[0]
		theta = []
		theta += [0.5]*n_var
		shift = n_var
		for i, ni in enumerate(reversed(range(1, n_var+1))):
			theta += list((corr[i, i:]+3.)/12.)
			shift += ni

		if n_moments > 2:
			for m in range(3, n_moments+1):
				theta += [1./(m+1)]*n_var

		assert len(theta) == n_moments * n_var + n_var * (n_var-1)//2

		return np.array(theta)


	@staticmethod
	def order_corr(corr):
		n_var = corr.shape[0]
		indices = list(reversed(np.abs(corr).sum(axis=0).argsort()))
		ordered_corr = corr[indices].T[indices]
		rounded_ordered_corr = [['1.0' if i == j else '%.3f' % ordered_corr[i, j] \
					for j in range(n_var)] for i in range(n_var)]

		return rounded_ordered_corr		


	@cached_property
	def ordered_spearman_corr_matrix(self):
		'''
		Spearman correlation matrix, where variable are ordered by decreasing order of
		total absolute correllation.
		'''
		return FullSpearmanZMC.order_corr(self.spearman_corr_matrix)


	@cached_property
	def as_dict(self):
		return {\
			'created_at': time(), \
			'max_entropy_constraints': 'full-spearman-correlation-matrix', \
			'd': self.n_var, \
			'n_moments': self.n_moments, \
			'entropy': self.entropy, \
			'theta': list(self.theta), \
			'n_constraints': len(self.theta), \
			'expectations': list(self.gradient_log), \
			'spearman_corr_matrix': {i: list(self.spearman_corr_matrix[i, :]) for i in range(self.n_var)}, \
			'ordered_spearman_corr_matrix': {i: list(self.ordered_spearman_corr_matrix[i]) for i in range(self.n_var)}, \
			'moment_constraints': self.moment_constraints, \
			'model_id': str(self.model_id), \
			'model_id_md5': self.model_id_md5}


	@property
	def constraints_scales(self):
		return np.ones_like(self.theta)


