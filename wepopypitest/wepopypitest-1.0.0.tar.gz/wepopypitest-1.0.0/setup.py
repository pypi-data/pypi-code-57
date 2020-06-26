from setuptools import setup, find_packages 
  
long_description = 'Sample Package made for a demo'
  
setup( 
        name ='wepopypitest', 
        version ='1.0.0', 
        author ='Riccardo Pressiani', 
        author_email ='riccardo.pressiani@gmail.com', 
        description ='Demo Package.', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT',
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'wppypi = wepo_pypi_test.main:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='python package', 
        zip_safe = False
) 