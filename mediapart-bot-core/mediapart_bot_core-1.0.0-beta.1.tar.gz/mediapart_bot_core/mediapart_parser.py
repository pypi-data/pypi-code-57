import feedparser
import requests
import time
import os
from bs4 import BeautifulSoup
from requests import Session

 
class MediapartParser:

    mediapart_base_pdf_url = "https://www.mediapart.fr/tools/pdf/"

    mediapart_user = ""
    mediapart_pwd = ""

    def __init__(self, user, pwd): 
        self.mediapart_user = user
        self.mediapart_pwd = pwd

    def get_rss_entries(self):
        mediapart_parsed_rss = feedparser.parse("https://www.mediapart.fr/articles/feed")
        last_articles = mediapart_parsed_rss.entries
        return last_articles

    def get_last_articles_titles(self):
        titles = []
        last_articles = self.get_rss_entries()  
        for article in last_articles:
            titles.append(article.title)
        return titles
    
    def get_last_categories(self):
        categories = []
        last_articles = self.get_rss_entries()  
        for article in last_articles:
            categories.append(article.tags[0].term)
        return categories

    def get_last_articles_links(self):
        all_links = []
        last_articles = self.get_rss_entries()  
        for article in last_articles:
            for link in article.links:
                all_links.append(link.href)
        return all_links
     
    def get_last_full_articles_links(self):
        full_article_suffix = "?onglet=full"
        all_links = []
        last_articles = self.get_rss_entries()  
        for article in last_articles:
            for link in article.links:
                all_links.append(link.href + full_article_suffix)
        return all_links

    def get_article_id(self, article_url): 
        page = requests.get(article_url,auth=(self.mediapart_user, self.mediapart_pwd))
        soup = BeautifulSoup(page.text, "html.parser")
        result = soup.find("div", {"class":"sub-header accur8-desktop accur8-tablet accurWidth-desktop accurWidth-tablet"})
        return result["data-nid"]
    
    def get_all_pdf_links(self):
        pdf_link_preffix = "https://www.mediapart.fr/tools/pdf/"
        pdf_links = []

        all_articles_links = self.get_last_articles_links()

        for article_link in all_articles_links:
            article_id = self.get_article_id(article_link)
            article_pdf_link = pdf_link_preffix + article_id
            pdf_links.append(article_pdf_link)

        return pdf_links

    def url_to_pdf(self, article_id, final_file_path):
        url = self.mediapart_base_pdf_url + str(article_id)

        s = Session()
        login_data = {"name":self.mediapart_user,"password":self.mediapart_pwd,"op":"Se+connecter"}
        s.post("https://www.mediapart.fr/login_check",login_data)
        page = s.get(url)
        f = open(final_file_path, 'wb')
        f.write(page.content)
        f.close()

        while not os.path.exists(final_file_path):
            time.sleep(1)

        


