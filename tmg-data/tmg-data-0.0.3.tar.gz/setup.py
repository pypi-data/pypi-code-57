import os
import io
import setuptools


name = "tmg-data"
description = "TMG data library"
version = "0.0.3"
dependencies = [
    "bcrypt==3.1.7",
    "cachetools==4.1.0",
    "certifi==2020.4.5.1",
    "cffi==1.14.0",
    "chardet==3.0.4",
    "cryptography==2.9.2",
    "delegator.py==0.1.1",
    "dnspython==1.16.0",
    "google-api-core==1.17.0",
    "google-api-python-client==1.8.2",
    "google-auth==1.14.0",
    "google-auth-httplib2==0.0.3",
    "google-cloud-bigquery==1.24.0",
    "google-cloud-core==1.3.0",
    "google-cloud-storage==1.27.0",
    "google-resumable-media==0.5.0",
    "googleapis-common-protos==1.51.0",
    "httplib2==0.17.3",
    "idna==2.9",
    "Jinja2==2.11.2",
    "MarkupSafe==1.1.1",
    "mysql-connector==2.2.9",
    "oauth2client==4.1.3",
    "paramiko==2.7.1",
    "parse==1.15.0",
    "pexpect==4.8.0",
    "protobuf==3.6.1",
    "ptyprocess==0.6.0",
    "pyasn1==0.4.8",
    "pyasn1-modules==0.2.8",
    "pycparser==2.20",
    "PyNaCl==1.4.0",
    "pysftp==0.2.9",
    "pytz==2019.3",
    "requests==2.23.0",
    "rsa==4.0",
    "six==1.14.0",
    "uritemplate==3.0.1",
    "urllib3==1.25.9"
]

package_root = os.path.abspath(os.path.dirname(__file__))

readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()


setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author='TMG Data Platform team',
    author_email="data.platform@telegraph.co.uk",
    license="Apache 2.0",
    url='https://github.com/telegraph/tmg-data',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    install_requires=dependencies,
    python_requires='>=3.6',

)
