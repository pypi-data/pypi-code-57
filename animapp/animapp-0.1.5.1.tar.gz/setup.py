import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="animapp",
    version="0.1.5.1",
    author="Srinivasa Rao",
    author_email="srinivasarao.rao@gmail.com",
    description="A package to track the movement of an object (a small animal) in a video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sraorao/animapp_pyqt5",
    packages=setuptools.find_packages(),
    # scripts=['bin/animapp', 'bin/threshold'],
    entry_points={'console_scripts': ['threshold=animapp.set_thresholds:main', 'animapp=animapp.animapp:main'],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
