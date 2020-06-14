from urllib.parse import urlencode


BASE_AUTH_URL = "https://www.urban-rivals.com/ajax/player/account/?"


def create_auth_url(username, password, url):
    """Generates authentication url based on given parameters"""
    url = BASE_AUTH_URL if url is None else url
    form_data = {
        'login': username,
        'password': password,
        'action': 'signin',
        'frompage': ''
    }
    return url + urlencode(form_data)
