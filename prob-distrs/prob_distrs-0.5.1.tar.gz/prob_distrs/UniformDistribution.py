import math
import matplotlib.pyplot as plt
import numpy as np
from .GeneralDistribution import Distribution

class Uniform(Distribution):
	""" 
	Uniform distribution class for calculating and visualizing a Uniform distribution.
	
	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) representing the standard deviation of the distribution
		data (list of floats) a list of floats extracted from the data file
		a (float) lower bound
		b (float) upper bound
			
	"""
	def __init__(self, a=-1, b=1):
		try:
			assert a < b, 'a should be strictly less than b'
		except AssertionError as error:
			raise

		self.a = a
		self.b = b

		Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
		self.data = np.random.uniform(self.a, self.b, 500)

	
	def calculate_mean(self):
	
		"""
		Function to calculate the mean of the data set.
		
		Args: 
			None
		
		Returns: 
			float: mean of the data set
	
		"""
					
		self.mean = (self.a + self.b)/2.0
		
		return self.mean
		

	def calculate_stdev(self):

		"""
		Function to calculate the standard deviation of the data set.
		
		Args: 
			None
		
		Returns: 
			float: standard deviation of the data set
	
		"""

		self.stdev = math.sqrt((self.a - self.b) ** 2 / 12.0)

		return self.stdev
		

	def read_data_file(self, file_name):
	
		"""
		Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute. 
		After reading in the file, the mean and standard deviation are calculated
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			float: a parameter
			float: b parameter
		
		"""
			
		Distribution.read_data_file(self, file_name)

		self.a = min(self.data)
		self.b = max(self.data)

		self.mean = self.calculate_mean()
		self.stdev = self.calculate_stdev()

		return self.a, self.b
		
	def pdf(self, x):
	
		"""
		Probability density function calculator for the uniform distribution.
		
		Args:
			x (float): point for calculating the probability density function
		
		Returns:
			float: probability density function output
		"""
		
		return 1.0/(self.b - self.a) if self.a <= x and x <= self.b else 0
	
	def cdf(self, x):
	
		"""
		Cumulative density function calculator for the uniform distribution.
		
		Args:
			x (float): point for calculating the cumulative density function
		
		Returns:
			float: cumulative density function output
		"""
		if(x < self.a): 
			return 0
		
		return 1.0 * (x - self.a)/(self.b - self.a) if self.a <= x and x <= self.b else 1		

	def plot(self):

		"""
		Function to plot the probability density function
		
		Args:
			None
		
		Returns:
			list: x values for the both plot
			list: y1 values for the pdf plot
			list: y2 values for cdf plot
			
		"""
		x = list(set(self.data))
		x.sort()
		y1 = []
		y2 = []

		for elem in x:
			y1.append(self.pdf(elem))
			y2.append(self.cdf(elem))

		#Make plots
		fig, axes = plt.subplots(3, sharex = True, sharey = True)
		fig.subplots_adjust(hspace = .5)

		np.seterr(divide='ignore', invalid='ignore')
		axes[0].hist(x, bins = int(round(self.b - self.a)), density = True)
		axes[0].set_title("Normed Hisogram of Data")
		axes[0].set_ylabel('Density')
		axes[0].set_xlim([self.a - 1, self.b + 1])
		axes[0].set_xticks([self.a, self.b])
		axes[0].set_ylim([0,1.5])
		axes[0].set_yticks([0,1])
		
		axes[1].plot(x, y1)
		axes[1].set_title('Probability Distribution of Data')
		axes[1].set_ylabel('Probability Density')
		axes[1].axvline(self.a, 0, self.pdf(self.a)/1.5)
		axes[1].axvline(self.b, 0, self.pdf(self.b)/1.5)

		axes[2].plot(x, y2)
		axes[2].set_title('Cumulative Distribution of Data')
		axes[2].set_ylabel('Probability')
		axes[2].axhline(y=0, xmin=0, xmax=self.a/(self.b - self.a + 2))
		axes[2].axhline(y=1, xmin=1.0 * (self.b - self.a + 1)/(self.b - self.a + 2), xmax=1)

		plt.show()

		return x, y1, y2

	def __add__(self, other):
		pass
		
		
	def __repr__(self):
	
		"""
		Function to output the characteristics of the Uniform instance
		
		Args:
			None
		
		Returns:
			string: characteristics of the Uniform
		
		"""
		
		return "mean {}, standard deviation {}, a {}, b {}".format(self.mean, self.stdev, self.a, self.b)

































