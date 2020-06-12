from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.0.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [
    x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')
]

if __name__ == "__main__":
    setup(
        name='venvhpl',
        version=__version__,
        description="Links Host's Python Library into Virtualenv",
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/mcfletch/venvhpl',
        download_url='https://github.com/mcfletch/venvhpl/tarball/' + __version__,
        license='MIT',
        classifiers=[
            'Intended Audience :: Developers',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 2',
        ],
        keywords='venv host package link',
        packages=find_packages(exclude=['docs', 'tests*']),
        include_package_data=True,
        author='Mike C. Fletcher',
        install_requires=install_requires,
        dependency_links=dependency_links,
        author_email='mcfletch@vrplumber.com',
        entry_points={'console_scripts': ['venv-hpl=venvhpl.venvhpl:main',],},
    )
