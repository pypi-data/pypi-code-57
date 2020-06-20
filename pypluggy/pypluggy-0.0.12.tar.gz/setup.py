import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pypluggy",
    version="0.0.12",
    packages=[
        'pypluggy',
    ],
    # from here all is optional
    description="pypluggy is a lightweight plugin framework for python",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'plugin',
        'python',
    ],
    url="https://veltzer.github.io/pypluggy",
    download_url="https://github.com/veltzer/pypluggy",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'pytconf',
        'pylogconf',
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
        'pymakehelper=pymakehelper.endpoints.main:main',
    ]},
    python_requires=">=3.6",
)
