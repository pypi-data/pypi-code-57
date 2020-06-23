"""For some reason I don't understand, this only works if I do "python3 -m pytest" """
from tvguiden import tvguiden
import requests


def test_baseurl():
    response = requests.head(url=tvguiden._baseURL)
    assert response.ok


