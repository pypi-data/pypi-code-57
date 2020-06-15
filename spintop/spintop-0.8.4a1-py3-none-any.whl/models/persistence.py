""" Base models that allow persistency and indexing using the spintop.persistence modules.
"""
from datetime import datetime
from collections import OrderedDict
from typing import List, Dict, Optional, Any, NamedTuple

from .base import BaseDataClass, model_property, model_attribute, DefaultPrimitiveView
from .serialization import SerializedWrapper, TYPE_KEY, ValidationError
from .queries import BaseQuery
from .meta import FieldsOf
from .view import DataClassPrimitiveView

from spintop.utils import utcnow_aware, is_aware, dict_ops, is_valid_py_identifier

def validate_tags_are_py_identifers(tags):
    for key in tags:
        if not is_valid_py_identifier(key):
            raise ValidationError(f'{key!r} is not a valid python identifier.')

class PersistenceIDRecord(BaseDataClass):
    uuid: str
    is_deleted: bool = False
    tags: Dict[str, Optional[Any]] = model_attribute(dict, validators=[validate_tags_are_py_identifers])
    start_datetime: datetime = utcnow_aware

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.start_datetime and not is_aware(self.start_datetime):
            raise ValueError('Please provide a tz-aware datetime.')


class PersistenceRecord(BaseDataClass):
    # Common to all
    uuid: str = model_property(fget=lambda record: record.index.uuid)

    # Same attributes, type should be changed by sub classes.
    index: PersistenceIDRecord = None
    data: BaseDataClass = None

class SerializedPersistenceRecord(SerializedWrapper):
    pass

index_fields = PersistenceIDRecord.fields()

class PersistenceRecordCollection(BaseDataClass):
    records: List[PersistenceRecord] = list

    def __init__(self, records=None):
        records = list(records) if records else []
        super().__init__(records=sorted(records, key=lambda record: index_fields.uuid.get_value(record.index)))
    
    @property
    def collector(self):
        return self.add_record

    def add_record(self, record):
        self.records.append(record)
        
    def apply(self, *fns):
        for record in self.iter_records():
            for fn in fns:
                fn(record)
                
    def iter_records(self):
        for record in self.records:
            yield record
                
    def count_unique(self, key=lambda record: record.uuid):
        occurances = set()
        self.apply(lambda record: occurances.add(key(record)))
        return len(occurances)
            
    def sort(self, key=lambda record: record.index.start_datetime):
        self.records.sort(key=key)
        
    def __eq__(self, other):
        return self.records == other.records

index_fields = PersistenceIDRecord.fields()

class Query(BaseQuery):
    
    def default_parts(self):
        yield index_fields.is_deleted == False


class PersistenceRecordView(object):
    data_prefix = ('data',)
    index_prefix = ()
    default_view = DefaultPrimitiveView()
    
    def __init__(self, data_view=None, include_index=True, include_data=True, data_prefix=None, index_prefix=None):
        self.include_index = include_index
        self.include_data = include_data

        if data_view:
            self.data_view = DataClassPrimitiveView(data_view)
        else:
            self.data_view = None

        if data_prefix is not None:
            self.data_prefix = data_prefix
        
        if index_prefix is not None:
            self.index_prefix = index_prefix

    def apply(self, record, flatten_dict=True):
        result = OrderedDict()
        
        if self.include_index:
            index_data = self.apply_index(record, flatten_dict=flatten_dict, key_prefix=self.index_prefix)
            dict_ops.update(result, index_data)
        
        if self.data_view:
            data = self.apply_data(record, flatten_dict=flatten_dict, key_prefix=self.data_prefix)
            dict_ops.update(result, data)
        
        result = dict_ops.replace_defaults(result)

        return result
    
    def apply_index(self, record, **apply_kwargs):
        return self.default_view.apply(record.index, **apply_kwargs)

    def apply_data(self, record, **apply_kwargs):
        return self.data_view.apply(record.data, **apply_kwargs)
    