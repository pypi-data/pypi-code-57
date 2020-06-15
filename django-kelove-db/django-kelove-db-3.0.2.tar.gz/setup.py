# ==================================================================
#       文 件 名: setup.py
#       概    要: 扩展包构建
#       作    者: IT小强 
#       创建时间: 5/28/20 9:57 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

from json import loads

from os import path as path

from setuptools import setup, find_packages

from django_kelove_db import PACKAGE_VERSION

base_directory = path.abspath(path.dirname(__file__))

# 获取全部的包信息
all_packages = find_packages()

# 移除 django_kelove 包
try:
    all_packages.remove('django_kelove')
except ValueError:
    pass


def read_file(filename):
    """
    读取文件内容
    :param filename: 文件名
    :return:
    """
    with open(path.join(base_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
        return long_description


def read_requirements(filename='Pipfile.lock'):
    """
    获取依赖
    :param filename: 文件名
    :return:
    """
    requires = loads(read_file(filename))
    requires = requires.get('default', {})
    requires = [(k + v.get('version', '')) for k, v in requires.items()]
    return requires


setup(

    name='django-kelove-db',

    python_requires='>=3.7.0',

    version=PACKAGE_VERSION,

    description="Django数据库迁移优化（目前只完善MySQL）",

    long_description=read_file('README.md'),

    long_description_content_type="text/markdown",

    author="IT小强xqitw.cn",

    author_email='mail@xqitw.cn',

    url='https://e.coding.net/xqitw/django-kelove/django-kelove-db.git',

    packages=all_packages,

    install_requires=read_requirements(),

    include_package_data=True,

    license="Apache-2.0",

    keywords=['django', 'mysql', 'comment'],

    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
