import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipywidgets_game_maze", 
    version="0.0.1",
    author="Edwige GROS",
    author_email="edwige.gros@laposte.net",
    description="Solve a 3 dimentional maze with Jupyter Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.u-psud.fr/edwige.gros/ipywidgets-games.git",
    include_package_data=True,
    data_files=[
        # like `jupyter nbextension install --sys-prefix`
        ("nbextensions/ipywidgets_game_maze", ["ipywidgets_game_maze/static/tete3.jpg","ipywidgets_game_maze/static/seville.jpg"])
    ],
    packages=setuptools.find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
     install_requires = ['timer', 'ipywidgets', 'pythreejs'],
    python_requires='>=3.6',
)
