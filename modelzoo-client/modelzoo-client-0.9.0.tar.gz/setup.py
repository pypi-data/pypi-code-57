#  Copyright (C) 2020 Servly AI.
#  See the LICENCE file distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import find_packages, setup


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="modelzoo-client",
    version="0.9.0",
    author="Model Zoo, Inc.",
    install_requires=[
        # Do not pin tqdm and requests since they're very commonly used in
        # downstream environments.
        "tqdm",
        "requests",
        "Pillow",
        # Pin these rarer dependencies.
        "colorama==0.4.3",
        "termcolor==1.1.0",
        "yaspin==0.16.0",
        "names==0.3.0",
        "click==7.1",
    ],
    extras_require={
        "transformers": ["transformers>=2.10.0", "torch"],
        "tensorflow": ["tensorflow>2"],
    },
    packages=find_packages(),
    description="The Model Zoo Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="admin@modelzoo.dev",
    license="Apache 2.0",
    keywords="model zoo",
    url="https://www.modelzoo.dev",
    entry_points={"console_scripts": ["modelzoo = modelzoo.cli:cli"]},
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    test_suite="tests",
    python_requires=">=3.5",
)
