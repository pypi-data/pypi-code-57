import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitter_activity",
    version="0.0.1",
    author="sammer sallam",
    author_email="samersallam92@gmail.com",
    description="This library is to help you work with web-hook, Classify twitter account activities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Samer92/twitter_activity",
    packages=["twitter_activity/activity_manager","twitter_activity/webhook_manager"],
    install_requires=["certifi==2020.4.5.2", "chardet==3.0.4", "idna==2.9", "oauthlib==3.1.0", "PySocks==1.7.1", 
                      "requests==2.24.0", "requests-oauthlib==1.3.0", "six==1.15.0", "tweepy==3.8.0", "urllib3==1.25.9"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)