"""
Main interface for macie2 service.

Usage::

    ```python
    import boto3
    from mypy_boto3_macie2 import (
        Client,
        Macie2Client,
    )

    session = boto3.Session()

    client: Macie2Client = boto3.client("macie2")
    session_client: Macie2Client = session.client("macie2")
    ```
"""
from mypy_boto3_macie2.client import Macie2Client

Client = Macie2Client


__all__ = ("Client", "Macie2Client")
