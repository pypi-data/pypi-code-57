import matplotlib.pyplot as plt
import numpy as np
from .BinomialDistribution import Binomial

class Bernoulli(Binomial):
    """ 
    Bernoulli distribution class for calculating and visualizing a Bernoulli distribution.
    A Bernoulli distribution is a special case of a Binomial distribution (n = 1)
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
    """
    
    
    def __init__(self, prob = .5):

        self.n = 1        
        self.p = prob
        
        Binomial.__init__(self, self.p, self.n)

    def read_data_file(self):
        pass

    def pmf(self, k):

        """
        Probability mass function calculator for the bernoulli distribution.
        
        Args:
            k (unsigned int): point for calculating the probability mass function. k is in support (the set{0, 1})
        
        Returns:
            float: probability density function output
        """
        
        try:
            assert k in range(2), 'k isn\'t in support'
        except AssertionError as error:
            raise
        
        return 1 - self.p if k == 0 else self.p

    def cdf(self, k):

        """
        Cumulative distribution function calculator for the bernoulli distribution.
        
        Args:
            k (float): point for calculating the cumulative distribution function.
        
        Returns:
            float: cumulative density function output
        """
        if(k < 0): return 0
        return 1 - self.p if k >=0 and k < 1 else 1 

    def plot(self):

        """
        Function to plot the pmf and cdf of the Bernoulli distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pmf plot
            list: y values for the pmf plot
            list: x2 values for the cdf plot
            list: y2 values for the cdf plot
        """
        x = [0,1]
        y = [self.pmf(0), self.pmf(1)]
        x2 = np.arange(-2, 2, .05).tolist()
        y2 = map(self.cdf, x2)

        # make the plots
        fig, axes = plt.subplots(2)
        fig.subplots_adjust(hspace=.5)
        
        axes[0].plot(x, y, 'o')
        axes[0].set_title('Probability Distribution of Outcomes')
        axes[0].set_ylabel('Probability Density')
        axes[0].set_ylim([0,1])
        axes[0].set_xticks([0, 1])
        axes[0].axvline(x[0],0, y[0])
        axes[0].axvline(x[1],0, y[1])

        axes[1].plot(x2, y2)
        axes[1].set_title('Cumulative Distribution of Outcomes')
        axes[1].set_ylabel('Probability')

        plt.show()

        return x, y, x2, y2
