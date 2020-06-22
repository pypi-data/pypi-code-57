from setuptools import setup, find_packages

setup(
    name='youtubelight',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['requests'],
    #url='https://github.com/seferaua/django-convert-doc-to-pdf',
    long_description="This library makes it easy to communicate with the YouTube API v3. "
                     "This library can easily keep track of information: channel info, playlist info, "
                     "playlistitem info, video info, video comment info",
    author="Sergey Savchenko"
)