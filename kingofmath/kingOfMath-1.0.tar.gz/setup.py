#coding=utf-8
from distutils.core import setup

setup(
    name = "kingOfMath" , #对外我们模块的名字
    version = "1.0" ,#版本号
    description = "这是第一个对外发布的模块，测试哦" ,#描述
    author = "wzl" ,#作者
    author_email = "282134264@qq.com",
    py_modules = ["kingOfMath.demo1","kingOfMath.demo2"]  #要发布的模块

)