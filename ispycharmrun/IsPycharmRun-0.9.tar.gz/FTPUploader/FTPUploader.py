from ftplib import FTP
import ftplib
from uploader.uploader import uploader
import os

class ftpUploader(uploader):
    def __init__(self):
        super(ftpUploader, self).__init__()
        self.client = self._initClient()

    def _initClient(self):
        client = FTP()
        client.set_debuglevel(2)
        client.connect("10.0.107.63", 21)
        client.login("zhouxin", "123456")
        return client

    def makeRemoteDir(self, pathName):
        subDirList = pathName.split("/")
        if subDirList[-1] == "":
            subDirList = subDirList[:-1]
        print(subDirList)
        self.client.cwd("/")
        for subDir in subDirList:
            try:
                self.client.cwd(subDir)
            except ftplib.error_perm:
                print("creat remote dir - %s"%subDir)
                self.client.mkd(subDir)
                self.client.cwd(subDir)

    def enterDir(self, pathName):
        subDirList = pathName.split("/")
        if subDirList[-1] == "":
            subDirList = subDirList[:-1]
        self.client.cwd("/")
        for subDir in subDirList:
            print("enter dir - %s"%subDir)
            self.client.cwd(subDir)

    def uploadFile(self, fileName, remotePath, **kwargs):
        if remotePath[-1] == "/":
            remotePath = remotePath[:-1]
        elif remotePath[0] == "/":
            remotePath = remotePath[1:]
        try:

            buffSize = 1024
            file = open(fileName, "rb")
            print(file)
            print("STOR %s"%("/"+remotePath+"/"+fileName.split(os.sep)[-1]), file, buffSize)
            self.client.storbinary("STOR %s"%("/"+remotePath+"/"+fileName.split(os.sep)[-1]), file, buffSize)
            self.client.set_debuglevel(0)
            file.close()
            # self.client.close()
            return True
        except Exception as e:
            print(e)
            return False

    def quitFTP(self):
        self.client.quit()

if __name__ == "__main__":
    a = ftpUploader()
    print(a.uploadFile("uploadTestFile", "android"))
