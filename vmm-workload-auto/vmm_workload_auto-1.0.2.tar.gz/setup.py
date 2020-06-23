# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
Setup file.
'''
#from distutils.core import setup
import os
from setuptools import setup, find_packages

def read(fname):
    '''
    Read the file contents for lomng description.
    '''
    with open(os.path.join(os.path.dirname(__file__), fname),
              encoding='utf-8') as file_desc:
        file_data = file_desc.read()
    str_var = ""
    for file_ln in file_data.split("\n"):
        if not file_ln.startswith("#"):
            str_var = str_var + file_ln + "\n"
    return str_var

vmm_env = os.getenv("VMM_TMP_VENV")
if vmm_env is None:
    CFG_DIR = '/etc/vmm_workload_auto'
else:
    CFG_DIR = './etc/vmm_workload_auto'

setup(name='vmm_workload_auto',
      version='1.0.2',
      description='Workload Automation for VMM',
      author='Padmanabhan Krishnan',
      author_email='padkrish@cisco.com',
      url='https://www.cisco.com',
      long_description=read('./README.txt'),
      long_description_content_type='text/x-rst',
      #package_dir={'vmm_workload_auto': 'workload_auto'},
      #packages=['vmm_workload_auto'],
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      #data_files=[('/etc/vmm_workload_auto',
      data_files=[(CFG_DIR,
                   ['config/conf.yml',
                    'config/sample.csv',
                    'config/conf_multiple_dcnm.yml',
                    'config/conf_multiple_vcenter.yml'])],
      install_requires=[
          'pyvim', 'pyvmomi', 'PyYAML', 'Flask',
      ],
      entry_points={
          'console_scripts': ['vmm_workload_auto = workload_auto.main:wl_auto_main']
      },
      scripts=['setup.sh'],
      zip_safe=False,)
