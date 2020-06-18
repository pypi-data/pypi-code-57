from setuptools import setup, find_packages

setup(name='tasktools',
      version='1.0.2',
      description='Some useful tools for asycnio Tasks: async while, the Scheduler and Assignator classes',
      url='https://tasktools.readthedocs.io/en/latest/',
      author='David Pineda Osorio',
      author_email='dpineda@uchile.cl',
      license='GPL3',
      install_requires=['networktools'],      
      package_dir={'tasktools': 'tasktools'},
      package_data={
          'tasktools': ['../doc', '../docs', '../requeriments.txt']},
      packages=find_packages(),
      include_package_data=True,      
      zip_safe=False)
