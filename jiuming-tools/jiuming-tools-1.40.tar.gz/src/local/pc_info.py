import os
import re
import subprocess

import click
import psutil


def echo_pc_info():
    """
    输出 设备产品信息
    :return:
    """
    os_info = os.uname()
    # 获取当前系统虚拟化方式
    virtual_type_str = str.split(subprocess.getoutput("lscpu | grep -E  '超管理器厂商|Hypervisor vendor'").strip(''))[1]

    memory_info_str = '''
操作系统:
  用户名:     {}
  主机名:     {}
  发行版本:   {}
  内核版本:   {}
  硬件架构:   {}
  虚拟化方式:  {}
cpu信息:
  cpu型号:    {}
  cpu物理核心: {}
  cpu逻辑核心: {}
  
内存信息:
{}

网卡信息:
{}

磁盘信息:
{}
        '''.format(
        os.getlogin(),
        os_info.nodename,
        subprocess.getoutput('cat /etc/issue').strip('\n'),
        os_info.release,
        os_info.machine,
        virtual_type_str,
        cpu_info().modelName,
        psutil.cpu_count(logical=False),
        psutil.cpu_count(),
        subprocess.getoutput('free -h'),
        subprocess.getoutput('ip addr'),
        subprocess.getoutput('df -h')
    )
    click.echo(memory_info_str)


def cpu_info():
    """
    从 /proc/cpuinfo 中读取cpu 模型名称
    :return:
    """
    f_cpu_info = open('/proc/cpuinfo', 'r')
    c = f_cpu_info.readlines()
    for i in c:
        tmp_str_list = i.split(':')
        if re.match(".*model.*name.*", tmp_str_list[0]):
            return cpuInfo(tmp_str_list[1].strip('\n').strip('\t'))


class cpuInfo(object):
    def __init__(self, modelName):
        self.modelName = modelName


def byteToGb(byteNumber):
    # b   kb     mb      gb
    return str(format(byteNumber / 1024 / 1024 / 1024, '.3'))
