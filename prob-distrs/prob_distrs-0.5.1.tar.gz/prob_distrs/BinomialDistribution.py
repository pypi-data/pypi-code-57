import math
import matplotlib.pyplot as plt
import numpy as np
import random
from .GeneralDistribution import Distribution

class Binomial(Distribution):
    """ 
    Binomial distribution class for calculating and visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) number of trials            
    """
    
    
    def __init__(self, prob = random.uniform(0,1), size = 20):
                
        self.n = size
        self.p = prob
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
        self.data = np.random.binomial(self.n, self.p, 500)
    
                        
    
    def calculate_mean(self):
    
        """
        Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.mean = self.p * self.n
                
        return self.mean



    def calculate_stdev(self):

        """
        Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        
        return self.stdev
        
        
    def read_data_file(self, file_name):
    
        """
        Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute. 
        After reading in the file, the mean and standard deviation are calculated
        
        Args: 
            file_name (string): name of a file to read from
        
        Returns: 
            float: the p value
            float: the n value
    
        """

        Distribution.read_data_file(self, file_name)

        try:
            npdata = np.array(self.data)
            assert np.array_equal(npdata, npdata.astype(bool)), 'data contains values other than 0 or 1'
        except AssertionError as error:
            raise

        self.n = len(self.data)
        self.p = 1.0 * sum(self.data) / self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        
        return self.p, self.n

    
        
    def plot_raw_data(self):

        """
        Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
                
        plt.bar(x = ['0', '1'], height = [(1 - self.p) * self.n, self.p * self.n])
        plt.title('Bar Chart of Data')
        plt.xlabel('Outcome')
        plt.ylabel('Count')
        plt.show()
        
        
    def pmf(self, k):

        """
        Probability mass function calculator for the binomial distribution.
        
        Args:
            k (unsigned int): point for calculating the probability mass function. k is in support (the set{0, 1, ..., n})
        
        Returns:
            float: probability density function output
        """
        
        try:
            assert k in range(self.n + 1), 'k isn\'t in support'
        except AssertionError as error:
            raise

        n_choose_k = math.factorial(self.n) / (math.factorial(k) * (math.factorial(self.n - k)))
        prob_of_k_successes = (self.p ** k)
        prob_rest_are_failures = (1 - self.p) ** (self.n - k)
        
        return n_choose_k * prob_of_k_successes * prob_rest_are_failures


    def cdf(self, k):

        """
        Cumulative distribution function calculator for the binomial distribution.
        
        Args:
            k (unsigned float): point for calculating the cumulative distribution function.
        
        Returns:
            float: cumulative density function output
        """
        
        try:
            assert k >= 0, 'k isn\'t nonnegative'
        except AssertionError as error:
            raise

        return sum([self.pmf(x) for x in range(int(math.floor(k)) + 1)])        

    def plot(self):

        """
        Function to plot the pmf and cdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the both plot
            list: y1 values for the pmf plot
            list: y2 values for cdf plot
            
        """
        
        x = []
        y1 = []
        y2 = []
        
        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y1.append(self.pmf(i))
            y2.append(self.cdf(i))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        
        axes[0].plot(x, y1)
        axes[0].set_title('Probability Distribution of Outcomes')
        axes[0].set_ylabel('Probability Density')

        axes[1].plot(x, y2)
        axes[1].set_title('Cumulative Distribution of Outcomes')
        axes[1].set_ylabel('Probability')

        plt.show()

        return x, y1, y2
        
    def __add__(self, other):
        
        """
        Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        result.calculate_mean()
        result.calculate_stdev()
        
        return result
        
        
    def __repr__(self):
    
        """
        Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial
        
        """
        
        return "mean = {}, standard deviation = {}, p = {}, n = {}".\
        format(self.mean, self.stdev, self.p, self.n)