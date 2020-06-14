import json
import sys

import argparse
import requests

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

DEBUG = False


def initial_search(search_phrase: 'str', search_url: str, inpunt_id: str, result_tag_class: str = "result__a") -> str:
    opts = Options()
    opts.headless = True

    browser = Firefox(options=opts)
    browser.get(search_url)

    search_form = browser.find_element_by_id(inpunt_id)
    search_form.send_keys(search_phrase)
    search_form.submit()
    wait = WebDriverWait(browser, 5)
    try:
        wait.until(ec.element_to_be_clickable((By.ID, result_tag_class)))
    except TimeoutException as e:
        if DEBUG:
            print(e)
        pass
    html_body = browser.page_source
    browser.close()
    return html_body


def parse_yandex(html_body: str) -> dict:
    found_results = {}
    parser = BeautifulSoup(html_body, "html.parser")
    links = parser.findAll('a')
    for link in links:
        to_add = link.get('href')
        if not isinstance(to_add, str):
            continue
        if to_add.find('http') != -1 and to_add.find('yandex') == -1:  # filtering urls from service links
            found_results[link.text.strip()] = to_add
    return found_results


def parse_duckduckgo(html_body: str) -> dict:
    found_results = {}
    parser = BeautifulSoup(html_body, "html.parser")
    links = parser.findAll('a', class_='result__a')

    for link in links:
        to_add = link.get('href')
        if not isinstance(to_add, str):
            continue
        if to_add.find('http') != -1:
            found_results[link.text.strip()] = to_add
    return found_results


class Logger():
    """Singleton class to store and log results of search"""
    __data = dict()
    __log_file = None
    __log_format = None

    def __init__(self, log_file: str = None):
        if log_file is None:  # log_file is empty - do nothing
            pass
        elif self.__log_file is not None:  # __log_file already defined - do nothing
            pass
        else:
            ext = None  # To calm down PyCharm
            try:
                _, ext = log_file.split('.')
            except (ValueError, AttributeError):
                sys.exit('Invalid file name')
            if ext in ('json', 'csv'):
                Logger.__log_format = ext
            else:
                sys.exit('Invalid file extension')
            Logger.__log_file = log_file

    @classmethod
    def add(cls, data: dict):
        assert isinstance(data, dict), "Logging data must be a dict"
        cls.__data.update(data)

    @classmethod
    def log(cls):
        to_log = None
        if cls.__log_format == 'json':
            to_log = json.dumps(cls.__data)
        elif cls.__log_format == 'csv':
            to_log = ''
            for item in cls.__data:
                to_log += f"{item}, {cls.__data[item]}\n"
        if cls.__log_format:
            with open(cls.__log_file, 'w') as file:
                file.write(to_log)
        else:
            print('Results found:\n')
            for item in cls.__data:
                print(item, ':', cls.__data[item])


class Searcher:

    def __init__(self, url: str, recursion_depth: int, number_of_searches: int, log_file: str = None):
        self.url = url
        self.recursion_depth = recursion_depth
        self.number_of_searches = number_of_searches
        self.log_file = log_file
        self.found_results = {}
        self.response = None
        Logger(log_file) # initing logger if didn`t call before
        self._requesting()
        self._parsing()
        self._building_pool()


    def _requesting(self):
        if DEBUG:
            print(f'Requesting {self.url}')
        try:
            self.response = requests.get(self.url)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema,
                requests.exceptions.ConnectionError,
                requests.exceptions.SSLError,
                ConnectionError,) as e:
            if DEBUG:
                print(e)

    def _parsing(self):
        # Checking if response is not None and if status code in success range 2**
        if not self.response or not 199 < self.response.status_code < 300:
            return
        html_body = self.response.text
        parser = BeautifulSoup(html_body, "html.parser")
        links = parser.findAll('a')
        number_of_instances = self.number_of_searches
        for link in links:
            if number_of_instances:
                self.found_results[link.text.strip()] = link.get('href')
            else:
                break
            number_of_instances -= 1
        if self.found_results:
            Logger.add(self.found_results)

    def _building_pool(self) -> None:
        if self.recursion_depth == 1 or self.number_of_searches < 1:
            return
        for url in self.found_results.values():
            Searcher(url, self.recursion_depth - 1, self.number_of_searches)



def main():
    # Building CLI and parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('request', type=str, help="Input your request. Use '_' for spaces between words;")
    parser.add_argument('-e', '--engine', type=str, default='yandex.ru',
                        help="Choose search engine. Yandex.ru and DuckDuckGo.com are available. Yandex by default;")
    parser.add_argument('-r', '--recursion', type=int, default=1,
                        help="Input depth or recursion of search. Max value is 5. 1 by default;")
    parser.add_argument('-n', '--number', type=int, default=10,
                        help="Number of search results on page or in each recursion level, if recursion is enabled;")
    parser.add_argument('-f', '--file', type=str, default=None,
                        help='Input path/file for output of results. *.json and *.csv formats are supported; '
                             'Logging to console by default')
    args = parser.parse_args()
    start_key_words = ' '.join(args.request.split('_'))
    initial_data = None
    if args.engine.lower() == 'yandex.ru':
        initial_data = (start_key_words, 'https://ya.ru', 'text',)
    elif args.engine.lower() == 'duckduckgo.com':
        initial_data = (start_key_words, 'https://duckduckgo.com', 'search_form_input_homepage',)
    else:
        sys.exit("Invalid search engine. Start search with '-e yandex.ru' or '-e duckduckgo.com' argument")
    recursion_depth = args.recursion
    if recursion_depth < 1 or recursion_depth > 5:
        sys.exit('Recursion depth must be in 1 to 5 range')
    log_file = args.file
    number_of_searches = args.number
    if number_of_searches < 1:
        sys.exit('Numbers of search must be positive integer')

    # Calling main functionality
    Logger(log_file)
    initial_search_body = initial_search(*initial_data)
    if args.engine == 'duckduckgo.com':
        results = parse_duckduckgo(initial_search_body)
    else:
        results = parse_yandex(initial_search_body)
    Logger.add(results)
    if recursion_depth > 1:
        for url in results.values():
            Searcher(url, recursion_depth - 1, number_of_searches)
    Logger.log()


if __name__ == '__main__':
    main()
