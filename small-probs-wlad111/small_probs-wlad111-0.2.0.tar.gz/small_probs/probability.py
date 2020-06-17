import pymc3_ext as pm
import numpy as np
from small_probs import estimates
from scipy.stats import norm
import math




class ProbabilityEstimator:

    def __init__(self, p, scorefun, proposal, default_val, save_trace=False, n_samples=1000000):

        self.initial_p = p
        self.scorefun = scorefun
        self.proposal = proposal
        self.save_trace = save_trace
        #self.weights = initial_weights
        self.default_val = default_val
        self.fitted = False
        self.n_samples = n_samples


    def estimate_boolean(self, bool_func):
        pass

    def estimate_between(self, left, right):
        score_trace = self.__get_score_trace()
        mask = estimates.interval_mask(score_trace, left, right)
        self.__estimate_masked(mask, score_trace)
        self.fitted = True

    def confint(self, gamma=0.95):
        if self.fitted:
            z = norm.ppf((1 + gamma)/2)
            left = self.prob - (z * np.sqrt(self.var)) / np.sqrt(self.n_samples)
            right = self.prob + (z * np.sqrt(self.var)) / np.sqrt(self.n_samples)
        else:
            print("Probability is not estimated yet!")
        return left, right

    def summary(self):
        pass

    def __get_score_trace(self, n_samples=1000000):

        with pm.Model() as m:
            s = pm.WeightedScoreDistribution('S', scorer=self.scorefun,
                                             cat=True,
                                             default_val=self.default_val)
            trace = pm.sample(n_samples, cores=1, start={'S': self.default_val},
                              step=pm.GenericCatMetropolis(vars=[s], proposal=self.proposal),
                              compute_convergence_checks=False, chains=1, wl_weights=True)
            #self.weights = np.exp(s.distribution.weights.get_value())
            weights = s.distribution.weights_dict
            self.weights_exp = {k: math.exp(v) for k, v in weights.items()}

        score_trace = np.array([self.scorefun(x) for x in trace['S']]).astype('int32')

        if self.save_trace:
            self.score_trace = score_trace
        return score_trace

    def __estimate_masked(self, mask, score_trace):
        w = np.array([self.weights_exp[s] for s in score_trace])
        prob = estimates._estimate_numenator(mask, w) / estimates._estimate_denominator(w)
        self.prob = prob
        self.var = estimates.varianceOBM(w, mask)

