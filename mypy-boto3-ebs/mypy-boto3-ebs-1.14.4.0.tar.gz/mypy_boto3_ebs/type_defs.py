"""
Main interface for ebs service type definitions.

Usage::

    ```python
    from mypy_boto3_ebs.type_defs import BlockTypeDef

    data: BlockTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BlockTypeDef",
    "ChangedBlockTypeDef",
    "GetSnapshotBlockResponseTypeDef",
    "ListChangedBlocksResponseTypeDef",
    "ListSnapshotBlocksResponseTypeDef",
)

BlockTypeDef = TypedDict("BlockTypeDef", {"BlockIndex": int, "BlockToken": str}, total=False)

ChangedBlockTypeDef = TypedDict(
    "ChangedBlockTypeDef",
    {"BlockIndex": int, "FirstBlockToken": str, "SecondBlockToken": str},
    total=False,
)

GetSnapshotBlockResponseTypeDef = TypedDict(
    "GetSnapshotBlockResponseTypeDef",
    {
        "DataLength": int,
        "BlockData": IO[bytes],
        "Checksum": str,
        "ChecksumAlgorithm": Literal["SHA256"],
    },
    total=False,
)

ListChangedBlocksResponseTypeDef = TypedDict(
    "ListChangedBlocksResponseTypeDef",
    {
        "ChangedBlocks": List["ChangedBlockTypeDef"],
        "ExpiryTime": datetime,
        "VolumeSize": int,
        "BlockSize": int,
        "NextToken": str,
    },
    total=False,
)

ListSnapshotBlocksResponseTypeDef = TypedDict(
    "ListSnapshotBlocksResponseTypeDef",
    {
        "Blocks": List["BlockTypeDef"],
        "ExpiryTime": datetime,
        "VolumeSize": int,
        "BlockSize": int,
        "NextToken": str,
    },
    total=False,
)
