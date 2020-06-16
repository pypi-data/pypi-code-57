import math
import matplotlib.pyplot as plt
import numpy as np
from .GeneralDistribution import Distribution

class Gaussian(Distribution):
	""" 
	Gaussian distribution class for calculating and visualizing a Gaussian distribution.
	
	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) representing the standard deviation of the distribution
		data_list (list of floats) a list of floats extracted from the data file
			
	"""
	def __init__(self, mu=0, sigma=1):
		
		Distribution.__init__(self, mu, sigma)
		self.data = np.random.normal(self.mean, self.stdev, 500)

	
	def calculate_mean(self):
	
		"""
		Function to calculate the mean of the data set.
		
		Args: 
			None
		
		Returns: 
			float: mean of the data set
	
		"""
							
		self.mean = 1.0 * sum(self.data)/len(self.data)
		
		return self.mean
		

	def calculate_stdev(self, sample=True):

		""" 
		Function to calculate the standard deviation of the data set.
		
		Args: 
			sample (bool): whether the data represents a sample or population
		
		Returns: 
			float: standard deviation of the data set
	
		"""

		size = len(self.data) - int(sample == True)
		adjusted_data = [(num - self.mean) ** 2 for num in self.data]
		self.stdev = math.sqrt(sum(adjusted_data) / size)

		return self.stdev
		

	def read_data_file(self, file_name, sample=True):
	
		"""
		Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute. 
		After reading in the file, the mean and standard deviation are calculated
				
		Args:
			file_name (string): name of a file to read from
			sample (bool): whether the data represents a sample or population
	
		Returns:
			None
		
		"""
			
		Distribution.read_data_file(self, file_name)
		self.mean = self.calculate_mean()
		self.stdev = self.calculate_stdev(sample)
		
		
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
		
		
	def pdf(self, x):
	
		"""
		Probability density function calculator for the gaussian distribution.
		
		Args:
			x (float): point for calculating the probability density function
			
		
		Returns:
			float: probability density function output
		"""
		
		return (1.0/(self.stdev * math.sqrt(2 * math.pi))) * math.exp(-0.5*((x - self.mean) / self.stdev) ** 2)
		
	def cdf(self, x):
	
		"""
		Cumulative density function calculator for the gaussian distribution.
		
		Args:
			x (float): point for calculating the cumulative density function
			
		
		Returns:
			float: cumulative density function output
		"""
		
		return .5 * (1 + math.erf((x - self.mean)/(self.stdev * math.sqrt(2))))

	def plot(self, n_spaces = 50):

		"""
		Function to plot the normalized histogram of the data and a plot of the 
		probability density function along the same range
		
		Args:
			n_spaces (int): number of data points 
		
		Returns:
            list: x values for the both plot
            list: y1 values for the pmf plot
            list: y2 values for cmf plot
			
		"""

		min_range = min(self.data)
		max_range = max(self.data)
		
		interval = 1.0 * (max_range - min_range) / n_spaces

		x = []
		y1 = []
		y2 = []
		
		for i in range(n_spaces):
			tmp = min_range + interval*i
			x.append(tmp)
			y1.append(self.pdf(tmp))
			y2.append(self.cdf(tmp))

		fig, axes = plt.subplots(3,sharex=True)
		fig.subplots_adjust(hspace=.5)
		
		axes[0].hist(self.data, n_spaces, density=True)
		axes[0].set_title('Normed Histogram of Data')
		axes[0].set_ylabel('Density')

		axes[1].plot(x, y1)
		axes[1].set_title('Probability Distribution of Data')
		axes[1].set_ylabel('Probability Density')

		axes[2].plot(x, y2)
		axes[2].set_title('Cumulative Distribution of Data')
		axes[2].set_ylabel('Probability')

		plt.show()

		return x, y1, y2
		
	def __add__(self, other):
		
		"""
		Function to add together two Gaussian distributions
		
		Args:
			other (Gaussian): Gaussian instance
			
		Returns:
			Gaussian: Gaussian distribution
			
		"""
		
		result = Gaussian()
		
		result.mean = self.mean + other.mean
		result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
		
		return result

	def __sub__(self, other):
		
		"""
		Function to subtract together two Gaussian distributions
		
		Args:
			other (Gaussian): Gaussian instance
			
		Returns:
			Gaussian: Gaussian distribution
			
		"""
		
		result = Gaussian()
		
		result.mean = self.mean - other.mean
		result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
		
		return result	
		
	def __repr__(self):
	
		"""
		Function to output the characteristics of the Gaussian instance
		
		Args:
			None
		
		Returns:
			string: characteristics of the Gaussian
		
		"""
		
		return "mean = {}, standard deviation = {}".format(self.mean, self.stdev)
