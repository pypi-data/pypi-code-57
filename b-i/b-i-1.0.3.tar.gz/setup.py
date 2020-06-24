__author__ = 'https://cpp.la'


from setuptools import setup, find_packages

files = ["b-i/*"]

with open('README.md', "r") as readme:
    long_description = readme.read()

setup(
    name='b-i',
    version='1.0.3',
    keywords=['b-i', 'hive', 'mysql', 'elasticsearch', 'cppla'],
    description='BI tools for data developer use Python Language. by:cpp.la',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',

    author='cppla',
    author_email='i@cpp.la',
    url='https://github.com/cppla/b-i',

    packages=find_packages(),

    platforms='linux',
    install_requires=[
        'sasl',
        'thrift',
        'thrift-sasl',
        'pyhive',
        'pymysql',
        'requests',
        'sqlalchemy',
        'loguru',
        'python-dateutil',
        'elasticsearch',
        'sqlparse'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires=">=3.6",
)
