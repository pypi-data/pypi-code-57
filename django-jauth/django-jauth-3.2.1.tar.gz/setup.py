# -*- coding: utf-8 -*-
from distutils.core import setup


def parse_requirements(filename, session=False):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_requires = parse_requirements('requirements.txt', session=False)

setup(
    name='django-jauth',
    version='3.2.1',
    author=u'Jani Kajala',
    author_email='kajala@gmail.com',
    packages=['jauth'],
    include_package_data=True,
    url='https://github.com/kajala/django-jauth',
    license='MIT licence, see LICENCE.txt',
    description='Simple OAuth2 login support for Django and Django REST Framework projects',
    long_description=open('README.md').read(),
    zip_safe=True,
    install_requires=install_requires
)
