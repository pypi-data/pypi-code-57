import bs4
import requests
from bs4 import BeautifulSoup

def scrape(k, n):

    keylink=[]
    index2 = 1
    c = -1
    res = requests.get("http://www.google.com/search?q=" + k + ' definition')
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    # print(soup)
    for link in soup.find_all('a', href=True):
        if link.text.find("https") >= 0:
            str = link['href']
            a = str.find('http')
            b = str.find('&sa')

            keylink.append(str[a:b])
            index2 = index2 + 1
            if index2 == n+1:
                break
    return keylink