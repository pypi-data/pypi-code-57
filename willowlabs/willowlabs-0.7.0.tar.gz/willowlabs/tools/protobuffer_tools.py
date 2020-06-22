from google.protobuf.json_format import MessageToDict
from datetime import date, datetime
from typing import Any, Dict, Optional, Union
from willowlabs.service_grpc.company_information import company_information_service_pb2 as pb2


def date_to_pb2_date(d: Union[date, datetime, None]) -> Optional[pb2.Date]:
    if d is None:
        return None
    return pb2.Date(year=d.year, month=d.month, day=d.day)


def to_dict(message, **kwargs: Any) -> Union[Dict[str, Any], date, datetime]:
    class_name = str(message.__class___)[8:-2]
    if class_name.endswith(".Date"):
        return date(year=message.year, month=message.month, day=message.day)
    if class_name.endswith(".Timestamp"):
        return datetime(year=message.year, month=message.month, day=message.day, hour=message.hour,
                        minute=message.minute, second=message.second, microsecond=message.microsecond)
    return MessageToDict(message, **kwargs)
