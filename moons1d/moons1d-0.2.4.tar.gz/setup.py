from setuptools import find_packages, setup

def setup_package():
    setup(
        name='moons1d',
        packages=find_packages(),
        version='0.2.4',
        description='1D simulator for MOONS/VLT',
        author='Myriam Rodrigues',
        license='MIT',
        author_email="myriam.rodrigues@obspm.fr",
        url="https://gitlab.obspm.fr/mrodrigues/moons1d",
        include_package_data=True,
        install_requires=["numpy>=1.16",
           "astropy==3.0.0",
           "configobj",
           "matplotlib",
           "pyparsing",
           "scipy",
           "skycalc_ipy",
           "numpy"
           ],
           )

if __name__ == '__main__':
    setup_package()