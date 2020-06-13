# History
# 0.0.3: Exposed EyeDiagram
# 0.0.4: Added Curve.filter()
# 0.0.6: Pickle support, equality operand.
# 0.0.7: Fix in Curve.prbs_check()

import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="curve",
    version="0.0.7",
    description="A waveform manipulation and analysis library for Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Juan Pablo Caram",
    author_email="jpcaram@gmail.com",
    url="https://bitbucket.org/jpcgt/curve",
    requires=['matplotlib', 'numpy', 'scipy'],
    install_requires=['matplotlib', 'numpy', 'scipy'],
    packages=['curve'],
    python_requires='>=3.6',
    package_dir={'curve': 'curve'},
)
