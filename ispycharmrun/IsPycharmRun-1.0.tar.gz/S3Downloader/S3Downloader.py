import boto3
from botocore.exceptions import ClientError
import logging

class s3Downloader:
    def __init__(self):
        self.client = self._initClient()

    def _initClient(self):
        client = boto3.client(
            "s3",
            aws_access_key_id = "AKIAV5IWKTRTPWUW6FCK",
            aws_secret_access_key = "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",
        )
        return client

    #下载成功返回1，远端无文件返回2，否则返回false
    def downloadFile(self, fileName, remotePath, **kwargs):
        bucketName = kwargs["bucketName"]
        if remotePath[-1] == "/":
            remotePath = remotePath[:-1]
        elif remotePath[0] == "/":
            remotePath = remotePath[1:]
        try:
            self.client.download_file(bucketName, remotePath, fileName)
        except ClientError as e:
            if e.response["Error"]["Message"] == "Not Found":
                return 2
            else:
                logging.error(e)
                return False
        return 1

if __name__ == '__main__':
    a = s3Downloader()
    print(a.downloadFile("1234.xml", "puzzle-public-test/public/alpha_update123123.xml", bucketName="puzzle-public"))