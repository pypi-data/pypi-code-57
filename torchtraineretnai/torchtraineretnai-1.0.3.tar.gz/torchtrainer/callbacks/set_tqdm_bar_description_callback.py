from torchtrainer.callbacks.training_callback import TrainingCallback

class SetTQDMBarDescriptionCallback(TrainingCallback):
	def __init__(self, keys=["Loss", "Accuracy"]):
		self.keys = keys

	def on_mode_end(self, mode, log):
		log['tqdm_bar'].refresh()
		log['tqdm_bar'].close()

	def on_batch_end(self, batch, log):
		#description = "{}:\t".format(log['mode'])
		description = ""
		for key in self.keys:
			description+="{} = {:0.4f} ".format(key, log[key])
		log['tqdm_bar'].set_description(description)
