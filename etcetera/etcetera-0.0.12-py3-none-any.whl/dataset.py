import json
from pathlib import Path
from typing import Optional


class Dataset:
    '''Represents locally installed dataset'''

    def __init__(self, location:str, name:Optional[str]=None):
        location = Path(location).resolve()
        self.validate(location)
        self.location = location
        self.name = name or location.name
        self.meta = {}
        if self.file('meta.json').is_file():
            json_text =self._file('meta.json').read_text()
            self.meta.update(json.loads(json_text))

    def file(self, *av):
        '''convenience method to build a file path relative to dataset root.

        Example: ``dataset.file('README.md')``
        '''
        return self.location.joinpath(*av)

    @property
    def data(self):
        '''Path to the data directory within the dataset'''
        return self.file('data')

    def partitions(self):
        '''Returns sorted list of partition names'''
        return sorted(x.name for x in self.data.iterdir())

    def keys(self):
        return set(self.partitions())

    def items(self):
        for p in self.partitions():
            yield p, self[p]

    def values(self):
        for _, v in self.items():
            yield v

    def __len__(self):
        '''Dataset length is the number of partitions'''
        return len(self.keys())

    def __iter__(self):
        yield from self.partitions()

    def __getitem__(self, partition):
        '''Returns :class:`pathlib.Path` object for the partition directory

        Args:
            partition (str): name of the partition

        Example::
            dataset = ...
            partition = dataset['train']

            for filename in partition.iterdir():
                print(filename)
        '''
        p = self.data / partition
        if not p.is_dir():
            raise ValueError(f'Partition {partition} does not exist in dataset {self.name}')
        return p

    def __repr__(self):
        return self.name

    @classmethod
    def validate(cls, path:Path):
        if not path.exists():
            raise ValueError(f'Directory {path} does not exist')

        if not (path / 'data').exists():
            raise ValueError(f'Directory {path} is not a dataset: expect "data/" subdirectory to exist')

        count = 0
        for partition in (path / 'data').iterdir():
            if not partition.is_dir():
                raise ValueError(f'Directory {path} is not a dataset: "data/" must have only partition subdirectories, seen: {partition}')
            count += 1
        if count == 0:
            raise ValueError(f'Directory {path} is not a dataset: "data/" must have at least one partition in it')
