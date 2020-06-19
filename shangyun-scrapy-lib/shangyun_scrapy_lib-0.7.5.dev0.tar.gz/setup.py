#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import setuptools
from pkgutil import walk_packages
from setuptools import setup


def find_packages(path):
    # This method returns packages and subpackages as well.
    return [name for _, name, is_pkg in walk_packages([path]) if is_pkg]


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_rst(filename):
    # Ignore unsupported directives by pypi.
    content = read_file(filename)
    return ''.join(line for line in io.StringIO(content)
                   if not line.startswith('.. comment::'))


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


# setup(
#     name='shangyun_scrapy_redis',
#     version=read_file('VERSION'),
#     description="Redis-based components for Scrapy.",
#     long_description=read_rst('README.rst') + '\n\n' + read_rst('HISTORY.rst'),
#     author="Rolando Espinoza",
#     author_email='rolando@rmax.io',
#     url='https://github.com/rolando/scrapy-redi',
#     packages=list(find_packages('src')),
#     package_dir={'': 'src'},
#     setup_requires=read_requirements('requirements-setup.txt'),
#     install_requires=read_requirements('requirements-install.txt'),
#     include_package_data=True,
#     license="MIT",
#     keywords='shangyun-scrapy-redis',
#     classifiers=[
#         'Development Status :: 4 - Beta',
#         'Intended Audience :: Developers',
#         'License :: OSI Approved :: MIT License',
#         'Natural Language :: English',
#         "Programming Language :: Python :: 2",
#         'Programming Language :: Python :: 2.7',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#     ],
# )
setup(
    name="shangyun_scrapy_lib",  #pypi中的名称，pip或者easy_install安装时使用的名称
    version=read_file('VERSION'),
    author="Andreas Schroeder",
    author_email="andreas@drqueue.org",
    description=("This is a service of redis subscripe"),
    license="GPLv3",
    keywords="redis subscripe",
    url="https://ssl.xxx.org/redmine/projects/RedisRun",
    packages=setuptools.find_packages(),  # 需要打包的目录列表
    # 需要安装的依赖
    install_requires=read_requirements('requirements-install.txt'),

    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
