from distutils.core import setup
setup(
  name = 'pioton',         # How you named your package folder (MyLib)
  packages = ['pioton'],   # Chose the same as "name"
  version = '0.3.0',      # Start with a small number and increase it with every change you make
  license='GPL',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'píotón language is a superset of Python allowing it to be written in Irish. Not for use in any important work',   # Give a short description about your library
  author = 'Luke Roantree',                   # Type in your name
  author_email = 'luke@roantree.com',      # Type in your E-Mail
  url = 'https://github.com/LukeRoantree4815162342/pioton',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/LukeRoantree4815162342/pioton/archive/v_030.tar.gz',    # I explain this later on
  keywords = ['IPython', 'Gaeilge', 'Irish'],   # Keywords that define your package best
  install_requires=['ipython'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License (GPL)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
