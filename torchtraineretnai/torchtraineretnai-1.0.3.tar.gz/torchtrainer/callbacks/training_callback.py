from abc import ABC

class TrainingCallback(ABC):

	def set_trainer(self, trainer):
		self.trainer = trainer

	def on_train_begin(self, log):
		pass

	def on_train_end(self, log):
		pass

	def on_epoch_begin(self, epoch, log):
		pass

	def on_epoch_end(self, epoch, log):
		pass

	def on_mode_begin(self, mode, log):
		pass

	def on_mode_end(self, mode, log):
		pass

	def on_batch_begin(self, batch, log):
		pass

	def on_batch_end(self, batch, log):
		pass
