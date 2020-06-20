import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pysigfd",
    version="1.3.4",
    packages=[
        'pysigfd',
    ],
    # from here all is optional
    description="linux signal file descriptor for python",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'signalfd',
        'python3',
        'linux',
    ],
    url="https://veltzer.github.io/pysigfd",
    download_url="https://github.com/veltzer/pysigfd",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'cffi',
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    data_files=[
    ],
    entry_points={"console_scripts": [
    ]},
    python_requires=">=3.6",
)
