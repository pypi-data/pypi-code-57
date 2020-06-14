from distutils.core import setup
setup(
    name='mediapart_bot_core',
    packages=['mediapart_bot_core'],
    version='1.0.0-beta.1',
    license='MIT',
    description='Provide tools to parser and download Mediapart articles as PDF.',
    author='Robin Perice',
    author_email='robin.perice@protonmail.com',
    url='https://github.com/r0perice/mediapart-bot-core',
    download_url='https://github.com/r0perice/mediapart-bot-core/archive/1.0.0-beta.1.tar.gz',
    install_requires=[
          'feedparser',
          'beautifulsoup4',
          'requests',
      ],

)