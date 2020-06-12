import os
from setuptools import find_packages, setup
import subprocess as sp


def get_version():
    cp = sp.run(["git", "describe", "--abbrev=0", "--tags"], stdout=sp.PIPE, universal_newlines=True)
    if cp.returncode:
        raise ChildProcessError("Unable to retrieve tag value from Git")
    version = cp.stdout.rstrip()
    version = version[1:] if version.startswith('v') else version
    return version


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='django-comments-dab',
    version=get_version(),
    packages=find_packages(exclude=['docs', 'test*']),
    include_package_data=True,
    author=u'Radico',
    author_email='mus.radi85@gmail.com',
    maintainer='Radi Mustafa',
    maintainer_email='mus.radi85@gmail.com',
    url='https://github.com/radi85/Comment',
    project_urls={
        'Documentation': 'https://django-comment-dab.readthedocs.io/index.html',
        'Source Code': 'https://github.com/radi85/Comment',
    },
    license='MIT',
    description='Django Comment app. It can be associated with any given model.',
    long_description=README,
    install_requires=['django'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='django comment development ajax',
    zip_safe=False,
)
