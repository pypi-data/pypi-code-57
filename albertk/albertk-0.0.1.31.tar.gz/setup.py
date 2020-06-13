# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os import path as os_path
import time
this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
long_description="""



#搜索关键词进行聚类

from albertk import *
model,tokenizer=load_albert("data/albert_tiny")
keyword=input("输入关键词：")
# keyword="边境牧羊犬智商"
klist=run_search_sent(keyword,20,tokenizer,model)
print(klist)


"""
setup(
    name='albertk',
    version='0.0.1.31',
    description='Terry albertk',
    author='Terry Chan',
    author_email='napoler2008@gmail.com',
    url='https://terry-toolkit.terrychan.org/zh/master/',
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'kmeans_pytorch==0.3',
        'pymongo==3.10.1',
        'elasticsearch_dsl==7.1.0',
        'elasticsearch==7.6.0',
        'scikit_learn==0.22.2.post1',
        'tkitFile==0.0.1.2',
        'tkitText==0.0.1.5',
        'tqdm==4.38.0',
        # 'unqlite==0.7.1',
        # 'cacheout==0.11.2',
        # 'harvesttext==0.5.4.2',
        # 'tqdm==4.38.0',
        # 'sqlitedict==1.6.0',
        # 'Whoosh==2.7.4',
        # 'plyvel==1.1.0',

    ],
    packages=['albertk'])
    # install_requires=[
    #     # asn1crypto==0.24.0
    #     # beautifulsoup4==4.7.1
    #     # bs4==0.0.1
    #     # certifi==2019.3.9
    #     # chardet==3.0.4
    #     # cryptography==2.1.4
    #     # cycler==0.10.0
    #     # docopt==0.6.2
    #     # idna==2.6
    #     # jieba==0.39
    #     # keyring==10.6.0
    #     # keyrings.alt==3.0
    #     # kiwisolver==1.0.1
    #     # matplotlib==3.0.3
    #     # numpy==1.16.2
    #     # pandas==0.24.2
    #     # pipreqs==0.4.9
    #     # PyAudio==0.2.11
    #     # pycrypto==2.6.1
    #     # pygobject==3.26.1
    #     # pyparsing==2.4.0
    #     # python-dateutil==2.8.0
    #     # pytz==2019.1
    #     # pyxdg==0.25
    #     # requests==2.21.0
    #     # scipy==1.2.1
    #     # SecretStorage==2.3.1
    #     # six==1.11.0
    #     # soupsieve==1.9.1
    #     # urllib3==1.24.1
    #     # yarg==0.1.9

    # ],

    #install_requires=['jieba'])
"""
pip freeze > requirements.txt
# https://python.terrychan.org/chang-yong-cao-zuo/python-xiang-mu-biao-zhun-hua-cao-zuo
python3 setup.py sdist
#python3 setup.py install
python3 setup.py sdist upload
"""