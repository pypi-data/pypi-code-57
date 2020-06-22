import setuptools

setuptools.setup(
    name='viper-research',
    version="1.0.0",
    author="zhangkai",
    author_email='zhangkai@yuliangtec.com',
    license='MIT',
    url='http://www.yuliangtec.cn',
    description='A framework for developing Quantitative Trading programmes',
    long_description=__doc__,
    keywords='quant quantitative investment trading algotrading',
    classifiers=["Operating System :: OS Independent",
                 'Programming Language :: Python :: 3',
                 # 'Programming Language :: Python :: 3.6',
                 'Topic :: Office/Business :: Financial :: Investment',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'License :: OSI Approved :: MIT License'],
    packages=setuptools.find_packages(),
)
