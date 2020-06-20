import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pymultienv",
    version="0.0.3",
    packages=[
        'pymultienv',
    ],
    # from here all is optional
    description="pymultienv is a command to help you deal with multiple python environments",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'git',
        'python',
        'repositories',
        'multiple',
    ],
    url="https://veltzer.github.io/pymultienv",
    download_url="https://github.com/veltzer/pymultienv",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'gitpython',
        'pyfakeuse',
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
        'pymultienv=pymultienv.me:cli',
    ]},
    python_requires=">=3.6",
)
