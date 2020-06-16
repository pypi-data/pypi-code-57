import glob
import os
import shutil
import sys

from setuptools import setup, find_packages
from distutils.extension import Extension

# Do not edit version or _install_requires, which are overwritten by scripts/push_version.sh

_install_requires=["absl-py==0.6.1", "apache-beam==2.9.0", "astor==0.7.1", "avro==1.8.2", "backports.functools-lru-cache==1.5", "backports.weakref==1.0.post1", "boto3==1.9.75", "botocore==1.12.75", "cachetools==3.0.0", "certifi==2018.11.29", "chardet==3.0.4", "crcmod==1.7", "cycler==0.10.0", "Cython==0.29.2", "dill==0.2.8.2", "docopt==0.6.2", "docutils==0.14", "enum34==1.1.6", "fastavro==0.21.16", "fasteners==0.14.1", "flatten-dict==0.0.3.post1", "flatten-json==0.1.6", "funcsigs==1.0.2", "future==0.17.1", "futures==3.2.0", "gast==0.2.0", "google-api-core==1.7.0", "google-api-python-client==1.7.7", "google-apitools==0.5.24", "google-auth==1.6.2", "google-auth-httplib2==0.0.3", "google-cloud-bigquery==1.6.1", "google-cloud-core==0.28.1", "google-cloud-pubsub==0.35.4", "google-cloud-storage==1.12.0", "google-resumable-media==0.3.2", "googleapis-common-protos==1.5.5", "googledatastore==7.0.2", "grpc-google-iam-v1==0.11.4", "grpcio==1.17.1", "hdfs==2.2.2", "httplib2==0.11.3", "idna==2.8", "ipaddress==1.0.22", "jmespath==0.9.3", "jsonpickle==1.0", "kiwisolver==1.0.1", "Markdown==3.0.1", "matplotlib==2.2.3", "mock==2.0.0", "monotonic==1.5", "numpy==1.15.4", "oauth2client==3.0.0", "pathlib2==2.3.3", "pbr==5.1.1", "proto-google-cloud-datastore-v1==0.90.4", "protobuf==3.6.1", "psycopg2-binary==2.7.6.1", "pyasn1==0.4.4", "pyasn1-modules==0.2.2", "pydot==1.2.4", "pymongo==3.7.2", "pyparsing==2.3.0", "python-dateutil==2.7.5", "pytz==2018.4", "PyVCF==0.6.8", "PyYAML==3.13", "requests==2.21.0", "rsa==4.0", "s3transfer==0.1.13", "scandir==1.9.0", "scikit-learn==0.20.2", "scipy==1.1.0", "six==1.12.0", "sklearn==0.0", "subprocess32==3.5.3", "tensorboard==1.9.0", "tensorflow==1.9.0", "termcolor==1.1.0", "testfixtures==6.4.0", "typing==3.6.6", "ua-parser==0.8.0", "ujson==1.35", "uritemplate==3.0.0", "urllib3==1.24.1", "user-agents==1.1.0", "Werkzeug==0.14.1", "xgboost==0.81", "setuptools <=39.1.0"]

_dataflow_deps = [dep for dep in _install_requires if dep.split('==')[0] in (
      # These are the packages required to run (but not launch) various dataflow and training jobs
      # 'bytegain', can't put this here because there is no way to give pointer to fury.io.
      #             setup()'s dependency_links kwarg does not work. Hence in generated Dataflow requirements file.
      'catboost',
      'Cython',
      'jsonpickle',
      'xgboost'
)]

# Dataflow likes cythonize.  Gemfury likes the generated C code.
if os.environ.get('DATAFLOW_SETUP_PY'):
    from Cython.Build import cythonize
    EXTRA_ARGS = {'ext_modules': cythonize("**/*.pyx"),
                  'package_data': {'bytegain': ['**/*.pyx']}}
else:
    EXTRA_ARGS = {'ext_modules': [Extension("bytegain/custom/model_data/bucket",
                                            ["bytegain/custom/model_data/bucket.c"]),
                                  Extension("bytegain/custom/model_data/extractor",
                                            ["bytegain/custom/model_data/extractor.c"])]}

for extension in EXTRA_ARGS['ext_modules']:
    extension.cython_directives = {'language_level': "3"}

# Luckily we don't need this anymore.  When we do again, just uncomment and add tensorflow (or tensorflow-gpu) to the install_requires below.
# import tensorflow as tf
# EXTRA_ARGS['ext_modules'].append(Extension("bytegain/nn_tools/custom_op/sparse_row_to_dense",
#                                            ["bytegain/nn_tools/custom_op/sparse_row_to_dense.cc"],
#                                            extra_compile_args=["-std=c++11", "-I%s" % tf.sysconfig.get_include()]))
setup(name='al-model-trainer',
      version='0.3.0',
      description='ByteGain Custom Model code',
      url='https://github.com/apartmentlist/bytegain-training',
      author='Tom Collier',
      author_email='collier@apartmentlist.com',
      license='Commercial',
      packages=find_packages(),
      install_requires= _dataflow_deps,
      zip_safe=False,
      **EXTRA_ARGS)

# Clean up .egg-info that causes pip install problems, only when the package is created
if 'sdist' in sys.argv:
    for d in glob.glob('*.egg-info'):
        if os.path.isdir(d):
            shutil.rmtree(d)
