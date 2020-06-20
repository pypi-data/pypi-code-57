from uuid import UUID

from typing import List, Iterator, Tuple, Mapping

from anndb.dataset_pb2_grpc import DataManagerStub
from anndb.search_pb2_grpc import SearchStub
from anndb.dataset_pb2 import Dataset as DatasetPb, InsertRequest, RemoveRequest, BatchRequest, BatchItem
from anndb.search_pb2 import SearchRequest

class Dataset:

	def __init__(self, data_manager_stub:DataManagerStub, search_stub:SearchStub, proto:DatasetPb):
		self._data_manager_stub = data_manager_stub
		self._search_stub = search_stub
		self._proto = proto

	@property
	def id(self):
		return UUID(bytes=self._proto.id)

	@property
	def proto(self):
		return self._proto

	def insert(self, id:int, value:List[float], metadata:Mapping[str,str] = {}):
		return self._data_manager_stub.Insert(InsertRequest(
			dataset_id=self.proto.id,
			id=id,
			value=value,
			metadata=metadata
			))

	def batch_insert(self, items:List[Tuple[int, List[float], Mapping[str,str]]]):
		return self._data_manager_stub.BatchInsert(BatchRequest(
			dataset_id=self.proto.id,
			items=list(map(
				lambda t: BatchItem(id=t[0], value=t[1], metadata=t[2]),
				items
				))
			))

	def remove(self, id:int):
		return self._data_manager_stub.Remove(RemoveRequest(
			dataset_id=self.proto.id,
			id=id,
			))

	def batch_remove(self, ids:List[int]):
		return self._data_manager_stub.BatchRemove(BatchRequest(
			dataset_id=self.proto.id,
			items=list(map(
				lambda id: BatchItem(id=id),
				ids
				))
			))

	def search(self, query:List[float], k:int) -> Iterator[Tuple[int, Mapping[str,str], float]]:
		request = SearchRequest(dataset_id=self.proto.id, query=query, k=k)

		for item in self._search_stub.Search(request):
			yield (item.id, item.metadata, item.score)