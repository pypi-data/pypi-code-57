import requests

class taromaruInit():

    def __init__(self, apikey: str):
        self.apikey = apikey

    def image(self, type):
        r = requests.get(f'https://doggo-clicker.000webhostapp.com/api/{type}/', params={
            "apikey": self.apikey
        })
        return r.json()