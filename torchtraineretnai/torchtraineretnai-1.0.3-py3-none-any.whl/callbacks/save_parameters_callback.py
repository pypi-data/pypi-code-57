import os
import torch
from torchtrainer.callbacks.training_callback import TrainingCallback
from torchtrainer.trainer import Mode

class SaveParametersCallback(TrainingCallback):
	def __init__(self, folder_path):
		self.folder_path = folder_path

	def on_mode_end(self, mode, log):
		if mode==Mode.TRAIN:
			os.makedirs(self.folder_path, exist_ok=True)
			torch.save(self.trainer.model.state_dict(),'{}/epoch-{}.pth'.format(self.folder_path, log['epoch']))
