from setuptools import setup, find_packages
setup(
    name='CardinalNumeral',
    version='1.5dev',
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
	install_requires = [
		'pygame', 'pyogg', 'tinytag', 'requests'
	],
	include_package_data=True,
	package_data={'cardinal_numeral': ['*.ogg']}
    # long_description=open('README.txt').read(),
)