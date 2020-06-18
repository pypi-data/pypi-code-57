from distutils.core import setup
setup(
  name = 'quantumdl',         # How you named your package folder (MyLib)
  packages = ['quantumdl'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='Apache License 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A Quantum Deep Learning Library!',   # Give a short description about your library
  author = 'Debabrata Roy Chowdhury',                   # Type in your name
  author_email = 'debabrata.rc@dexterai.com',      # Type in your E-Mail
  url = 'https://github.com/dexterai-lab/quantumdl',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/dexterai-lab/quantumdl/archive/v0.1-alpha.tar.gz',    # I explain this later on
  keywords = ['QUANTUM COMPUTING', 'DEEP LEARNING', 'PYTHON'],   # Keywords that define your package best
  python_requires=('>=3.6.0'),
  install_requires=[            # I get to this in a second
          'cirq'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'   # Again, pick a license
  ],
)