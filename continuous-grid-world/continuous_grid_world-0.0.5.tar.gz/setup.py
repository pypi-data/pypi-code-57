import setuptools

setuptools.setup(name='continuous_grid_world',
    version='0.0.5',
    author="Christoper Glenn Wulur",
    packages=[package for package in setuptools.find_packages() if package.startswith('continuous_grid_world')],
    zip_safe=False,
    author_email="christoper.glennwu@gmail.com",
    description="Grid World with continuous action spaces",
    install_requires=['gym']#And any other dependencies required
)
