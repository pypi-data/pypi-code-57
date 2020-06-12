#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from setuptools import setup
from setuptools import find_packages

packages = find_packages()

setup(
    name = "labm8",
    version = "2020.06.01",
    description = "Utility libraries for doing science",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers = ["Development Status :: 4 - Beta", "Environment :: Console", "Intended Audience :: Developers", "License :: OSI Approved :: Apache Software License", "Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7", "Programming Language :: Python :: 3.8"],
    keywords = "utility library bazel protobuf",
    url = "https://github.com/ChrisCummins/labm8",
    author = "Chris Cummins",
    author_email = "chrisc.101@gmail.com",
    license = "Apache License, Version 2.0",
    packages=packages,
    install_requires=["GPUtil==1.4.0", "MarkupSafe==1.1.1", "Pygments==2.2.0", "SQLAlchemy==1.3.10", "Send2Trash==1.5.0", "absl-py==0.7.0", "appdirs==1.4.3", "appnope==0.1.0", "bleach==1.5.0", "certifi==2018.4.16", "chardet==3.0.4", "checksumdir==1.0.5", "cycler==0.10.0", "decorator==4.3.0", "entrypoints==0.2.3", "fasteners==0.15", "gspread-dataframe==3.0.3", "gspread==3.1.0", "html5lib==0.9999999", "httplib2==0.14", "humanize==0.5.1", "idna==2.6", "ipaddress==1.0.23", "ipykernel==4.8.2", "ipython-genutils==0.2.0", "ipython==5.7.0", "jinja2==2.10.1", "jsonschema==2.6.0", "jupyter-client==5.2.2", "jupyter-core==4.4.0", "jupyter==1.0.0", "jupyter_http_over_ws==0.0.7", "kiwisolver==1.0.1", "matplotlib==2.2.0rc1", "mistune==0.8.3", "monotonic==1.5", "mysqlclient==1.4.2.post1", "nbconvert==5.3.1", "nbformat==4.4.0", "networkx==2.2", "notebook==5.7.8", "numpy==1.16.4", "oauth2client==4.1.3", "pandas==0.24.1", "pandocfilters==1.4.2", "pexpect==4.4.0", "pickleshare==0.7.4", "prometheus_client==0.6.0", "prompt-toolkit==1.0.15", "protobuf==3.6.1", "ptvsd==4.3.2", "ptyprocess==0.5.2", "py==1.5.2", "pyOpenSSL==19.1.0", "pyasn1==0.4.7", "pyasn1_modules==0.2.7", "pyparsing==2.2.0", "python-dateutil==2.6.1", "pytz==2018.3", "pyzmq==19.0.1", "requests==2.20.1", "rsa==4.0", "scipy==1.2.1", "seaborn==0.9.0", "simplegeneric==0.8.1", "six==1.11.0", "tabulate==0.8.5", "terminado==0.8.1", "testpath==0.3.1", "tornado==5.0", "tqdm==4.38.0", "traitlets==4.3.2", "urllib3==1.24.2", "wcwidth==0.1.7"],
    zip_safe=False,
)
