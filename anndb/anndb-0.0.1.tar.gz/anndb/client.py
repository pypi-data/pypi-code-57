import grpc

from anndb.dataset_manager import DatasetManager

class Client:

	def __init__(self, addr):
		self._conn = grpc.insecure_channel(addr)
		self._dataset_manager = DatasetManager(self._conn)

	@property
	def datasets(self):
		return self._dataset_manager
	
