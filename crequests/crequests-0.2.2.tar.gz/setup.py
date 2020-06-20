import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crequests",
    version="0.2.2",
    author="Alex Skov Jensen",
    author_email="pydev@offline.dk",
    description="A lightweight cache wrapper for requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x821938/crequests",
    packages=["crequests"],
    license="MIT",
    keywords=["requests", "cache", "scrape", "scraping", "persistent", "persistance"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Intended Audience :: Developers",
    ],
    project_urls={
        "Documentation": "https://github.com/x821938/crequests",
        "Source": "https://github.com/x821938/crequests",
    },
    install_requires=["requests"],
)
