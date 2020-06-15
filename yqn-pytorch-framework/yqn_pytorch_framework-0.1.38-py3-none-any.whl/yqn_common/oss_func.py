import os
import re

import oss2
import sys

import yaml

HASH_REGEX = re.compile(r'-([a-f0-9]*)\.')
HOST_URL = "https://ai-models-yqn.oss-cn-hangzhou.aliyuncs.com"


def oss_calculate_file_crc64(file_name, block_size=64 * 1024, init_crc=0):
    """计算文件的MD5
    :param file_name: 文件名
    :param block_size: 计算MD5的数据块大小，默认64KB
    :return 文件内容的MD5值
    """
    with open(file_name, 'rb') as f:
        crc64 = oss2.utils.Crc64(init_crc)
        while True:
            data = f.read(block_size)
            if not data:
                break
            crc64.update(data)

    return crc64.crc


class OSSUpload:
    def __init__(self, app_id, version, bucket):
        self.app_id = app_id
        self.version = version
        self.bucket = bucket

    def upload_dir(self, dir_path):
        dist_start_path = os.path.join(self.app_id, self.version).__str__()
        self.rm_exist_version(dist_start_path)
        outputs = []
        self.add_file_to_oss(dir_path, dist_start_path, outputs)
        with open(r'./model_url_config.yml', 'w') as file:
            documents = yaml.dump(outputs, file)

    def add_file_to_oss(self, src, dist, outputs):
        for file_name in os.listdir(src):
            new_dist = os.path.join(dist, file_name)
            new_src = os.path.join(src, file_name)
            if os.path.isdir(new_src):
                self.add_file_to_oss(new_src, new_dist, outputs)
            else:
                result = self.bucket.put_object_from_file(new_dist, new_src, progress_callback=self.percentage)
                assert result.status == 200
                crc64 = result.headers['x-oss-hash-crc64ecma']
                file_url = os.path.join(HOST_URL, new_dist).__str__()
                local_path = new_src
                outputs.append({
                    "local_path": local_path,
                    "file_url": file_url,
                    "crc": crc64,
                })

    @staticmethod
    def percentage(consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end='')
            sys.stdout.flush()

    def rm_exist_version(self, version_dir):
        for obj in oss2.ObjectIterator(self.bucket, prefix=version_dir):
            self.bucket.delete_object(obj.key)
