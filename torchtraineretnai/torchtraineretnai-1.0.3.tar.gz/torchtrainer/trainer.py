import torch
from tqdm import tqdm
from enum import Enum

class Mode(Enum):
	TRAIN = 1
	EVALUATE = 2
	TEST = 3

class Trainer():
	def __init__(
		self,
		device,
		modes,
		model,
		data_loaders,
		epochs,
		starting_epoch=0,
		optimizer=None,
		criterion=None,
		prepare_batch_fn=None,
		callbacks=[]):

		self.device = device
		self.modes = modes
		self.model = model
		self.data_loaders = data_loaders
		self.epochs = epochs
		self.starting_epoch = starting_epoch
		self.optimizer = optimizer
		self.criterion = criterion
		self.prepare_batch_fn = prepare_batch_fn

		self.is_training = False
		self.b_stop = False
		self.callbacks = callbacks
		self.set_trainer()

	def to(self, device):
		self.device = device

	def __do_mode(self, mode, log):
		with torch.set_grad_enabled(mode==Mode.TRAIN):
			tqdm_data_loader = tqdm(self.data_loaders[mode])
			log['tqdm_bar'] = tqdm_data_loader
			for batch_index, (batch, gt) in enumerate(tqdm_data_loader):
				if self.prepare_batch_fn is not None:
					batch, gt = self.prepare_batch_fn(batch, gt)
				log['batch_index'] = batch_index
				log['batch_size'] = gt.size(0)
				batch = list(batch)
				for i in range(len(batch)):
					batch[i] = batch[i].to(self.device)
				gt = gt.to(self.device)
				self.on_batch_begin(batch_index, log)
				self.model.train(mode==Mode.TRAIN)
				output = self.model(batch)
				loss = self.criterion(output, gt)
				log['loss'] = loss.item()
				if mode==Mode.TRAIN:
					self.optimizer.zero_grad()
					loss.backward()
					self.optimizer.step()
				log['output'] = output
				log['gt'] = gt
				self.on_batch_end(batch_index, log)
				if self.b_stop: break

	def __do_epoch(self, epoch, log):
		for mode in self.modes:
			log['mode'] = mode
			self.on_mode_begin(mode, log)
			self.__do_mode(mode, log)
			self.on_mode_end(mode, log)
			if self.b_stop: break

	def start(self):
		self.is_training = True
		log = {'trainer': self, 'epoch': self.starting_epoch, 'optimizer': self.optimizer}
		self.on_train_begin(log)
		for epoch in range(self.starting_epoch, self.starting_epoch + self.epochs):
			print("Epoch {}".format(epoch), flush=True)
			log['epoch'] = epoch
			self.on_epoch_begin(epoch, log)
			self.__do_epoch(epoch, log)
			self.on_epoch_end(epoch, log)
			if self.b_stop: break
		self.on_train_end(log)
		self.is_training = False
		self.b_stop = False

	def stop(self):
		if not self.b_stop and self.is_training:
			self.b_stop = True

	def set_trainer(self):
		for callback in self.callbacks:
			callback.set_trainer(self)

	def on_train_begin(self, log):
		for callback in self.callbacks:
			callback.on_train_begin(log)

	def on_train_end(self, log):
		for callback in self.callbacks:
			callback.on_train_end(log)

	def on_epoch_begin(self, epoch, log):
		for callback in self.callbacks:
			callback.on_epoch_begin(epoch, log)

	def on_epoch_end(self, epoch, log):
		for callback in self.callbacks:
			callback.on_epoch_end(epoch, log)

	def on_mode_begin(self, mode, log):
		for callback in self.callbacks:
			callback.on_mode_begin(mode, log)

	def on_mode_end(self, mode, log):
		for callback in self.callbacks:
			callback.on_mode_end(mode, log)

	def on_batch_begin(self, batch, log):
		for callback in self.callbacks:
			callback.on_batch_begin(batch, log)

	def on_batch_end(self, batch, log):
		for callback in self.callbacks:
			callback.on_batch_end(batch, log)
