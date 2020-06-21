from distutils.core import setup
setup(
  name = 'weatherbitpypi',
  packages=['weatherbitpypi'],
  package_data={
    "": ["*.md"],
    "weatherbitpypi": ["translations/*.json"],
  },
  version = '0.23.1',
  license='MIT',
  description = 'Python Wrapper for Weatherbit API', 
  author = 'Bjarne Riis',
  author_email = 'bjarne@briis.com',
  url = 'https://github.com/briis/py-weatherbit',
  keywords = ['Weatherbit', 'Forecast', 'Python'],
  install_requires=[
          'asyncio',
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers', 
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)