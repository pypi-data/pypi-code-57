from enum import Enum, auto, unique
import json

###
# Type Definitions
###
class Constants():
    """Constants:  Used wherever a constant value is shared across multiple
       modules or classes
    """
    BOTO3_CLIENT_RETRIES = 5
    EMPTY_DICTIONARY = {}
    EMPTY_LIST = []
    KEY_DIALECT = 'dialect'
    KEY_INPUT = 'input'
    KEY_OPERATION = 'operation'
    KEY_OUTPUT = 'output'
    KEY_RECORDS = 'records'

@unique
class DataDialect(Enum):
    """DataDialect:  The data will be in "DATA_STEWARD" or "CONNECTED_SERVICE" format,
       depending on where it originated
    """
    DATA_STEWARD = auto()
    CONNECTED_SERVICE = auto()
    NONE = auto()

@unique
class SharedDataType(Enum):
    """SharedDataType: The type of the data being synchronized
    """
    USER = "user"
    EVENT = "event"
    OTHER = "other"

@unique
class EventSources(Enum):
    """EventSources:  Enumeration of supported event sources
    """
    QUEUE = auto(),
    TIMER = auto(),
    WEBHOOK = auto(),
    OTHER = auto()

@unique
class Operations(Enum):
    """Operations:  Enumeration of supported operations
    """
    PUSH_TO_SERVICE = auto(),
    PULL_FROM_SERVICE = auto(),
    RECEIVE_FROM_SERVICE = auto(),
    NOOP = auto()


class ServiceConnectorData:
    data: list = []
    timestamp: int = 0
    dialect: DataDialect.NONE

    def __init__(self,
                 data: list,
                 timestamp: int,
                 dialect: DataDialect,
                 source: str,
                 data_type: SharedDataType,
                 receipt_handle: str = None):
        self.data = data
        self.timestamp = timestamp
        self.dialect = dialect
        self.receipt_handle = receipt_handle
        self.source = source
        self.data_type = data_type

###
# Helper functions
###
VALID_OPERATIONS=[item.value for item in Operations]
VALID_DIALECTS=[item.value for item in DataDialect]
def _operation_dialect_factory(operation: Operations, dialect: DataDialect) -> dict:
    """Create the dictionary of operations and dialects use with the various
       input event sources
    
    Arguments:
        operation {Operations} -- The operation to perform
        dialect {DataDialect} -- The dialect of the data
    
    Returns:
        dict -- Dictionary container the operation and dialect
    """
    if not isinstance(operation, Operations) or operation.value not in VALID_OPERATIONS:
        raise ValueError(f'No such operation: {operation}')
    if not isinstance(dialect, DataDialect) or dialect.value not in VALID_DIALECTS:
        raise ValueError(f'No such data dialect: {dialect}')

    return {
        Constants.KEY_OPERATION : operation,
        Constants.KEY_DIALECT: dialect
    }

def _queue_arn_to_url(queue_arn: str) -> str:
    """Change an SQS ARN to its URL
    
    Arguments:
        queue_arn {str} -- The queue ARN
    
    Returns:
        str -- The queue URL
    """
    fields = queue_arn.split(':')
    if len(fields) != 6:
        raise ValueError(f'Expected queue arn {queue_arn} to have 6 fields, but got {json.dumps(fields)}')
    region = fields[3]
    account = fields[4]
    queue_name = fields[5]
    url = f'https://sqs.{region}.amazonaws.com/{account}/{queue_name}'
    return url