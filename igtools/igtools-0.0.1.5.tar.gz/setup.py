from distutils.core import setup
import os
os.system("rm -rf dist")
setup(
  name = 'igtools',         # How you named your package folder (MyLib)
  packages = ['igtools'],   # Chose the same as "name"
  version = '0.0.1.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Instagram Scraping tools and bot',   # Give a short description about your library
  long_description = """
Create A Login Session :

ex : 

a=igtools.Session()

a.login("username","pass") #login to instagram

print (a.is_login) #Return True If Succed login

a.follow("Username") #Following People

a.unfollow("username") #unfollowing people

a.likes("username") #like the first post of user

a.comments("username","comment") #comment first post of user

a.changepass("newpassword") #change your password

a.changemail("newemail") # change your email

a.changephone("newphone") # change your phone number

a.changebio("newbio") # change your biography

Instagram Scraping :

ex :

igtools.get_followers("username",max=1000) #Generator object,use it in loop
  ex: for i in igtools.get_followers("username",max=1000):
	  print u

igtools.getbyhashtag("hashtagname",max=1000) #Generator object too

igtools.get_followings("username",max=max) #generator object

igtools.getuserpost("username",max=10) #getting post id by username

igtools.search("username") #getting search list in instagram

igtools.getuserid("username") #getting username numeric id

igtools.login("Username","password",print_=False) # return true if login success



for future update please subscribe my channel : JustA Hacker
contact : whatsaapp (6289682009902)
""",
  author = 'JustAHacker',                   # Type in your name
  author_email = 'rafasyahagung@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/justahackers/animate',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/animate.tar.gz',    # I explain this later on
  keywords = ['instagram', 'python', 'tools'],   # Keywords that define your package best
  install_requires=['requests','bs4'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
os.system("twine upload dist/*")
