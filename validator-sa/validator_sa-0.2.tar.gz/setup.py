# coding: utf-8

# @Time:2020/3/15 12:34
# @Auther:sahala

import os
from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="validator_sa",  # 这里是pip项目发布的名称
    version="0.2",  # 版本号，数值大的会优先被pip
    keywords=("pip", "validator_sa", "featureextraction"),
    description="数据校验器：dict,list等python任何数据类型",
    long_description="数据校验器：dict,list等python任何数据类型 ",
    license="MIT Licence",

    url="https://github.com/",  # 项目相关文件地址，一般是github
    author="liyubin",
    author_email="1399393088@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[
                      "requests",
                      ]  # 这个项目需要的第三方库
)



# 步骤：

# 1.setup.py放在被打包同级
    # 本地打包项目文件
    # python setup.py sdist

# 2.上传项目到pypi服务器
    # pip install twine
    # twine upload dist/name.tar.gz

# 3.下载上传的库
    # pip install name
