import time
from enum import auto
from typing import List

from jsonrpcclient.clients.http_client import HTTPClient

import logging
from common.cs_enum import AutoName

DEFAULT_LEDGER_BOOK_ID = "1"

log = logging.getLogger(__name__)


class OperationType(AutoName):
    TRANSFER = auto()


class OperationStatus(AutoName):
    INIT = auto()
    PROCESSING = auto()
    APPLIED = auto()
    REJECTED = auto()


class LedgerClient:
    def __init__(self, ledger_endpoint: str, ledger_read_only_endpoint: str = None):
        self.rpc_client = HTTPClient(ledger_endpoint)
        if ledger_read_only_endpoint is not None:
            self.read_only_rpc_client = HTTPClient(ledger_read_only_endpoint)

    def _execute(self, method: str, *args, read_only_method: bool = False):
        start_time = int(time.time()*1000)
        if read_only_method is True and getattr(self, "read_only_rpc_client", None) is not None:
            rpc_response = self.read_only_rpc_client.request(method, *args)
        else:
            rpc_response = self.rpc_client.request(method, *args)
        end_time = int(time.time()*1000)
        log.info(f"LedgerClient: {method}: time_taken: {end_time-start_time}ms")
        return rpc_response.data.result

    def create_book(self, name: str, min_balance: str = None, metadata: dict = None):
        book_info = dict()
        book_info["name"] = name
        book_info["metadata"] = metadata
        if min_balance:
            book_info["restrictions"] = dict()
            book_info["restrictions"]["minBalance"] = min_balance
        return self._execute("createBook", book_info)

    def get_book(self, book_id: str):
        return self._execute("getBook", book_id, read_only_method=True)

    def get_book_balances(self, book_id: str, asset_id: str = None, metadata_filter: dict = None):
        return self._execute("getBalances", book_id, asset_id, metadata_filter, read_only_method=True)

    def get_operation(self, operation_id: str):
        return self._execute("getOperation", operation_id, read_only_method=True)

    def get_operations(self, book_id: str, metadata_filter: dict = None):
        return self._execute("getOperations", book_id, metadata_filter, read_only_method=True)

    def post_operation(self, operation_type: OperationType, entries: List[dict], memo: str = "", metadata: dict = None, sync: bool = False):
        operation = dict()
        operation["type"] = operation_type.value
        operation["entries"] = entries
        operation["memo"] = memo
        if metadata: operation["metadata"] = metadata
        return self._execute("postOperation", operation, sync)

    def post_transfer(self, from_book_id: str, to_book_id: str, asset_id: str, value: str, memo: str = "", metadata: dict = None, sync: bool = False):
        transfer = dict()
        transfer["fromBookId"] = from_book_id
        transfer["toBookId"] = to_book_id
        transfer["assetId"] = asset_id
        transfer["value"] = value
        transfer["memo"] = memo
        if metadata: transfer["metadata"] = metadata
        return self._execute("postTransfer", transfer, sync)

    def post_transfer_sync(self, from_book_id: str, to_book_id: str, asset_id: str, value: str, memo: str = "", metadata: dict = None):
        result = self.post_transfer(from_book_id=from_book_id, to_book_id=to_book_id, asset_id=asset_id, value=value, memo=memo, metadata=metadata, sync=True)
        if result["status"] == OperationStatus.REJECTED.value:
            raise Exception(result["rejectionReason"])
        return result

