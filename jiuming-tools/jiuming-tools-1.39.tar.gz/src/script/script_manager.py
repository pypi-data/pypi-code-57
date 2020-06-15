import copy
import os
import stat
import time

import click
import yaml

from src.config.global_config import config_default_file, script_default_file

script_config_default_file = config_default_file + '/script_config.yaml'


def script_create(type, name, remark):
    """
        添加服务配置
        :param type: 脚本类型名称
        :param name: 服务器名称
        :param remark: 脚本备注
        :return:
        """
    # 追加模式
    s_file_path = script_default_file + '/{}'.format(name)
    if os.path.exists(s_file_path):
        # todo ming 删除文件 和配置
        pass
    y_file = open(script_config_default_file, 'a+')
    sc = ScriptConfig(type=type, name=name, remark=remark, path=s_file_path)
    yaml.safe_dump([sc.__dict__], y_file)
    s_file = open(s_file_path, 'w+')
    write_str = """#!/usr/bin/env {} 
#author ming 
#创建时间:{} 
#{}
""".format(type, time.strftime('%Y-%m-%d %H:%M:%S'), remark)
    s_file.write(write_str)
    s_file.close()
    os.chmod(s_file_path, stat.S_IRWXU)
    os.system('vi {}'.format(s_file_path))


def script_remove(name):
    """
    删除服务器配置信息
    获取所有配置  删除其中name符合的数据
    :param name: 服务器名称
    :return:
    """
    y_read_file = open(script_config_default_file, 'r')
    config_list = yaml.safe_load(y_read_file)
    if config_list is None:
        click.echo("暂无服务器配置信息!")
        return
    # 深拷贝 配置列表 进行操作列表
    new_config_list = copy.deepcopy(config_list)
    for c in config_list:
        sc = ScriptConfig.to_obj(c)
        if sc.name == name:
            new_config_list.remove(c)
            click.echo("删除{}服务器".format(sc.name))
    # 重新打开链接
    if len(new_config_list) != 0:
        yaml.safe_dump(new_config_list, open(script_config_default_file, 'w+'))
    else:
        # 清空配置
        open(script_config_default_file, 'w+').truncate()
        click.echo("服务器配置已清空!")


class ScriptConfig(object):
    """
    脚本配置 对象
    """
    # 脚本类型  如 sh  bash  python   以linux shell的脚本引擎名称   执行脚本的时候  就是 type ./xxx
    type: str
    # 脚本名称
    name: str
    # 脚本备注
    remark: str
    # 脚本地址
    path: str

    def __init__(self, type, name, remark, path):
        self.type = type
        self.name = name
        self.remark = remark
        self.path = path

    @staticmethod
    def to_obj(d: dict):
        """
        将读取的dict 转换为 serverConfig
        :param d:  dict
        :return: ServerConfig
        """
        return ScriptConfig(type=d['type'], name=d['name'],
                            remark=d['remark'], path=d['path'])
