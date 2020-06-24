from distutils.core import setup
setup(
  name = 'syncmm',         # How you named your package folder (MyLib)
  packages = ['syncmm'],   # Chose the same as "name"
  version = '2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'You can sync your own music library',   # Give a short description about your library
  author = 'serg1evsky',                   # Type in your name
  author_email = 'niknamegreen3@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/serg1evsky/syncmm',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/serg1evsky/syncmm/archive/1.0.tar.gz',    # I explain this later on
  keywords = ['Sync', 'Music', 'vk'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'vk_api',
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license   #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
