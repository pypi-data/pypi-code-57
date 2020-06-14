from distutils.core import setup
setup(
    name='CardinalNumeral',
    version='0.4dev',
    packages=['cardinal_numeral',],
    license='Coffee License',
	package_dir={'cardinal_numeral': './cardinal_numeral'},
	include_package_data=True
    # long_description=open('README.txt').read(),
)