from distutils.core import setup
setup(
    name='CardinalNumeral',
    version='0.5dev',
    packages=['cardinal_numeral','cardinal_numeral.language.english', 'cardinal_numeral.language.vietnamese','cardinal_numeral.tts'],
    license='Coffee License',
	package_dir={'cardinal_numeral': './cardinal_numeral'},
	include_package_data=True
    # long_description=open('README.txt').read(),
)