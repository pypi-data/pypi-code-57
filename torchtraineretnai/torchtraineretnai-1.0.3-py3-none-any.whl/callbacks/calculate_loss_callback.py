from torchtrainer.callbacks.training_callback import TrainingCallback
from torchnet.meter import AverageValueMeter

class CalculateLossCallback(TrainingCallback):
	def __init__(self, key):
		self.key = key
		self.average_value_meter = AverageValueMeter()

	def on_mode_begin(self, mode, log):
		self.average_value_meter.reset()
		log[self.key] = float('NaN')

	def on_batch_end(self, batch, log):
		batch_size = log['batch_size']
		self.average_value_meter.add(log['loss']*batch_size, batch_size)
		log[self.key] = self.average_value_meter.value()[0]
