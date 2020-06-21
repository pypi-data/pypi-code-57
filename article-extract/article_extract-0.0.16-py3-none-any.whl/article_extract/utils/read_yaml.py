# -*- encoding=utf-8 -*-
import sys
import ruamel.yaml


def read_yaml_file():
    """读取yaml文件"""
    try:
        with open('article_rules.yaml', 'r', encoding='utf-8') as fr:
            return ruamel.yaml.load(fr.read(), Loader=ruamel.yaml.Loader)
    except:
        print('读取rules文件失败.')
        sys.exit()


def extract(selector, xpath_list):
    """测试xpath规则"""
    for xpath in xpath_list:
        if not xpath:
            continue
        res = selector.xpath(xpath).extract()
        if res:
            return '\n'.join(res)
    return ''
