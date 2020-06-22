from setuptools import find_packages, setup
import os

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')

with open(readme_file) as readme:
    README = f"{readme.read()}"
README = README.replace(README.split('# Install')[0], '')

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="tokko_rpc",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    license="BSD License",
    description="Tokko RPC flavor.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/TokkoLabs/services-tokkobroker/tools/tokko-rpc-plugin",
    author="Jose Salgado",
    author_email="jsalgado@navent.com",
    install_requires=[
        "arrow==0.15.6",
        "python-dateutil==2.2",
        "Werkzeug==1.0.1",
        "json-rpc==1.13.0",
        "coloredlogs==14.0",
        "requests==2.24.0",
        "jinja2==2.11.2",
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
