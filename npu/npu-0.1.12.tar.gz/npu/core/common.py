import hashlib
import requests

from .saving.saving import save_data
from .web.urls import TOKEN_URL, HASH_URL, UPLOAD_DATA_URL
from .Dataset import Dataset

_token = ""


def api(token_):
    global _token
    _token = token_
    params = {"token": _token}
    response = requests.get(TOKEN_URL, params=params)
    if response.status_code == 200:
        print("Token successfully authenticated")
        return response
    else:
        raise ValueError(response.text)
    # "API token not valid"


def getToken():
    return _token


def checkData(data):
    if isinstance(data, (str, dict)):
        return data
    elif isinstance(data, Dataset):
        return data
    else:
        return uploadData(data).json()


def sliceData(data):
    id = data["id"]
    x = data["indexes"]
    y = None
    if isinstance(x, slice):
        y = x.stop
        x = x.start
    return id, x, y


def uploadData(data):
    print("Saving data locally...")
    if isinstance(data, str):
        file = open(data, "rb")
    else:
        file = save_data(data)
    print("Hashing...")
    hash = hashlib.md5(file.read()).hexdigest()
    print("Checking if data is on servers...")
    params = {"token": getToken(), "hash": hash, "collection": 1}
    response = requests.get(HASH_URL, params=params)
    if response.status_code == 200:
        file.close()
        return response
    print("Data not found on servers. Uploading now...")
    file.seek(0)
    files = {'file': file}
    response = requests.post(UPLOAD_DATA_URL, files=files, params=params)
    if isinstance(data, str):
        file.close()
    return response

def hashData(data):
    pass









