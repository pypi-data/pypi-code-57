import os

from setuptools import find_packages, setup


EXCLUDE_FROM_PACKAGES = ['core', 'e_signatures', 'e_signatures.migrations']


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='django-handwriting-widget',
    version=os.environ['CIRCLE_TAG'],
    url='https://github.com/arthurc0102/django-handwriting-widget',
    author='Arthur Chang',
    author_email='arthurc0102@gmail.com',
    description='A handwriting widget for django',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    install_requires=[
        'django',
    ],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    keywords='handwrite',
)
