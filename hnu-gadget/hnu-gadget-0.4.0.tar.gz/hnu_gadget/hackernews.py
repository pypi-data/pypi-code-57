import requests


def stories_id():
    API_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'

    with requests.get(API_URL) as response:
        response.raise_for_status()
        return response.json()


def story(id_story):
    API_URL = f'https://hacker-news.firebaseio.com/v0/item/{id_story}.json?print=pretty'

    with requests.get(API_URL) as response:
        response.raise_for_status()
        return response.json()

