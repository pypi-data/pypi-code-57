import setuptools

setuptools.setup(
    name="ANIBBLE_X",
    version="0.7.2",
    url="",
    author="Mélanie Sawaryn",
    author_email="melanie.sawaryn@gmail.com",
    description="Creation of html graph from networkx",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    data_files = [("data_VIS",["data/vis.js","data/vis.css"])],
)
