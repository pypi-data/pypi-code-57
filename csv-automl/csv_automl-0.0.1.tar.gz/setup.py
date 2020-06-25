from distutils.core import setup
setup(
  name = 'csv_automl',         # How you named your package folder (MyLib)
  packages = ['csv_automl'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='bsd-2-clause',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'AutoML on CSV',   # Give a short description about your library
  author = 'Juliett Yi Chen',                   # Type in your name
  author_email = 'juliettyi@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/juliettyi/csv_automl',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/juliettyi/csv_automl/archive/v_001.tar.gz',    # I explain this later on
  keywords = ['csv', 'automl'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      'sklearn',
      'numpy',
      'torch',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: BSD License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
