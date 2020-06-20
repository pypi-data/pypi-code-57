from typing import Dict, Optional, Any
import time, requests, os
from enum import Enum

from fake_useragent import FakeUserAgent

Response = requests.Response

def download(
    url: str,
    path: str,
    max_request_try_count: int = 3,
    sleep_time: float = 2.5,
    debug: bool = False
) -> bool:
    current_try_count = 0

    while current_try_count < max_request_try_count:
        current_try_count += 1

        if debug:
            print(url + ' | ' + str(current_try_count) + '/' + str(max_request_try_count))
        
        res = __download(
            url,
            path,
            debug=debug
        )

        if res:
            return True
        
        time.sleep(sleep_time)
    
    return False

def __download(
    url: str, 
    path: str,
    debug: bool = False
) -> bool:
    import urllib

    try:
        urllib.request.urlretrieve(url, path)

        return os.path.exists(path)
    except Exception as e1:
        if debug:
            print(e1)
        
        try:
            os.remove(path)
        except Exception as e2:
            if debug:
                print(e2)
        
        return False

class RequestMethod(Enum):
    GET     = 'GET'
    POST    = 'POST'
    DELETE  = 'DELETE'

def request(
    url: str,
    method: RequestMethod = RequestMethod.GET,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    data: Optional[Any] = None,
    max_request_try_count: int = 10,
    sleep_time: float = 2.5,
    debug: bool = False,
    fake_useragent: bool = False
) -> Optional[Response]:
    current_try_count = 0

    while current_try_count < max_request_try_count:
        current_try_count += 1

        if debug:
            print(url + ' | ' + str(current_try_count) + '/' + str(max_request_try_count))

        resp = __request(
            url, method,
            params=params,
            headers=headers,
            data=data,
            debug=debug,
            fake_useragent=fake_useragent
        )

        if resp is not None:
            return resp

        time.sleep(sleep_time)
    
    return None

def get(
    url: str,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    max_request_try_count: int = 10,
    sleep_time: float = 2.5,
    debug: bool = False,
    fake_useragent: bool = False
) -> Optional[Response]:
    return request(url, method=RequestMethod.GET, params=params, headers=headers, max_request_try_count=max_request_try_count, sleep_time=sleep_time, debug=debug, fake_useragent=fake_useragent)

def post(
    url: str,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    data: Optional[Any] = None,
    max_request_try_count: int = 10,
    sleep_time: float = 2.5,
    debug: bool = False,
    fake_useragent: bool = False
) -> Optional[Response]:
    return request(url, method=RequestMethod.POST, params=params, headers=headers, data=data, max_request_try_count=max_request_try_count, sleep_time=sleep_time, debug=debug, fake_useragent=fake_useragent)

def delete(
    url: str,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    data: Optional[Any] = None,
    max_request_try_count: int = 10,
    sleep_time: float = 2.5,
    debug: bool = False,
    fake_useragent: bool = False
) -> Optional[Response]:
    return request(url, method=RequestMethod.DELETE, params=params, headers=headers, data=data, max_request_try_count=max_request_try_count, sleep_time=sleep_time, debug=debug, fake_useragent=fake_useragent)

def __request(
    url: str,
    method: RequestMethod,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    data: Optional[Any] = None,
    debug: bool = False,
    fake_useragent: bool = False
) -> Optional[Response]:
    if headers is None:
        headers = {}

    if fake_useragent:    
        headers = __headers_by_optionally_setting(
            headers,
            {
                'User-Agent':FakeUserAgent().random,
                'Accept':'*/*',
                'Cache-Control':'no-cache',
                'Accept-Encoding':'gzip, deflate, br',
                'Connection':'keep-alive'
            }
        )

    try:
        if method == RequestMethod.GET:
            resp = requests.get(url, params=params, headers=headers)
        elif method == RequestMethod.POST:
            resp = requests.post(url, data=data, params=params, headers=headers)
        else:#elif method == RequestMethod.DELETE:
            resp = requests.post(url, data=data, params=params, headers=headers)

        if resp is None:
            if debug:
                print('Response is None')
        elif resp.status_code not in [200, 201]:
            if debug:
                print(resp.status_code, resp.text)

            return None

        return resp
    except Exception as e:
        if debug:
            print('ERROR:', e)

        return None

def __headers_by_optionally_setting(
    headers: Dict, 
    keys_values: Dict
) -> Dict:
    for key, value in keys_values.items():
        if key not in headers:
            headers[key] = value
    
    return headers