# -*- coding: utf-8 -*-
import json
import os

from setuptools import find_packages, setup

import versioneer

version_map = {}
version_map["rqdatac"] = {
    "wcwidth",
    "tabulate",
    "requests",
    "cryptography>=2.9.2",
    "click>=7.0",
    "pyjwt>=1.7.1",
    "patsy==0.5.1",
    "statsmodels==0.11.1",
    "numpy>=1.18.1",
    "rqdatac==2.8.*",
    "rqdatac_bond==0.3.*",
}
version_map["rqfactor"] = version_map["rqdatac"] | {
    "ta-lib==0.4.17",
    "rqfactor==1.0.1",
}
version_map["rqoptimizer"] = version_map["rqdatac"] | {
    "ecos==2.0.7.post1",
    "scs==2.1.1.post2",
    "cvxpy==1.0.25",
    "osqp==0.6.1",
    "rqoptimizer2==1.2.7",
}
version_map["rqalpha_plus"] = version_map["rqfactor"] | version_map["rqoptimizer"] | {
    "rqalpha==4.1.*,>=4.1.4",
    "rqalpha-mod-option==1.1.2",
    "rqalpha-mod-optimizer2==1.0.*,>=1.0.2",
    "rqalpha-mod-convertible==1.1.*,>=1.1.3",
    "rqalpha-mod-ricequant-data==2.2.*,>=2.2.5",
    "rqalpha-mod-rqfactor==1.0.2",
    "rqalpha-mod-bond==1.0.1",
    "rqalpha-mod-spot==1.0.1",
    "rqalpha-plus==4.1.*,>=4.1.10",
}
for k, v in version_map.items():
    version_map[k] = list(v)

with open(os.path.join("rqsdk", "version_map.json"), "w", encoding="utf") as f:
    f.write(json.dumps(version_map, indent=4, sort_keys=True))

extras_require = {}
extras_require["rqdatac"] = version_map["rqdatac"]
extras_require["rqfactor"] = version_map["rqfactor"]
extras_require["rqoptimizer"] = version_map["rqoptimizer"]
extras_require["rqalpha_plus"] = version_map["rqalpha_plus"]

with open('README.md', encoding="utf8") as f:
    readme = f.read()

with open('HISTORY.md', encoding="utf8") as f:
    history = f.read()

setup(
    name="rqsdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Ricequant Native SDK",
    long_description="",
    author="Ricequant",
    author_email="public@ricequant.com",
    keywords="rqsdk",
    url="https://www.ricequant.com/",
    include_package_data=True,
    packages=find_packages(include=["rqsdk", "rqsdk.*"]),
    install_requires=extras_require["rqdatac"],
    python_requires=">=3.5",
    extras_require=extras_require,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "rqsdk = rqsdk:entry_point"
        ]
    },
)
