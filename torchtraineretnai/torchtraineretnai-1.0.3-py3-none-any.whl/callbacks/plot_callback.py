from torchtrainer.callbacks.training_callback import TrainingCallback
from torchtrainer.utils.epochs_plotter import EpochsPlotter

class PlotCallback(TrainingCallback):
	def __init__(self, folder_path, labels_map, columns):
		self.folder_path = folder_path
		self.columns = columns
		self.labels_map = labels_map
		self.epochs_plotter = EpochsPlotter(folder_path=folder_path, labels=labels_map.values(), columns=columns)

	def on_mode_end(self, mode, log):
		for column in self.columns:
			self.epochs_plotter.set(self.labels_map[mode], log['epoch'], column, log[column])
		self.epochs_plotter.save()
		self.epochs_plotter.plot()
