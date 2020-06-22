from setuptools import setup, Extension

with open('README.md') as f:
    readme = f.read()

setup(
    name = 'kaggleDownloader',         # How you named your package folder (MyLib)
    packages = ['kaggleDownloader'],   # Chose the same as "name"
    version = '4.2.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'Helps you to download the Kaggle Dataset to your Google Colab Notebook using Kaggle Dataset API link',   # Give a short description about your library
    long_description = readme,
    long_description_content_type = 'text/markdown',
    author = 'Antoreep Jana',                   # Type in your name
    author_email = 'antoreepjana@gmail.com',      # Type in your E-Mail
    url = 'https://gitlab.com/antoreep_jana/kaggledownloader/tree/master',   # Provide either the link to your github or to your website
    download_url = 'https://gitlab.com/antoreep_jana/kaggledownloader/-/archive/4.2.1/kaggledownloader-4.2.1.tar.gz',    # I explain this later on
    keywords = ['Kaggle Downloader' , 'Kaggle Dataset Downloader', 'dataset downloader' , 'Google Colab', 'kaggle dataset download in google colab' ],   # Keywords that define your package best
    #install_requires=[            # I get to this in a second
    #       
    #    ],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)
