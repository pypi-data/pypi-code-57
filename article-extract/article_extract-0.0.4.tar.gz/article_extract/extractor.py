# -*- coding: utf-8 -*-
import time
import json
from utils.data_loader import web_from_internet, bytes_to_lxml, extract_article_data


def extractor(url, is_content_html=False):
    web_page_bytes = web_from_internet(url)
    lxml_extract = bytes_to_lxml(web_page_bytes)
    if is_content_html:
        article_data = extract_article_data(url, lxml_extract, is_content_html=True)
    else:
        article_data = extract_article_data(url, lxml_extract)
    json_data = dict()
    json_data['url'] = url
    json_data['crawl_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    json_data['data'] = article_data
    return json_data


def start():
    # url = 'http://sz.bendibao.com/news/2020619/838960.htm'  # 本地宝
    url = 'https://blog.csdn.net/cui_yonghua/article/details/103787523'  # CSDN博客
    # url = 'https://www.jianshu.com/p/ee1540ad00a2'  # 简书
    data = extractor(url, is_content_html=False)
    print(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    start()
