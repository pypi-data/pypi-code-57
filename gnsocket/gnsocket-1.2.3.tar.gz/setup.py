from setuptools import setup, find_packages

setup(name='gnsocket',
      version='1.2.3',
      description='GPS Network Socket, with asyncio stream manager',
      url='https://gitlab.com/pineiden/gus',
      author='David Pineda Osorio',
      author_email='dpineda@csn.uchile.cl',
      license='GPL3',
      install_requires=["networktools","basic_queuetools", "basic_logtools",'chardet'],
      packages=find_packages(),      
      include_package_data=True,      
      package_dir={'gnsocket': 'gnsocket'},      
      zip_safe=False)
