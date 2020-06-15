#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: gm
# Mail: 1025304567@qq.com
# Created Time: 2019-04-11 15:37:04
#############################################


from setuptools import setup, find_packages
"""
name是包的分发名称。只要包含字母，数字_和 -。
version 是包版本看 PEP 440有关版本的更多详细信息。
author 和author_email用于识别包的作者。
description 是一个简短的，一句话的包的总结。
long_description是包的详细说明。这显示在Python Package Index的包详细信息包中。在这种情况下，加载长描述README.md是一种常见模式。
long_description_content_type告诉索引什么类型的标记用于长描述。在这种情况下，它是Markdown。
url是项目主页的URL。对于许多项目，这只是一个指向GitHub，GitLab，Bitbucket或类似代码托管服务的链接。
packages是应包含在分发包中的所有Python 导入包的列表。我们可以使用 自动发现所有包和子包，而不是手动列出每个包。在这种情况下，包列表将是example_pkg，因为它是唯一存在的包。find_packages()
classifiers告诉索引并点一些关于你的包的其他元数据。在这种情况下，该软件包仅与Python 3兼容，根据MIT许可证进行许可，并且与操作系统无关。您应始终至少包含您的软件包所使用的Python版本，软件包可用的许可证以及您的软件包将使用的操作系统。有关分类器的完整列表，请参阅 https://pypi.org/classifiers/。
"""
setup(
    name = "xapdbclib",
    version = "1.0",
    keywords = ("pip", "license","licensetool", "tool", "gm"),
    description = "XAP系统---数据库读取和存储python版",
    long_description = "XAP系统---数据库读取和存储python版",
    license = "MIT Licence",

    url = "https://github.com/lanwajing/xapdbclib",
    author = "xuanbin",
    author_email = "1454240159@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['chardet']
)