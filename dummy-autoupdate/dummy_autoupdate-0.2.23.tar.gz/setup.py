import re
from setuptools import setup, find_packages


def get_version():
    version_file = "dummy_autoupdate/__version.py"
    with open(version_file, 'r') as f:
        file_str = f.read()

    mo = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", file_str, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (version_file,))


setup(
    name='dummy_autoupdate',
    packages=find_packages(),
    version=get_version(),
    author='Vladimir Starostin',
    author_email='vladimir.starostin@uni-tuebingen.de',
    description='Dummy autoupdate for testing',

    license='MIT',
    python_requires='>=3.7.2',
    entry_points={
        "gui_scripts": [
            "dummy_autoupdate = dummy_autoupdate.__main__:main",
        ]
    },
    install_requires=[
        'PyQt5',
        'requests'
    ]
)
