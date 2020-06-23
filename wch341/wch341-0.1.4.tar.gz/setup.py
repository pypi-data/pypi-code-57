# -*- coding: utf-8 -*
import os
from setuptools import setup
from glob import glob

dirs = ['wch341']
modules = ['wch341']
for path,dir_list,file_list in os.walk("./wch341"):
    for dir_name in dir_list:
        if dir_name.find("__")==-1 and dir_name.find("egg")==-1:
            dirs.append((path+"/"+dir_name).replace("/",".").replace("..",""))
    for file_name in file_list:
        if file_name.find(".py")!=-1 and file_name.find(".pyc")==-1:
            modules.append((path+"."+file_name.replace(".py","")).replace("/",".").replace("..",""))

here = os.path.dirname(__file__)
setup(
    name='wch341',
    version='0.1.4',
    author='makeblock',
    author_email='flashindream@gmail.com',
    url='https://makeblock.com',
    description=u'driver for wch341/340',
    packages=dirs,
    data_files=[
        (here+'/wch341/driver',glob('./assets/ch34x_install.*'))
    ],
    py_modules=modules,
    include_package_data=True,
    # install_requires=['pyserial'],
)