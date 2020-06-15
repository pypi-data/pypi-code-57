from distutils.core import setup
setup(
  name = 'bsoid',         # How you named your package folder (MyLib)
  packages = ['bsoid'],   # Chose the same as "name"
  version = '0.1.3',      # Start with a small number and increase it with every change you make
  license='GPL-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An open-source machine learning algorithm for parsing spatio-temporal patterns.',   # Give a short description about your library
  author = 'Alex Hsu',                   # Type in your name
  author_email = 'ahsu2@andrew.cmu.edu',      # Type in your E-Mail
  url = 'https://github.com/YttriLab/B-SOID',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/runninghsus/Bsoid/archive/v0.1.3.tar.gz',    # I explain this later on
  keywords = ['Unsupervised learning', 'UMAP', 'HDBSCAN', 'Behavioral extraction'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'tqdm',
          'matplotlib',
          'opencv-python',
          'seaborn',
          'scikit-learn',
          'umap-learn',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
