import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tasklist",
    version="1.2.1",
    author="BuddyNS.com",
    author_email="support@buddyns.com",
    description="A library to manage lists of commands with re-trial.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/buddyns/tasklist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: System"
    ],
)
