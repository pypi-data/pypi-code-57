import asyncio

from .async_requests import async_make_requests
from .requests_result import RequestsResult


def make_requests(*requests_data) -> RequestsResult:
    return asyncio.run(async_make_requests(*requests_data))
