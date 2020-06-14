from distutils.core import setup
from glob import glob

package_data = [filename.replace('micromlgen/', '')
                for filename in glob('micromlgen/**/*.jinja', recursive=True)]

setup(
  name = 'micromlgen',
  packages = ['micromlgen'],
  version = '1.1.1',
  license='MIT',
  description = 'Generate C code for microcontrollers from Python\'s sklearn classifiers',
  author = 'Simone Salerno',
  author_email = 'eloquentarduino@gmail.com',
  url = 'https://github.com/eloquentarduino/micromlgen',
  download_url = 'https://github.com/eloquentarduino/micromlgen/archive/v_111.tar.gz',
  keywords = [
    'ML',
    'microcontrollers',
    'sklearn',
    'machine learning'
  ],
  install_requires=[
    'jinja2',
    'scikit-learn'
  ],
  package_data= {
    'micromlgen': package_data
  },
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Code Generators',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)