from setuptools import setup, find_packages
setup(
    name='CardinalNumeral',
    version='1.4dev',
    # packages=[
	# 	'cardinal_numeral',
	# 	'cardinal_numeral.language.english.sound',
	# 	'cardinal_numeral.language.english',
	# 	'cardinal_numeral.language.vietnamese',
	# 	'cardinal_numeral.language.vietnamese.sound',
	# 	'cardinal_numeral.tts'
	# ],
	packages = find_packages(include=['cardinal_numeral', 'cardinal_numeral.*']),
    license='Coffee License',
	# package_dir={'cardinal_numeral': './cardinal_numeral'},
	install_requires = [
		'pygame', 'pyogg', 'tinytag'
	],
	include_package_data=True,
	package_data={'cardinal_numeral': ['*.ogg']}
    # long_description=open('README.txt').read(),
)