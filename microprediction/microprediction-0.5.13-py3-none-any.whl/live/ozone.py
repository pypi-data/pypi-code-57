import requests

from microprediction.config_private import UV_KEY

import requests
headers = {
    'x-access-token': UV_KEY,
}
params = (
    ('lat', '41.08'),
    ('lng', '-73.50'),
    ('dt', '2018-01-24T10:50:52.283Z'),
)

def ozone():
    response = requests.get('https://api.openuv.io/api/v1/uv', headers=headers, params=params)
    return float(response.json()['result']['ozone'])/1000.

if __name__=="__main__":
    data = ozone()
    print(data)