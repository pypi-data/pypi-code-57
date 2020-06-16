#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
import os
from stat import S_ISDIR as isdir

paramiko.util.log_to_file("paramiko.log")
import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


class DownLoadManager:
    def __init__(self, user_name, password, file_name):
        # meta data
        self.host_name = '10.141.221.89'
        self.user_name = user_name
        self.password = password
        self.port = 22
        self.name_records = {"annotation_sentence_vote_valid.json", "1.txt"}
        similar_score = 0
        similar_name = file_name

        for name in self.name_records:
            score = string_similar(name, file_name)
            if similar_score < score:
                similar_score = score
                similar_name = name
        # remote path
        self.remote_dir = '/home/fdse/data/' + similar_name
        # local path
        self.local_dir = 'file_download/'

        # link
        self.transport = paramiko.Transport((self.host_name, self.port))
        self.transport.connect(username=self.user_name, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def start_download(self):
        print(self.remote_dir)
        self.down_from_remote(self.sftp, self.remote_dir, self.local_dir)

    def close_link(self):
        if self.sftp: self.sftp.close()
        if self.transport: self.transport.close()

    def down_from_remote(self, sftp_obj, remote_dir_name, local_dir_name):
        remote_file = sftp_obj.stat(remote_dir_name)
        if isdir(remote_file.st_mode):
            print(remote_dir_name)
            # dir -> loop
            check_local_dir(local_dir_name)
            local_dir_name = DownLoadManager.create_dir(local_dir_name, remote_dir_name.split("/")[-1])
            print('start download dir:' + remote_dir_name)
            for remote_file_name in self.sftp.listdir(remote_dir_name):
                sub_remote = os.path.join(remote_dir_name, remote_file_name)
                sub_remote = sub_remote.replace('\\', '/')
                sub_local = os.path.join(local_dir_name, remote_file_name)
                sub_local = sub_local.replace('\\', '/')
                self.down_from_remote(sftp_obj, sub_remote, sub_local)
        else:
            print('start download file:' + remote_dir_name)
            if not os.path.isfile(local_dir_name):
                local_dir_name = local_dir_name + "/" + remote_dir_name.split("/")[-1]
            self.sftp.get(remote_dir_name, local_dir_name)

    @staticmethod
    def create_dir(work_dir, dir_n):
        try:
            if not os.path.exists(os.path.join(work_dir, dir_n)):
                p = os.path.join(work_dir, dir_n)
                os.makedirs(p)
                print("%s created" % dir_n)
                return p
            else:
                print("dir exist")
                return ""
        except Exception as e:
            print(e)
            return ""


def check_local_dir(local_dir_name):
    if not os.path.exists(local_dir_name):
        os.makedirs(local_dir_name)

