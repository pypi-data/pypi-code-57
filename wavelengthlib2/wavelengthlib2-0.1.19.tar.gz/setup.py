from setuptools import setup, find_packages

setup(
   name='wavelengthlib2',
   version='0.1.19',
   description='Wavelength library 2',
   author='Simon',
   author_email='simon.elliott@wavelength.law',
   package_dir={'': '.'},
   packages=['wllib2','wllib2.lib_tests','wllib2.env_lib','wllib2.az_lib','wllib2.db_lib','wllib2.pdf_lib','wllib2.img_lib','wllib2.test_lib']
)