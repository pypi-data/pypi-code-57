
import site, shutil, os, sys

#print(site.getusersitepackages()) # https://stackoverflow.com/questions/122327/how-do-i-find-the-location-of-my-python-site-packages-directory

s = site.getusersitepackages()
shutil.copyfile(s+"/pyabr/pyabr.zip","pyabr.zip")
shutil.unpack_archive("pyabr.zip","pyabr-install","zip")
os.system("cd pyabr-install && \""+sys.executable+"\" setup.py")
shutil.rmtree("pyabr-install")
os.remove("pyabr.zip")
