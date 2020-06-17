from uploader.uploader import uploader
import paramiko
from scp import SCPClient

class scpUploader(uploader):
    def __init__(self):
        super(scpUploader, self).__init__()
        self.host = "10.0.109.90"
        self.port = 22  # 端口号
        self.username = "binjia"  # ssh 用户名
        self.password = "831811"  # 密码

    def uploadFile(self, fileName, remotePath, **kwargs):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(self.host, self.port, self.username, self.password)
        scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
        try:
            scpclient.put(fileName, remotePath)
        except FileNotFoundError as e:
            print(e)
            print("系统找不到指定文件" + fileName)
        else:
            print("文件上传成功")
        ssh_client.close()

if __name__ == "__main__":
    a = scpUploader()
    a.uploadFile("/Users/shiboxuan/testTools/scpUploader/uploadTestFile32342","/Users/binjia/Sites")