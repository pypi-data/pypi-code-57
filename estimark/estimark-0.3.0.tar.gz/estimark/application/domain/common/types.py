from typing import List, Union, Tuple, MutableMapping, Any

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = List[Union[str, TermTuple]]

DataDict = MutableMapping[str, Any]

RecordList = List[DataDict]
