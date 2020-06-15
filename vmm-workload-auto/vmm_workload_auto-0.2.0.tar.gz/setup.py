# Copyright 2020 Cisco Systems, Inc.
# All Rights Reserved.
#
#
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
        return file_desc.read()

vmm_env = os.getenv("VMM_TMP_VENV")
if vmm_env is None:
    CFG_DIR = '/etc/vmm_workload_auto'
else:
    CFG_DIR = './etc/vmm_workload_auto'

setup(name='vmm_workload_auto',
      version='0.2.0',
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
