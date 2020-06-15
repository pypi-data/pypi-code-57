import setuptools

long_description = open("README.rst").read()
#Version change by Shunxing
VERSION = "0.12.5.3"

setup_params = dict(
    name="CacheControl_ldax",
    version=VERSION,
    author="Shunxing Bao",
    author_email="onealbao@gmail.com",
    url="https://github.com/VUIIS/cachecontrol",
    keywords="requests http caching web - ldax testing version",
    packages=setuptools.find_packages(),
    package_data={"": ["LICENSE.txt"]},
    package_dir={"cachecontrol": "cachecontrol"},
    include_package_data=True,
    description="httplib2 caching for requests",
    long_description='''The package is hosted at VUIIS github repo, which is a customized package to enable ldax cahce feature (testing only). The project is orginal hosted at https://github.com/ionrock/cachecontrol''',
    install_requires=["requests", "msgpack>=0.5.2"],
    extras_require={"filecache": ["lockfile>=0.9"], "redis": ["redis>=2.10.5"]},
    entry_points={"console_scripts": ["doesitcache = cachecontrol._cmd:main"]},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
)


if __name__ == "__main__":
    setuptools.setup(**setup_params)
