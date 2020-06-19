import asyncio
from logging import getLogger
from time import time
from typing import Optional, List
from uuid import uuid4

import aiohttp
from aiohttp import ClientSession, ClientConnectorError

from .request_data import RequestData
from .requests_result import RequestsResult
from .response_data import ResponseData

logger = getLogger()
ASYNCIO_SEMAPHORE = 1024


async def async_make_requests(*requests_data) -> RequestsResult:
    call_id = str(uuid4()).replace('-', '')

    requests_data: List[RequestData] = [RequestData.make(req) for req in requests_data]
    semaphore = asyncio.Semaphore(ASYNCIO_SEMAPHORE)
    results = list()
    tasks = list()
    start_at = time()

    requests_data_expanded = list()

    for req in requests_data:
        for i in range(req.count):
            requests_data_expanded.append(dict(method=req.method,
                                               url=req.url,
                                               json=req.json,
                                               headers=req.headers))

    requests_count = len(requests_data_expanded)
    requests_id_len = len(str(requests_count))

    async with ClientSession() as session:
        for i in range(requests_count):
            method = requests_data_expanded[i]['method']
            url = requests_data_expanded[i]['url']
            request_id = f'{call_id} | {i+1:0>{requests_id_len}}'
            task = asyncio.create_task(_request_fetch(session=session,
                                                      semaphore=semaphore,
                                                      method=method,
                                                      url=url,
                                                      headers=requests_data_expanded[i]['headers'],
                                                      json=requests_data_expanded[i]['json'],
                                                      request_id=request_id))
            # bodies_size += getsizeof(dumps(req.json)) if req.json is not None else 0
            tasks.append(task)
        await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
        # await asyncio.gather(*tasks)
        results = [task.result() for task in tasks]

    result = RequestsResult(responses=results,
                            elapsed=time()-start_at)
    logger.info(f'[ {call_id} ] ASYNC REQUESTS RESULT:\n'
                f'  Requests count: {len(result.responses)}\n'
                f'  Elapsed time:   {result.elapsed} seconds\n'
                f'  Average time:   {result.average} seconds\n'
                f'  Statuses:       {result.status_codes}\n'
                f'  Failed:         {result.failed}')

    return result


async def _request_fetch(session: ClientSession,
                         semaphore: asyncio.Semaphore,
                         method: str,
                         url: str,
                         headers: Optional[dict] = None,
                         json: Optional[dict] = None,
                         request_id: Optional[str] = None) -> Optional[ResponseData]:

    async with semaphore:
        started_at = time()
        logger.info(f'[ {request_id} ] -> start task with {method} request to {url}')
        # headers = {'Content-Type': 'application/json'}  if json else None

        try:
            async with session.request(method=method,
                                       url=url,
                                       json=json,
                                       headers=headers,
                                       ssl=False) as response:
                await response.read()

        except asyncio.TimeoutError as err:
            logger.warning(f'[ {request_id} ] {err.__class__.__name__} {url}')
            return ResponseData(exception=err, url=url, started_at=started_at)
        except ClientConnectorError as err:
            logger.warning(f'[ {request_id} ] {err.__class__.__name__} {url}')
            return ResponseData(exception=err, url=url, started_at=started_at)

    finished_at = time()
    logger.info(f'[ {request_id} ] <- receive response from {url} ({finished_at-started_at:.3f} sec.)')

    response_data = ResponseData(response=response,
                                 url=url,
                                 started_at=started_at,
                                 finished_at=finished_at)
    response_data.text = await response.text()
    response_data.json = None

    try:
        response_data.json = await response.json()
    except aiohttp.ContentTypeError:
        logger.warning(f'[ {request_id} ] is not JSON response ({response.status} {response.reason})')

    return response_data
