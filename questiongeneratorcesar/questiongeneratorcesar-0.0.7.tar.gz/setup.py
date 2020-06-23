import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        requirements = fd.read().splitlines()
        print(requirements)
        return requirements

setuptools.setup(
    name="questiongeneratorcesar", # Replace with your own username
    version="0.0.7",
    author="César Juárez Ramírez",
    author_email="cesar@wordbox.ai",
    description="Question generator package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wordbox-tech/Backend-Services-QuestionGenerator",
    packages=setuptools.find_packages(),
    package_data = {
        '': ['*.pk', '*.json', '*.csv'],
    },
    install_requires=list_reqs(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)