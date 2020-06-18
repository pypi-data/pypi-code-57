from setuptools import setup, find_packages

setup(name='datadbs',
      version='0.1.3',
      description='DataDBS are some class to manage data NoSQL type',
      url='http://www.gitlab.com/dpineda/datadbs',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='MIT',
      packages=['datadbs'],
      install_requires=['networktools', 'basic-logtools'],
      package_dir={'datadbs': 'datadbs'},
      package_data={
          'datadbs': ['../doc', '../docs', '../requeriments.txt']},
      include_package_data=True,      
      zip_safe=False)
