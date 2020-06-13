import torch
from torchnet.meter import AverageValueMeter
#from sklearn.metrics import accuracy_score
from torchtrainer.callbacks.training_callback import TrainingCallback

class CalculateTopNAccuracyCallback(TrainingCallback):
	def __init__(self, keys=('Top-1 accuracy',), topk=(1,)):
		self.keys = keys
		self.topk = topk
		self.average_value_meters = {key: AverageValueMeter() for key in self.keys}
		#self.average_value_meter = AverageValueMeter()

	def on_mode_begin(self, mode, log):
		for key in self.keys:
			self.average_value_meters[key].reset()
			log[key] = float('NaN')

	def on_batch_end(self, batch, log):
		batch_size = log['batch_size']
		gt = log['gt'].to("cpu")
		output = log['output'].to("cpu")
		#accuracy = accuracy_score(gt, output.max(1)[1])
		accuracies = self.calculate_topn_accuracy(output, gt, self.topk)
		for index, accuracy in enumerate(accuracies):
			current_average_value_meter = self.average_value_meters[self.keys[index]]
			current_average_value_meter.add(accuracy.item()*batch_size, batch_size)
			log[self.keys[index]] = current_average_value_meter.value()[0]

	def calculate_topn_accuracy(self, output, target, topk=(1,)):
		"""Computes the accuracy over the k top predictions for the specified values of k"""
		with torch.no_grad():
			maxk = max(topk)
			batch_size = target.size(0)

			_, pred = output.topk(maxk, 1, True, True)
			pred = pred.t()
			correct = pred.eq(target.view(1, -1).expand_as(pred))

			res = []
			for k in topk:
				correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
				res.append(correct_k.mul_(100.0 / batch_size))
			return res
