import setuptools
setuptools.setup(
    name="k3confloader",
    packages=["k3confloader"],
    version="0.1.0",
    license='MIT',
    description='k3confloader loads conf for other pykit3 modules',
    long_description='# k3confloader\n\n[![Build Status](https://travis-ci.com/pykit3/k3confloader.svg?branch=master)](https://travis-ci.com/pykit3/k3confloader)\n[![Documentation Status](https://readthedocs.org/projects/k3confloader/badge/?version=stable)](https://k3confloader.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3confloader)](https://pypi.org/project/k3confloader)\n\nk3confloader loads conf for other pykit3 modules\n\nk3confloader is a component of [pykit3] project: a python3 toolkit set.\n\n\n# Install\n\n```\npip install k3confloader\n```\n\n# Synopsis\n\n```python\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3',
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/drmingdrmer/k3confloader',
    keywords=['conf', 'loader', 'lazyload'],
    python_requires='>=3.0',

    install_requires=['semantic_version~=2.8.5', 'jinja2~=2.11.2', 'PyYAML~=5.3.1', 'sphinx~=3.1.0', 'k3ut~=0.1.7', 'k3proc~=0.2.3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
