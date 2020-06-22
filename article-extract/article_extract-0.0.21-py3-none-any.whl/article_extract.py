# -*- coding: utf-8 -*-

import re
import sys
import time
import json
import requests
import ruamel.yaml
from scrapy import Selector

DIRTY_CHARS = re.compile(r'[Ҫ瀹╄ㄥɾڸŲӰеԪΪЩй˾ǹӦȾڷҽա⣿Ŀѣ╀ц¤ㄣ�]', flags=(re.I|re.S))


def guess_encoding(content, encoding):
    try:
        html = content.decode(encoding, errors='ignore')
        no_ascii_content_str = re.sub(re.compile(r'[\sa-zA-Z0-9`i\~\!@#\$\%\^\&\*\(\)_\+\-=\[\]\{\}\|\?/<>,\.;\':"]', flags=(re.I|re.S)), '', html)
        chi_chars = re.findall(re.compile(r'[的一是了我不人在他有这个上们来到时大地为子中你说生国年着就那和要她出也得里后自以会家可下而过天去能对小多然于心学么之都好看起发当没成只如事把还用第样道想作种开网]', flags=(re.I|re.S)), no_ascii_content_str)
        str_chars = re.findall(DIRTY_CHARS, no_ascii_content_str)
        if (len(chi_chars) / len(no_ascii_content_str) >= 0.1 or
                len(chi_chars) >= 3) and (len(set(str_chars))<=2):
            return html
    except Exception:
        pass
    return None


def bytes_to_html(content):
    if not isinstance(content, bytes):
        raise Exception("content type should be bytes.")
    match = re.search(rb'charset="?([A-Za-z0-9-]*)"?', content)
    encoding = 'utf-8'
    html = ''
    if match:
        encoding = match.group(1).decode('ascii')
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'utf-8'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'gbk'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'gb2312'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'utf16'
        html = guess_encoding(content, encoding)
    if not html:
        encoding = 'unicode'
        html = guess_encoding(content, encoding)
    if html is not None:
        return (encoding, html)
    else:
        raise Exception()


def read_yaml_file():
    """读取yaml文件"""
    with open(r'article_extract/article_rules.yaml', 'r', encoding='utf-8') as fr:
        return ruamel.yaml.load(fr.read(), Loader=ruamel.yaml.Loader)


def extract(selector, xpath_list):
    """测试xpath规则"""
    for xpath in xpath_list:
        if not xpath:
            continue
        res = selector.xpath(xpath).extract()
        if res:
            return '\n'.join(res)
    return ''


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

    super_domain = re.findall(r'https?://(.*?)/', url)[0]
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
