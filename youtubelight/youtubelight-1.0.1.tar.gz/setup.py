from setuptools import setup, find_packages

setup(
    name='youtubelight',
    version='1.0.1',
    packages=find_packages(),
    install_requires=['requests'],
    url='https://github.com/seferaua/light_youtube_python_api_v3',
    long_description="This library makes it easy to communicate with the YouTube API v3. "
                     "This library can easily keep track of information: channel info, playlist info, "
                     "playlistitem info, video info, video comment info. ",
    author="Sergey Savchenko"
)