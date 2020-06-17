from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple, Union

KwargsType = Union[
    Mapping[
        Union[str, bytes, int, float],
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    str,
    bytes,
    None,
    Tuple[
        Union[str, bytes, int, float],
        Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        str, Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        bytes, Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        int, Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
    Mapping[
        float, Union[str, bytes, int, float, Iterable[Union[str, bytes, int, float]]],
    ],
]

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]

ListOutputType = List[Union[str, int, float, bool, List[Union[str, int, float, bool]]]]

DictOutputType = List[Dict[str, Union[str, int, float, bool]]]

ParamsType = Optional[
    Dict[str, Union[str, int, float, bool, Iterable[Union[str, int, float, bool]]]]
]
