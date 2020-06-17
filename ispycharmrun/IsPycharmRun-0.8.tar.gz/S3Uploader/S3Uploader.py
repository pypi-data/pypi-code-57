import boto3
from botocore.exceptions import ClientError
import logging
import os
import time
from uploader.uploader import uploader

class S3Uploader(uploader):
    def __init__(self, region="us-west-2"):
        super(S3Uploader, self).__init__()
        self.region = region
        self.client = self._initClient()
        # tempPath = "puzzle-public/puzzle-public-test/public/{folder1}/DataAndroid_Upgrade/{folder2}"
        # self.bucketName_7z = tempPath.replace("/", os.sep)
        # tempPath = "puzzle-public/puzzle-public-test/public/{folderConf}/"
        # self.bucketName_conf = tempPath.replace("/", os.sep)
        # tempPath = "/Users/binjia/develop/S1GameClient_Android/Match3Project/DataAndroid/SubPackage/"
        # self.path_7z = tempPath.replace("/", os.sep)
        # tempPath = "Match3Project/Assets/StreamingAssets/conf/"
        # self.path_alpha = tempPath.replace("/", os.sep)
        # tempPath = "Match3Project/Assets/StreamingAssets/conf/"
        # self.path_serverList = tempPath.replace("/", os.sep)
        # self.fileName_alpha = "alpha_update.xml"
        # self.fileName_serverList = "alpha_serverlist.xml"

    def _initClient(self):
        client = boto3.client(
            "s3",
            region_name = self.region,
            aws_access_key_id = "AKIAV5IWKTRTPWUW6FCK",
            aws_secret_access_key = "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",
        )
        return client

    def getFileList(self, path):
        files = os.listdir(path)  # 得到文件夹下的所有文件名称
        s = []
        for file in files:  # 遍历文件夹
            if not os.path.isdir(file):
                s.append(file)
        return s

    # def listExistingBuckets(self):
    #     resp = self.client.get_bucket_tagging(Bucket='my-bucket')
    #     tagList = resp["TagSet"]
    #     for tag in tagList:
    #         print(tag)

    def uploadFile(self, fileName, remotePath, **kwargs):
        # try:
        bucketName = kwargs["bucketName"]
        # except IndexError as e:
        #     print(e)
        #     bucketName = None
        # if objName is None:
        #     objName = fileName
        if remotePath[-1] == "/":
            remotePath = remotePath[:-1]
        elif remotePath[0] == "/":
            remotePath = remotePath[1:]
        try:
            print(remotePath + "/" + fileName.split(os.sep)[-1])
            response = self.client.upload_file(fileName, bucketName, remotePath + "/" + fileName.split(os.sep)[-1])
        except ClientError as e:
            logging.error(e)
            return False
        return True

if __name__ == '__main__':
    a = S3Uploader(region="us-west-2")
    bucketName = "puzzle-public"
    print(a.uploadFile("uploadTestFile32342", "puzzle-public-test/public/1210/uploadTestFile32342", bucketName=bucketName))