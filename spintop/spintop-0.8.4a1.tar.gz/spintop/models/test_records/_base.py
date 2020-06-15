""" Storage-friendly internal data classes. """
import numbers

from collections import defaultdict
from collections.abc import Mapping
from base64 import urlsafe_b64decode, urlsafe_b64encode
from uuid import UUID, uuid4

from datetime import datetime
from dataclasses import dataclass, fields, _MISSING_TYPE, MISSING, field, asdict
from typing import Union, List, Optional

from ..serialization import cls_of_obj

from ..base import (
    BaseDataClass, 
    _fields_cache,
    model_property
)

from ..persistence import PersistenceIDRecord

from ..view import ComplexPrimitiveView

from spintop.utils import isnan, utcnow_aware

NAME_SEPARATOR = ':'
NO_VERSION = 'none'

def create_uuid():
    return uuid4()

def uuid_to_slug(uuidstring):
    try:
        uuid = UUID(uuidstring)
    except AttributeError:
        uuid = uuidstring
    
    return urlsafe_b64encode(uuid.bytes).rstrip(b'=').decode('ascii')

def test_uuid_generator(testbench_record=None, start_datetime=None, dut_record=None):
    datetime_format = None

    if start_datetime:
        datetime_format = start_datetime.strftime("%Y%m%d-%H%M%S-%f")

    if not datetime_format:
        # Not enough info for unique id. Generate one.
        value =  uuid_to_slug(create_uuid())
    else:
        value =  f"{str(testbench_record)}.{datetime_format}"

    if dut_record.id:
        value = f"{value}.{dut_record.id}-{dut_record.version}"
    
    return value
    

def slug_to_uuid(slug):
    return str(UUID(bytes=urlsafe_b64decode(slug + '==')))

def compute_stats(features):
    name_tuple_to_count_map = defaultdict(int)

    for feature in features:
        # For feature ('x', 'y', 'z'), increment ('x',), ('x', 'y') and ('x', 'y', 'z')
        name_tuple = feature.name_tuple

        for i in range(1, len(name_tuple)):
            sub_name = name_tuple[:i]
            name_tuple_to_count_map[sub_name] += 1

    for feature in features:
        feature.feature_count = name_tuple_to_count_map[feature.name_tuple]


class VersionIDRecord(BaseDataClass):
    id: Optional[str]
    version: Optional[str]
    
    @classmethod
    def create(cls, id_or_dict, version=None):
        if isinstance(id_or_dict, cls):
            return id_or_dict
        if isinstance(id_or_dict, Mapping):
            id = id_or_dict.get('id', None)
            version = id_or_dict.get('version', None)
        else:
            id = id_or_dict
            
        if version is None:
            version = NO_VERSION
            
        return cls(
            id=id,
            version=version
        )
        
    def match(self, other):
        id_match = self.id == other.id if self.id is not None else True
        version_match = self.version == other.version if self.version is not None else True
        return id_match and version_match

    def __str__(self):
        if self.version and self.version != NO_VERSION:
            return f'{self.id}-{self.version}'
        elif self.id:
            return str(self.id)
        else:
            return 'default'

class TestbenchIDRecord(VersionIDRecord):
    pass

class DutIDRecord(VersionIDRecord):
    pass

class OutcomeData(BaseDataClass):
    message: str = ''
    is_pass: bool = True
    is_skip: bool = False
    is_abort: bool = False
    is_ignore: bool = False
    
    def __bool__(self):
        return self.is_pass and not self.is_abort

    @classmethod
    def create(cls, outcome):
        if isinstance(outcome, cls):
            pass # already correct type
        elif isinstance(outcome, bool):
            outcome = cls(is_pass=outcome)
        elif isinstance(outcome, Mapping):
            outcome = cls(**outcome)
        else:
            raise TypeError((
    'Outcome (%s) should either be a boolean that indicates if this test passed or failed, ' 
    'or a dictionnary of one or more of the following attributes: %s'
            ) % (outcome, [f.name for f in cls.dataclass_fields()]))
        return outcome

    def impose_upon(self, other_outcome):
        if not self.is_ignore:
            # Pass propagates by falseness. False will propagate up, not True
            other_outcome.is_pass = other_outcome.is_pass and self.is_pass

            # Abort propagates by trueness. True will propagate up, not False
            other_outcome.is_abort = other_outcome.is_abort or self.is_abort

            # Abort propagates by trueness. True will propagate up, not False
            other_outcome.is_skip = other_outcome.is_skip or self.is_skip

