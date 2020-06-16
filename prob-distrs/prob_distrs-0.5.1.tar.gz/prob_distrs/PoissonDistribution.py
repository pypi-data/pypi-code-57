import math
import matplotlib.pyplot as plt
import numpy as np
from .GeneralDistribution import Distribution

class Poisson(Distribution):
	""" 
	Poisson distribution class for calculating and visualizing a Poisson distribution.
	
	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) representing the standard deviation of the distribution
		data_list (list of floats) a list of floats to be extracted from the data file
		lam (float) mean number of times an event occurs in a time interval
	"""
	
	
	def __init__(self, lam = 5):
				
		self.lam = lam
		
		Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
		self.data = np.random.poisson(self.lam, 500)
	
						
	
	def calculate_mean(self):
	
		"""
		Function to calculate the mean from lam

		Args: 
			None
		
		Returns: 
			float: mean of the data set
	
		"""
		
		self.mean = self.lam
				
		return self.mean



	def calculate_stdev(self):

		"""
		Function to calculate the standard deviation from lam
		
		Args: 
			None
		
		Returns: 
			float: standard deviation of the data set
	
		"""
		
		self.stdev = math.sqrt(self.lam)
		
		return self.stdev
 

	def read_data_file(self, file_name):
	
		"""
		Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute. 
		After reading in the file, the mean and standard deviation are calculated
		
		Args: 
			file_name (string): name of a file to read from
		
		Returns: 
			float: the lam value
	
		"""
		
		Distribution.read_data_file(self, file_name)

		self.lam = 1.0 * sum(self.data)/len(self.data)

		self.mean = self.calculate_mean()
		self.stdev = self.calculate_stdev()
		
		return self.lam

	def plot_raw_data(self):
	
		"""
		Function to output a histogram of the instance variable data using 
		matplotlib pyplot library.
		
		Args:
			None
			
		Returns:
			None
		"""
		plt.hist(self.data)
		plt.title('Histogram of Data')
		plt.xlabel('Data')
		plt.ylabel('Count')
		plt.show()

	def pmf(self, k):

		"""
		Probability mass function calculation for the poisson distribution.
		
		Args:
			k (unsigned int): point for calculating the probability density function
		
		Returns:
			float: probability density function output
		"""

		try:
			assert (isinstance(k, int) or k.is_integer()) and k >= 0, 'k isn\'t a natural number'
		except AssertionError as error:
			raise

		return 1.0 * math.exp(-self.lam)*(self.lam ** k)/math.factorial(k)
		
	def cdf(self, k):

		"""
		Cumulative distribution function calculator for the poisson distribution.
        
        Args:
			k (unsigned float): point for calculating the cumulative distribution function.
        
 		Returns:
			float: cumulative density function output
		"""

		try:
			assert k >= 0, 'isn\'t nonnegative'
		except AssertionError as error:
			raise

		return sum([self.pmf(x) for x in range(int(math.floor(k)) + 1)])

	def plot(self):

		"""
		Function to plot the pmf of the poisson distribution
		
		Args:
			None
		
		Returns:
			list: x values for the both plot
			list: y1 values for the pmf plot
			list: y2 values for the cdf plot
		"""

		x = list(set(self.data))
		x.sort()
		y1 = []
		y2 = []
		
		# calculate the y values to visualize
		for elem in x:
			y1.append(self.pmf(elem))
			y2.append(self.cdf(elem))

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
		
		"""
		Function to add together two Poisson distributions
		
		Args:
			other (Poisson): Poisson instance
			
		Returns:
			Poisson: Poisson distribution
			
		"""
		
		result = Poisson()
		result.lam = self.lam + other.lam
		result.calculate_mean()
		result.calculate_stdev()
		
		return result
		
		
	def __repr__(self):
	
		"""
		Function to output the characteristics of the Poisson instance
		
		Args:
			None
		
		Returns:
			string: characteristics of the Binomial
		
		"""
		
		return "mean = {}, standard deviation = {}, lam = {}".\
		format(self.mean, self.stdev, self.lam)