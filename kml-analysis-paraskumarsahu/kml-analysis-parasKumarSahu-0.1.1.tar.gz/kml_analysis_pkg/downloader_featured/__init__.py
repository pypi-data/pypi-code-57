from multiprocessing import Pool, cpu_count
import wikipediaapi
import time
from bs4 import BeautifulSoup
from itertools import islice
from datetime import datetime
import requests


def get_user_views(title):
    url1 = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/'
    url2 = '/monthly/19900101/22200101'
    response = requests.get(url1+title+url2)

    if response:
        months = len(response.json()['items'])
        user_views = 0

        for i in range(months):
            user_views += int(response.json()['items'][i]['views'])    
        return user_views   
    #Incase of error assume zero views        
    else:
        return 0      


def download_wiki(title):
    try:
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(title)

        if page_py.exists() and len(str(page_py.text.encode("utf-8"))) > 10:
            user_views = get_user_views(title)
            file = open("featured/"+str(user_views)+"$#@"+title+".txt","w")
            file.write(str(page_py.text.encode("utf-8")))
            file.close()
            print(title, "downloaded")
        else:
            print("Error in downloading ->", title)    

    except Exception as e:
        print(e)


def run(html_file_path):
    page = open(html_file_path, encoding="utf-8")
    soup = BeautifulSoup(page, 'html.parser')
    page.close()

    spans = soup.find_all(class_="featured_article_metadata has_been_on_main_page")
    titles = []

    for s in spans:
        titles.append(s.text)

    #print(len(titles))
    titles_iter = iter(titles) 
    sub_titles_list = [list(islice(titles_iter, 10)) for i in range(490)]

    print("There are {} CPUs on this machine ".format(cpu_count()))

    startTime = datetime.now()

    for sub_titles in sub_titles_list: 
        pool = Pool(cpu_count())
        results = pool.map(download_wiki, sub_titles)
        pool.close()
        pool.join()
        time.sleep(1)

    print("Download Time", datetime.now() - startTime)