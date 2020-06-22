#coding=utf-8
from distutils.core import setup

setup(
    name='myfirstpypipackage',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，测试哦',  #描述
    author='yeqingyao',  # 作者
    author_email='44292807@qq.com', py_modules=['myfirstpypipackage.demo1','myfirstpypipackage.demo2']  # 要发布的模块
)