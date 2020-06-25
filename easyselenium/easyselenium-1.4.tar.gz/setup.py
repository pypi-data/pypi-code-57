import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

    
setuptools.setup(
     name='easyselenium',    # This is the name of your PyPI-package.
     version='1.4',                          # Update the version number for new releases
              # The name of your scipt, and also the command you'll be using for calling it
     author="Ankit Kothari",
    author_email="ankit.kothari@hotmail.com",
    description="This is a selenium easy library which has easy syntax build on selenium.all the things are running in background we are calling only functions..This is too easy for begineers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    keywords =['selenium','ankit kothari','step2success','easyselenium','easy-selenium','python selenium','selenium webdriver'],
    
    
    
    
    url="https://github.com/ankitk29kothari/Step2success/tree/master/Selenium-Web%20Automation/easy_selenium",
    packages=setuptools.find_packages(),
    
  	download_url = 'https://github.com/ankitk29kothari/Step2success/tree/master/Selenium-Web%20Automation/easy_selenium', 
    license = 'GPLv2',
    classifiers = ["Programming Language :: Python"],
    python_requires='>=3.6',

     install_requires=[
          'setuptools',
          'selenium',
          'webdriver-manager',
          # -*- Extra requirements: -*-
      ],
   

)