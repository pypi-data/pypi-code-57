from os import path
from setuptools import setup
from glob import glob


def readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name='fdroid_mirror_monitor',
    version='0.3.0',
    description='monitoring of known https://f-droid.org mirrors',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/marzzzello/mirror-monitor/',
    author='marzzzello',
    author_email='853485-marzzzello@users.noreply.gitlab.com',
    license='AGPL-3.0',
    packages=['fdroid_mirror_monitor'],
    python_requires='>=3.8',
    data_files=[('fdroid_mirror_monitor/templates', glob('templates/*'))],
    install_requires=[
        'coloredlogs',
        'dnspython',
        'fdroidserver',
        'GeoIP',
        'jinja2',
        'json2html',
        'pillow',
        'pypng',
        'pyqrcode',
        'pyyaml',
        'requests',
    ],
    extras_require={'tests': ['coverage', 'responses']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Archiving :: Mirroring',
        'Topic :: System :: Archiving :: Packaging',
        'Topic :: System :: Networking :: Monitoring',
    ],
    zip_safe=False,
)
