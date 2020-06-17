import os
import sys
import json

sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0] + "/../../")

from aos.constant import OS_REPO, OS_CACHE
from aos.managers import addon
from aos.managers import repo
from aos.managers import sqlitedb
from aos.managers import rpmfile

c = addon.Cache()
c.create()

db = sqlitedb.PrimaryDB(c.primary_db)
print(json.dumps(db.getPackages([]), indent=4))

#db = sqlitedb.FilelistsDB(c.filelists_db)
#print(db.getFiles('603'))

r = repo.Repo(OS_REPO, OS_CACHE)
localfile = r.getPackage("activation-1.0.0-r0.aos.noarch.rpm")

#r = rpm.RPMFile("test/activation-1.0.0-r0.aos.noarch.rpm")
#r = rpmfile.RPMFile("test/buildsystem-1.0.1.3-r0.aos.noarch.rpm")
r = rpmfile.RPMFile(localfile)
r.install("/tmp/alios")
