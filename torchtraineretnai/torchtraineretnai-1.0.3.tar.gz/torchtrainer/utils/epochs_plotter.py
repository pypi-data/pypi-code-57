import os
import glob
import pandas as pd
import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

class EpochsPlotter:
	def __init__(self, folder_path, labels=None, columns=None, load=True):
		self.folder_path = folder_path
		self.exp_name = os.path.basename(os.path.normpath(folder_path))
		self.dataframes = {}
		if not os.path.exists(self.folder_path):
			load = False
		if load:
			if os.path.exists(self.folder_path):
				dataframe_paths = glob.glob(os.path.join(self.folder_path, "*.csv"))
				self.labels = [os.path.basename(os.path.splitext(x)[0]) for x in dataframe_paths]
			else:
				raise Exception("{} folder does not exists".format(self.folder_path))
			if not self.labels:
				raise Exception("{} folder does not contain any csv file".format(self.folder_path))
			for label, path in zip(self.labels, dataframe_paths):
				self.dataframes[label] = pd.read_csv(path, index_col='Epoch')
			self.columns = list(self.dataframes[label].columns)
		else:
			self.labels = labels
			self.columns = columns
			for label in self.labels:
				self.dataframes[label] = pd.DataFrame(columns=self.columns, dtype=float)
				self.dataframes[label].index.name = "Epoch"

	def save(self):
		os.makedirs(self.folder_path, exist_ok=True)
		for label in self.labels:
			csv_path = os.path.join(self.folder_path, "{}.csv".format(label))
			self.dataframes[label].to_csv(csv_path)

	def plot(self, show=False):
		for column in self.columns:
			fig, ax = plt.subplots(figsize=(16, 10))
			fig.suptitle(self.exp_name)
			for label in self.labels:
				ax.plot(self.dataframes[label][column], label=label)
			ax.set(xlabel='Epoch', ylabel=column, title=column)
			ax.grid()
			ax.legend()
			ax.xaxis.set_major_locator(MaxNLocator(integer=True))
			plot_path = os.path.join(self.folder_path, "{}.png".format(column))
			fig.savefig(plot_path)
			if show:
				plt.show()
			plt.close()

	def set_row(self, label, epoch, row):
		self.dataframes[label].loc[epoch] = pd.Series(data=row, name=epoch)

	def set(self, label, epoch, column, value):
		self.dataframes[label].at[epoch, column] = value
