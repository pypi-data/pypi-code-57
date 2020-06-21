# -*- encoding=utf-8 -*-
import re
import os
import sys
import ruamel.yaml
from urllib.parse import urljoin
from termcolor import colored
import requests
from scrapy import Selector
from utils import bytes_to_html
from utils.read_yaml import read_yaml_file, extract


def web_from_internet(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
    resp = requests.get(url, headers=headers)
    if not resp.ok:
        print("resp.status_code: ", resp.status_code)
        print("resp.content: ", resp.content)
        sys.exit(-1)
    return resp.content


def bytes_to_lxml(wp_bytes):
    _, html = bytes_to_html(wp_bytes)

    html = re.sub(r'&nbsp', ' ', html).strip()
    sel = Selector(text=html)
    return sel


def extract_article_data(url, selector, is_content_html=False):
    article_data = dict()

    article_data['title'] = ''  # 标题
    article_data['publish_time'] = ''  # 文章时间
    article_data['author'] = ''  # 作者
    article_data['read_count'] = ''  # 阅读量
    article_data['praise_count'] = ''  # 点赞量
    article_data['collection_count'] = ''  # 收藏量
    article_data['source'] = ''  # 来源
    article_data['category'] = ''  # 分类
    article_data['content_html'] = ''  # 文章内容的html
    article_data['content'] = ''  # 文章内容
    article_data['img_list'] = []

    try:
        super_domain = re.findall(r'https?://(.*?)/', url)[0]
    except:
        print(colored('error: ', 'red'), '提取{}的super_domain失败，请检查写入url。'.format(url))
        return
    message_dict = read_yaml_file()
    for rules in ['title', 'publish_time', 'author', 'content', 'content_html']:
        result_message = extract(selector, message_dict[super_domain][rules + '_xpath_list'])
        article_data[rules] = result_message.strip()

    img_message = extract(selector, message_dict[super_domain]['img_xpath_list'])
    message_list = img_message.split('\n')
    article_data['img_list'] = message_list

    if not is_content_html:
        article_data['content_html'] = ''

    # 去除字典中的空值
    for k in list(article_data.keys()):
        if not article_data[k]:
            del article_data[k]

    return article_data

