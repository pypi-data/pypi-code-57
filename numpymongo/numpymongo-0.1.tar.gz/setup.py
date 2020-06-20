from setuptools import setup

setup(name='numpymongo',
      version='0.1',
      description='A wrapper to export NumPy data to MongoDB',
      url='https://github.com/manuel-lang/NumpyMongo',
      author='Manuel Lang',
      author_email='manuellang183@gmail.com',
      license='MIT',
      packages=['numpymongo'],
      install_requires=[
          'pymongo',
          'numpy',
      ],
      zip_safe=False)