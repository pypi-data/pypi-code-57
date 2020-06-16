import math
import matplotlib.pyplot as plt
from .GeneralDistribution import Distribution
import numpy as np

class Exponential(Distribution):
    """ 
    Exponential distribution class for calculating and visualizing a Exponential distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        rate (float) rate at which events occur
    """
    
    
    def __init__(self, rate = 1):
                
        self.rate = rate
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

        self.data = np.random.exponential(1.0/self.rate, 500)
                        
    
    def calculate_mean(self):
    
        """
        Function to calculate the mean from rate

        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.mean = 1.0/self.rate
                
        return self.mean



    def calculate_stdev(self):

        """
        Function to calculate the standard deviation from rate
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        self.stdev = 1.0/self.rate
        
        return self.stdev
 

    def read_data_file(self, file_name):
    
        """
		Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute. 
		After reading in the file, the mean and standard deviation are calculated
		
		Args: 
			file_name (string): name of a file to read from
		
		Returns: 
			float: rate parameter
	
        """
        Distribution.read_data_file(self, file_name)
        
        self.rate = 1.0 * len(self.data)/sum(self.data)
        
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        
        return self.rate

    def pdf(self, k):

        """
        Probability density function calculator for the poisson distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        Returns:
            float: probability density function output
        """

        return self.rate * math.exp(-self.rate * k) if k >= 0 else 0
    
    def cdf(self, k):

        """
        Cumulative density function calculator for the poisson distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: cumulative density function output
        """

        return 1 - math.exp(-self.rate * k) if k >= 0 else 0
        

    def plot(self):

        """
        Function to plot the data, pdf, cdf of the exponential distribution
        
        Args:
            None
        
        Returns:
            list: x values for the both plot
            list: y1 values for the pdf plot
            listL y2 values for the cdf plot
            
        """
        
        mu = self.mean
        sigma = self.stdev
        data = self.data.sort()

        x = list(set(self.data))
        x.sort()
        y1 = []
        y2 = []
		
		# calculate the y values to visualize
        for i in x:
            y1.append(self.pdf(i))
            y2.append(self.cdf(i))

		# make the plot
        fig, axes = plt.subplots(3,sharex=True)
        fig.subplots_adjust(hspace=.5)

        axes[0].hist(self.data, len(x), density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')
        
        axes[1].plot(x, y1)
        axes[1].set_title('Probability Distribution for Data')
        axes[1].set_ylabel('Probability Density')

        axes[2].plot(x, y2)
        axes[2].set_title('Cumulative Distribution for Data')
        axes[2].set_ylabel('Probability')

        plt.show()

        return x, y1, y2
        
    def __add__(self, other):
        pass
        
    def __repr__(self):
    
        """
        Function to output the characteristics of the Exponential instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Exponential
        
        """
        
        return "mean {}, standard deviation {}, rate parameter {}".\
        format(self.mean, self.stdev, self.rate)