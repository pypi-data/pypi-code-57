import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thread-task",
    version="0.9.6",
    author="Christoph Gaukel",
    author_email="christoph.gaukel@gmx.de",
    description="organize and run thread tasks",
    long_description=long_description,
    url="https://github.com/ChristophGaukel/thread_task",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
