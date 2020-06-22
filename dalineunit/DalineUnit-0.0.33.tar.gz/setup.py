import setuptools
from setuptools.command.install import install

with open("readme.md", "r",encoding='utf8') as fh:
    long_description = fh.read()



setuptools.setup(
    name="DalineUnit",
    version="0.0.33",
    author="kun.z",
    author_email="kun.z@daline.com.cn",
    description="daline unit generator and runner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DalineWH",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            # 这一行是安装到命令行运行的关键
            'DalGenScript = DalineUnit.DalGenScript:run'
        ]
    },
    classifiers=[
        # "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='daline Unit',
    install_requires=[
        'astroid==2.3.3',
        'beautifulsoup4==4.8.2',
        'certifi==2019.11.28',
        'chardet==3.0.4',
        'Click==7.0',
        'colorama==0.4.3',
        'google==2.0.3',
        'grpcio==1.26.0',
        'grpcio-tools==1.26.0',
        'httpie==2.0.0',
        'idna==2.8',
        'isort==4.3.21',
        'lazy-object-proxy==1.4.3',
        'lxml==4.5.0',
        'mccabe==0.6.1',
        'protobuf==3.11.2',
        'pycurl==7.43.0.5',
        'Pygments==2.6.1',
        'pylint==2.4.4',
        'requests==2.22.0',
        'six==1.14.0',
        'soupsieve==1.9.5',
        'tornado==6.0.3',
        'typed-ast==1.4.1',
        'urllib3==1.25.8',
        'wrapt==1.11.2',
        'xlwt==1.3.0',
        'cx_Oracle==7.3.0'
    ],
)



# !!!!打包的环境要有GRPC！！！！！！，最好与调试环境相同
# python setup.py sdist bdist_wheel
# twine upload dist/*

