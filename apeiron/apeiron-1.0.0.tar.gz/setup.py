import sys
from pathlib import Path
from setuptools import setup, find_packages

if not sys.version_info >= (3, 8):
    raise RuntimeError('apeiron requires at least python 3.8')

readme = Path('README.md').read_text()
history = Path('HISTORY.md').read_text()

requirements = Path('requirements.txt').read_text().splitlines()
setup_requirements = []
test_requirements = Path('requirements_dev.txt').read_text().splitlines()

setup(
    author='Andriy Kushnir (Orhideous)',
    author_email='me@orhideous.name',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.8',
    ],
    description='Simple CLI for modpack management',
    install_requires=requirements,
    license='MIT license',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['Minecraft', 'modpack'],
    name='apeiron',
    packages=find_packages(include=['apeiron']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://git.mc4ep.org/mc4ep/apeiron',
    version='1.0.0',
    zip_safe=False,
    entry_points='''
        [console_scripts]
        apeiron=apeiron.cli:cli
    ''',
)
