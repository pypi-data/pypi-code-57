from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

long_description = 'Commandline script to convert any video to a image with a sequence of average color strikes, in chronological order.'

setup( 
		name ='colorsofmotion', 
		version ='1.0.3', 
		author ='Lusorio', 
		author_email ='manuel.buenstorf@gmail.com', 
		url ='https://github.com/Lusori0/colorsofmotion', 
		description ='CLI-script to achieve colors of motion effect', 
		long_description = long_description, 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(),
		entry_points ={ 
			'console_scripts': [ 
				'colorsofmotion = colorsofmotion.__init__:main'
			] 
		}, 
		classifiers =( 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		), 
		keywords ='colorsofmotion video poster', 
		install_requires=['moviepy>=1.0.2', 'Pillow>=7.1.2', 'numpy>=1.18.5'],
		zip_safe = False
) 
