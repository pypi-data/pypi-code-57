import oss2
import os
import uuid
import time
from django.conf import settings
from tfduck.common.defines import BMOBJ, Et
import base64


class AliyunOss(object):
    """
    @des: 阿里云oss的基本操作
    """

    def __init__(self, bucket_name, aly_access_key_id, aly_access_key_secret, aly_endpoint):
        """
        @des:初始化
        """
        self.access_key_id = aly_access_key_id
        self.access_key_secret = aly_access_key_secret
        self.bucket_name = bucket_name
        # oss-us-east-1.aliyuncs.com
        self.endpoint = aly_endpoint
        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret),
                                  self.endpoint, self.bucket_name)

    def gen_local_unique_file(self, ext="csv"):
        """
        @des:生成本地文件唯一路径
        """
        if BMOBJ.get_current_env() == "server":
            media_root = settings.MEDIA_ROOT
            base_dir = os.path.join(media_root, "data")
        else:
            base_dir = os.path.join(os.environ.get('HOME', ''), "tmp/tfduck")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        real_name = "%s%s.%s" % (uuid.uuid1().hex, uuid.uuid1().hex, ext)
        file_path = os.path.join(base_dir, real_name)
        return file_path

    def download(self, remote_filename):
        """
        @des:下载oss文件到本地---head_object
        """
        BMOBJ.log_error("download", remote_filename,  "start")
        #
        unique_path = self.gen_local_unique_file()
        tmp_unique_file = "%s.tmp.json" % unique_path
        #
        total_retry = 18
        for i in range(total_retry):
            try:
                self.bucket.restore_object(remote_filename)
            except Exception as _:
                pass

            try:
                oss2.resumable_download(
                    self.bucket, remote_filename, tmp_unique_file)
                break
            except Exception as e:
                BMOBJ.remove_file(tmp_unique_file)
                if i >= total_retry-1:
                    raise e
                else:
                    time.sleep(10)
        os.rename(tmp_unique_file, unique_path)
        #
        BMOBJ.log_error("download", remote_filename,  "end")
        #
        if 0:
            with open(unique_path, 'rb') as f:
                file_content = f.read()
            BMOBJ.remove_file(unique_path)
            file_base64_str = base64.b64encode(file_content).decode()
            return file_base64_str
        else:
            with open(unique_path, 'r') as f:
                file_content = f.read()
            BMOBJ.remove_file(unique_path)
            #
            return file_content
        

    def upload(self, file_content, remote_filename):
        """
        @des:上传文件
        @param file_content: 字符串
        @param remote_filename: 上传到远程oss的路径
        """
        BMOBJ.log_error("upload",  "start")
        if type(file_content)!=str:
            raise Et(2, "file_content must be str")
        # local_filename = download_image_local(fid)
        unique_path = self.gen_local_unique_file()
        tmp_unique_file = "%s.tmp.json" % unique_path
        if 0:
            with open(tmp_unique_file, 'wb') as f:
                f.write(file_content)
        else:
            with open(tmp_unique_file, 'w') as f:
                f.write(file_content)
        os.rename(tmp_unique_file, unique_path)
        result = oss2.resumable_upload(
            self.bucket, remote_filename, unique_path)
        BMOBJ.remote_filename(unique_path)
        #
        BMOBJ.log_error(result)
        BMOBJ.log_error("upload",  "end")
        return True

    def exists(self, remote_filename):
        """
        @des: 判断oss上面文件是否存在
        """
        exists = self.bucket.object_exists(remote_filename)
        return exists
