

class ProjectDataset():
    '''

    '''

    def __init__(self, client, name=None, datasetType=None, datasetId=None, streamingDatasetId=None):
        self.client = client
        self.id = None
        self.name = name
        self.dataset_type = datasetType
        self.dataset_id = datasetId
        self.streaming_dataset_id = streamingDatasetId

    def __repr__(self):
        return f"ProjectDataset(name={repr(self.name)}, dataset_type={repr(self.dataset_type)}, dataset_id={repr(self.dataset_id)}, streaming_dataset_id={repr(self.streaming_dataset_id)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'name': self.name, 'dataset_type': self.dataset_type, 'dataset_id': self.dataset_id, 'streaming_dataset_id': self.streaming_dataset_id}
