from bs4 import BeautifulSoup


def execute_http_call(session, url):
    """Executes an http call with the given session and url"""
    return session.get(url)


def convert_html_to_soup(response):
    """Converts a Response object into BeautifulSoup"""
    return BeautifulSoup(response.text, 'html.parser')
