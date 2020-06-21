import setuptools

setuptools.setup(
    name="musurgia",
    version="2.2.1beta",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="tools for algorithmic composition",
    url="https://github.com/alexgorji/musurgia.git",
    packages=setuptools.find_packages(),
    install_requires=['quicktions',
                      'musicscore',
                      'prettytable',
                      'fpdf2',
                      'diff-pdf-visually',
                      'matplotlib'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
