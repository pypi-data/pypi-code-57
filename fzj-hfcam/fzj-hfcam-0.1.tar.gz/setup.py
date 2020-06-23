from setuptools import setup, find_packages

setup(
	name = 'fzj-hfcam',
	author = 'Alexander Knieps',
	author_email = 'a.knieps@fz-juelich.de',
	description = 'Virtual camera to convert point-clouds into heat-flux mappings',
	py_modules = ['hfcam'],
    version = '0.1',
	install_requires = [
        'numba>=0.44.1',
		'numpy>=1.16.0'
	]
);

