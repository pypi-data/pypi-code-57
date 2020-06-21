import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class BayesProportionsEstimation:

    def __init__(self, a, b, prior_alpha=0.5, prior_beta=0.5, n=10000, seed=None):
        '''
        Initialises the BayesProportionsEstimation class and samples from the posterior distribution
        Parameters
        ----------
        a: list, ndarray or Series [successes, trials]:  array describing results from sample a
        b: list, ndarray or Series [successes, trials]:  array describing results from sample b
        prior_alpha: float, alpha parameter for the Beta prior distribution, default = 0.5 (Jeffreys prior)
        prior_beta: float, beta parameter for the Beta prior distribution, default = 0.5 (Jeffreys prior)
        m: integer, number of samples to take from the posterior distribution, default = 10000
        seed: integer, set random seed at the start of the initialisation, default = None
        '''   
        self.a = a
        self.b = b
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self.n = n  
        self.seed = seed
        self._check_inputs()
        self._sample_posteriors()

    def _check_inputs(self):
        # Checks that parameters are in the correct format
        types = ['list', 'ndarray', 'Series']
        if ((type(self.a).__name__ not in types) or (type(self.b).__name__ not in types)):
            raise ValueError("type(a).__name__ and/or type(b).__name__ must be 'list', 'ndarray' or 'DataFrame'")
        if ((self.a[0] > self.a[1]) or (self.b[0] > self.b[1])):
            raise ValueError("the count of successes for a and/or b exceeds the number of trials")
        if ((self.prior_alpha <= 0) or (self.prior_beta <= 0)):
            raise ValueError("the prior_alpha and/or prior_beta parameters must be > 0")
        if self.n <= 0:
            raise ValueError("n must be a positive integer")
        if self.seed is not None and str(self.seed).isdigit() == False:
            raise ValueError("seed must be a positive integer or None")

    def _posterior_function(self, d):
        # Defines the posterior
        return np.random.beta(d[0] + self.prior_alpha, d[1] - d[0] + self.prior_beta, self.n)

    def _sample_posteriors(self):
        # Draws from posterior
        np.random.seed(self.seed)
        a_draw = self._posterior_function(self.a)
        b_draw = self._posterior_function(self.b)
        d_draw = b_draw - a_draw
        self.a_draw = a_draw
        self.b_draw = b_draw
        self.d_draw = d_draw

    def get_posteriors(self):
        '''
        Retrieves random draws from the posterior
        Returns
        -------
        tuple:
            - np.array[n] draws from the posterior of theta_a
            - np.array[n] draws from the posterior of theta_b
            - np.array[n] draws from the posterior of theta_b minus draws from the posterior of theta_a
        '''
        return (self.a_draw, 
                self.b_draw, 
                self.d_draw)

    def _calculate_quantiles(self, d, mean, quantiles):
        # Calculate mean and quantiles
        q = np.quantile(d, quantiles)
        if mean is True:
            q = np.append(q, np.mean(d))    
        return q

    def quantile_summary(self, mean=True, quantiles=[0.025, 0.5, 0.975], names = None):
        '''
        Summarises the properties of the estimated posterior
        Parameters
        ----------
        mean:  boolean, default True, calculates the mean of the draws from the posterior.  Default True
        quantiles: list, calculates the quantiles of the draws from the posterior.  Default [0.025, 0.5, 0.975]
        names:  list of length 3, parameter names in order: a, b, b-a.  Default ['theta_a', 'theta_b', 'delta']
        Returns
        -------
        pd.DataFrame:  
            'theta_a':  summaries of the posterior of theta_a
            'theta_b':  summaries of the posterior of theta_b
            'delta':  summaries of the posterior of theta_b - theta_a
        '''
        if quantiles is None:
            raise ValueError("quantiles must be a list of length > 0")      
        draws = [self.a_draw, self.b_draw, self.d_draw]
        if names is None:
            names = [
                    'theta_a',
                    'theta_b',
                    'delta'
                    ]
        if len(names) > 3:
            raise ValueError('names must be a list of length 3')
        q = []
        for i in draws:
            q.append(self._calculate_quantiles(i, mean, quantiles))
        df = pd.DataFrame(np.array(q))
        if mean is True:
            df.columns = list(map(str, quantiles)) + ['mean']
        else:
            df.columns = list(map(str, quantiles)) 
        df['parameter'] = names
        return df

    def kde_plot(self, quantiles=[0.025, 0.975], fig_size=(15, 5), names=None):
        '''
        Plots the density of the draws from the posterior distribution
        Parameters
        ----------
        quantiles: list of length 2, quantiles to denote credible intervals.  Default [0.025, 0.975]
        fig_size: tuple, plot dimensions (width, height).  Default (15, 5)
        names: list of length 3, parameter names for kde plot.  Default ['theta_a', 'theta_b', 'delta']
        '''        
        if len(quantiles) != 2:
            raise ValueError("quantiles must be a list of length 2")
        if names is None:
            names = [
                'theta_a',
                'theta_b',
                'delta'
                ]
        if len(names) > 3:
            raise ValueError('names must be a list of length 3')
        draws = [self.a_draw, self.b_draw, self.d_draw]
        fig, axes = plt.subplots(1, 3, figsize=fig_size)
        for i in range(0, 3):
            sns.kdeplot(draws[i], ax=axes[i])
            axes[i].set(xlabel=names[i], ylabel='density')    
            x, y = axes[i].lines[0].get_data()
            q = self._calculate_quantiles(draws[i], mean=False, quantiles=quantiles)
            axes[i].fill_between(x, y, where=((x >= q[0]) & (x <= q[1])), alpha=0.2)
            axes[i].fill_between(x, y, where=((x <= q[0]) | (x >= q[1])), alpha=0.1)
            if i == 2:
                axes[i].axvline(0, ls='--', color='red')
