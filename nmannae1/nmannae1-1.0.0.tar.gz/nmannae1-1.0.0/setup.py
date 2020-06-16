from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

long_description = 'bruteforce resistant encryption'

setup( 
		name ='nmannae1', 
		version ='1.0.0', 
		author ='neelanjan manna ', 
		author_email ='neelanjanmanna1997@gmail.com', 
		#url ='https://github.com/NeelanjanManna-max/e1', 
		description ='demo package for learning', 
		long_description = long_description, 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(), 
		#entry_points ={ 
		#	'console_scripts': [ 
		#		'gfg = vibhu4gfg.gfg:main'
		#	] 
		#}, 
		classifiers =[
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		], 
		keywords ='neelanjan manna e1', 
		install_requires = requirements, 
		zip_safe = False
) 
