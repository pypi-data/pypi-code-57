from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='jprimee',
  version='0.0.1',
  description='Checks whether number is prime or not',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Jiganesh Patil',
  author_email='jiganeshpatil01071999@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='prime', 
  packages=find_packages(),
  install_requires=[''] 
)