class FeatureRecordNoData(BaseDataClass):
    """ Feature ID is determined by its name.
    """
    oid: Optional[str]
    name: Optional[str] = ''
    description: str = ''
    version: int = 0
    depth: int = 0
    index: int = 0
    ancestors: List[str] = list
    original: bool = True
    
    @classmethod
    def defaults(cls, **others):
        others['name'] = others.get('name', '')
        others['ancestors'] = others.get('ancestors', [])
        return super().defaults(**others)

    @classmethod
    def data_dataclass_fields(cls):
        """ The data fields are all fields except the ones declare up to this cls
        in the cls MRO.
        
        If a subclass defines only a dataclass field 'foo', this method will return
        foo only as a data field.
        """
        return set(_fields_cache.retrieve(cls)) - set(_fields_cache.retrieve(FeatureRecordNoData))
    
    @property
    def name_tuple(self):
        return tuple(self.ancestors) + (self.name,)

    @property
    def complete_name(self) -> str:
        return NAME_SEPARATOR.join(self.name_tuple)
    
class FeatureRecord(FeatureRecordNoData):
    user_data: dict = dict
    outcome: OutcomeData = OutcomeData
    feature_count: int = 0 # Number of children
    
    def __post_init__(self):
        super().__post_init__()
        self.outcome = OutcomeData.create(self.outcome)

    @property
    def total_feature_count(self):
        return self.feature_count

    @classmethod
    def defaults(cls, **others):
        others['user_data'] = others.get('user_data', {})
        others['feature_count'] = others.get('feature_count', 0)
        return super(FeatureRecord, cls).defaults(**others)
    
class PhaseFeatureRecord(FeatureRecord):
    duration: Optional[float] = None
    
class TestIDRecord(PersistenceIDRecord, PhaseFeatureRecord):
    testbench: TestbenchIDRecord = TestbenchIDRecord
    station: TestbenchIDRecord = TestbenchIDRecord
    dut: DutIDRecord = DutIDRecord
    operator: str = ''
    stage: str = 'prod'

    def __post_init__(self):
        super().__post_init__()
        self.dut = DutIDRecord.create(self.dut)
        self.testbench = TestbenchIDRecord.create(self.testbench)
        self.station = TestbenchIDRecord.create(self.station)
        
        for key, value in self.tags.items():
            self.add_tag(key, value)

        if self.uuid is None:
            self.uuid = test_uuid_generator(self.testbench, self.start_datetime, self.dut)

    @property
    def testbench_name(self) -> Optional[str]:
        return self.testbench.id

    @testbench_name.setter
    def testbench_name(self, value):
        self.testbench.id = value

    def add_tag(self, key, value=True):
        self.tags[key] = tag_value_sanitizer(value)
        
    def remove_tag(self, key):
        del self.tags[key]

TestRecordSummary = TestIDRecord # backward compat

def tag_value_sanitizer(value):
    if isinstance(value, float) and isnan(value):
        # NaN to None.
        value = None

    return value

class MeasureFeatureRecord(FeatureRecord):
    value_f: Optional[float]
    value_s: Optional[str]

    @property
    def value(self) -> Union[float, str, None]:
        if self.value_f is not None:
            return self.value_f
        else:
            return self.value_s

    @value.setter
    def value(self, value):
        if value is None or isinstance(value, str):
            self.value_f = None
            self.value_s = value
        elif isinstance(value, numbers.Number):
            self.value_f = value
            self.value_s = None
        else:
            raise ValueError('Only string or numeric types are supported. Received {!r} of type {}'.format(value, type(value)))
    
class DutOp(BaseDataClass):
    dut_match: DutIDRecord
    dut_after: DutIDRecord
    op_datetime: datetime = utcnow_aware
    
    @classmethod
    def create(cls, dut_match, dut_after, op_datetime):
        return cls(
            dut_match=DutIDRecord.create(dut_match),
            dut_after=DutIDRecord.create(dut_after),
            op_datetime=op_datetime
        )
    
    def does_applies_to(self, dut, on_datetime):
        return self.dut_match.match(dut) and self.op_datetime < on_datetime
    
    def apply_or_return(self, dut, on_datetime):
        if self.does_applies_to(dut, on_datetime):
            return self.apply(dut)
        else:
            return dut
        
    def apply(self, dut):
        """Apply op to dut. Does not check for datetime. """
        new_dut = self.dut_after.copy()
        if new_dut.id is None:
            new_dut.id = dut.id
        return new_dut
        