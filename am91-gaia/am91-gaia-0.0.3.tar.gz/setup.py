from setuptools import setup

VERSION = '0.0.3'
REQUIREMENTS = ['jinja2']

with open('README.md', 'r') as readme_file:
    README = readme_file.read()

setup(
    name='am91-gaia',
    version = VERSION,
    author = 'Alejandro Alonso Mayo',
    author_email = 'alejandroalonsomayo@gmail.com',
    description='Project generator',
    long_description = README,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/AlejandroAM91/gaia',
    download_url = f'https://github.com/AlejandroAM91/gaia/archive/v{VERSION}.tar.gz',
    classifiers = [
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires = REQUIREMENTS,
    package_dir={'': 'src'},
    packages=['am91.gaia', 'am91.gaia.template.base'],
    entry_points={
        'console_scripts': 'gaia = am91.gaia.cli:main',
        'am91.gaia.template': 'base = am91.gaia.template.base',
    },
    package_data = {
        'am91.gaia_template_base': [
            'templates/*.jinja',
            'templates/.*.jinja',
            'templates/**/*.jinja'
        ]
    }
)
