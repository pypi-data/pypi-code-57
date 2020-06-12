import requests
import json
import os
from cnvrg.modules.errors import CnvrgError
import cnvrg.helpers.auth_helper as auth_helper
import cnvrg.helpers.logger_helper as logger_helper
from cnvrg.helpers.url_builder_helper import url_join
import urllib
import ssl
from cnvrg.helpers.error_catcher import suppress_exception

JSON_HEADERS = {
    "Content-Type": "application/json"
}

def verify_logged_in():
    if not credentials.logged_in:
        raise CnvrgError("Not authenticated")


def __parse_resp(resp, **kwargs):
    try:
        r_j = resp.json()
        if r_j.get("status") and r_j.get("status") != 200 and r_j.get("message"):
            print(r_j.get("message"))
        return r_j
    except Exception as e:
        logger_helper.log_error(resp.text)
        logger_helper.log_bad_response(**kwargs)
        return {"status": 400, "error": str(e)}


@suppress_exception
def request(action, url, **kwargs):
    callee = getattr(session, action)
    try:
        resp = callee(url, **kwargs)
        return __parse_resp(resp, url=url, **kwargs)
    except Exception as e:
        return {"status": 400, "error": str(e)}

@suppress_exception
def get_v2(url):
    verify_logged_in()
    get_url = url_join(credentials.api_url, "v2", url)
    return requests.get(url=get_url, headers={"Auth-Token": credentials.token})

@suppress_exception
def get(url, data=None):
    verify_logged_in()
    get_url = url_join(base_url, url)
    return request('get', get_url, timeout=420, params=data)


@suppress_exception
def post(url, data=None, files=None):
    verify_logged_in()
    get_url = url_join(base_url, url)
    return request('post', get_url, timeout=900, data=json.dumps(data), files=files)

@suppress_exception
def post_v2(url, data):
    verify_logged_in()
    get_url = url_join(credentials.api_url, "v2", url)
    return requests.post(url=get_url, json=data, headers={"Auth-Token": credentials.token})


@suppress_exception
def send_file(url, data=None, files=None):
    verify_logged_in()
    get_url = url_join(base_url, url)
    resp = requests.post(get_url, files=files, data=data, headers={"AUTH-TOKEN": credentials.token})
    return __parse_resp(resp, url=url, data=data)


@suppress_exception
def put(url, data=None):
    verify_logged_in()
    get_url = url_join(base_url, url)
    return request('put', get_url, timeout=900, data=json.dumps(data))

def download_file(url, fpath):
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(url, fpath)
        return fpath
    except Exception as e:
        print(e)

@suppress_exception
def download_raw_file(url):
    resp = requests.get(url)
    return resp.content

@suppress_exception
def update_credentials(creds):
    global credentials
    credentials = creds
    global session
    session = requests.session()
    session.headers = {
        "AUTH-TOKEN": credentials.token,
        **JSON_HEADERS
    }
    global base_url
    base_url = url_join(credentials.api_url, "v1")


credentials = auth_helper.CnvrgCredentials()
session = requests.session()
session.headers = {
    "AUTH-TOKEN": credentials.token,
    **JSON_HEADERS
}
base_url = url_join(credentials.api_url, "v1")

