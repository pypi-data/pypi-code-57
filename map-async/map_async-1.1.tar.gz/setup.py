import setuptools


setuptools.setup(
    name="map_async",
    version="1.1",
    license="MIT",
    description="Multiprocess mapping with a integrated progress bar.",
    author='Kang Min Yoo',
    author_email='kangmin.yoo@gmail.com',
    url='https://github.com/kaniblu/map-async',
    py_modules=["map_async"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
    keywords=[
        "asynchronous",
        "map",
        "multiprocessing"
    ],
    install_requires=[
        "tqdm>=4.46.1"
    ],
)
