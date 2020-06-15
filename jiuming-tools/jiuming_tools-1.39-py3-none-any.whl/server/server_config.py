# 默认配置路径
import copy
import os
import pathlib
import select
import sys
import termios
import tty

import click
import paramiko
import yaml

from src.config.global_config import config_default_file

# 默认配置file
server_config_default_file = config_default_file + '/server_config.yaml'


def server_add(name, host, port, username, password):
    """
    添加服务配置
    :param name: 服务器名称
    :param host: 服务器地址
    :param port: 服务器ssh端口
    :param username: 服务器用户名
    :param password: 服务器用户密码
    :return:
    """
    # 追加模式
    y_file = open(server_config_default_file, 'a+')
    sc = ServerConfig(name=name, host=host, port=port, username=username, password=password)
    yaml.safe_dump([sc.__dict__], y_file)
    click.echo('\n录入的服务器信息:\n名称:{}\n地址:{}\nssh端口:{}\n密码:{}'.format(name, host, port, password))


def server_edit():
    os.system('vi {}'.format(server_config_default_file))


def server_remove(name):
    """
    删除服务器配置信息
    获取所有配置  删除其中name符合的数据
    :param name: 服务器名称
    :return:
    """
    y_read_file = open(server_config_default_file, 'r')
    config_list = yaml.safe_load(y_read_file)
    if config_list is None:
        click.echo("暂无服务器配置信息!")
        return
    # 深拷贝 配置列表 进行操作列表
    new_config_list = copy.deepcopy(config_list)
    for c in config_list:
        sc = ServerConfig.to_obj(c)
        if sc.name == name:
            new_config_list.remove(c)
            click.echo("删除{}服务器".format(sc.name))
    # 重新打开链接
    if len(new_config_list) != 0:
        yaml.safe_dump(new_config_list, open(server_config_default_file, 'w+'))
    else:
        # 清空配置
        open(server_config_default_file, 'w+').truncate()
        click.echo("服务器配置已清空!")


def server_list():
    config_file = pathlib.Path(server_config_default_file)
    if not config_file.exists():
        click.echo("暂无服务器配置信息！")
        return
    if not config_file.is_file():
        click.echo("{}不是配置文件".format(server_config_default_file))
        return
    y_read_file = open(server_config_default_file, 'r')
    config_list = yaml.safe_load(y_read_file)
    if config_list is None:
        click.echo("暂无服务器配置信息!")
        return
    config_str = '服务器配置信息:\n'
    for index, c in enumerate(config_list):
        sc = ServerConfig.to_obj(c)
        config_str += '第{}台服务器名称:{},地址:{},端口:{}'.format(index + 1, sc.name, sc.host, str(sc.port) + '\n')
    config_str += "\n共{}台服务器\n".format(len(config_list))
    click.echo(config_str)


def server_connect(name):
    click.echo("连接{}服务器...".format(name))
    config_list = yaml.safe_load(open(server_config_default_file, 'r'))
    if config_list is None:
        click.echo("暂无{}服务器配置信息!".format(name))
        return
    connect_sc = None
    for c in config_list:
        sc = ServerConfig.to_obj(c)
        if sc.name == name:
            connect_sc = sc
            break
    if connect_sc is None:
        click.echo("不存在{}服务器配置！".format(name))
        return
    open_ssh_tty(connect_sc.host, connect_sc.port, connect_sc.username, connect_sc.password)


def open_ssh_tty(host, port, username, password):
    # https://www.cnblogs.com/langqi250/p/10141295.html
    # 建立一个socket
    trans = paramiko.Transport((host, port))
    # 启动一个客户端
    trans.start_client()

    # 如果使用用户名和密码登录
    trans.auth_password(username=username, password=password)
    # 打开一个通道
    channel = trans.open_session()
    # 获取终端  配置为当前终端宽高
    terminal_size = os.get_terminal_size()
    channel.get_pty(width=terminal_size.columns, height=terminal_size.lines)
    # 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
    channel.invoke_shell()

    # 获取原操作终端属性
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        # 将现在的操作终端属性设置为服务器上的原生终端属性,可以支持tab了
        tty.setraw(sys.stdin)
        channel.settimeout(0)
        while True:
            readlist, writelist, errlist = select.select([channel, sys.stdin, ], [], [])
            # 如果是用户输入命令了,sys.stdin发生变化
            if sys.stdin in readlist:
                # 获取输入的内容，输入一个字符发送1个字符
                input_cmd = sys.stdin.read(1)
                # 将命令发送给服务器
                channel.sendall(input_cmd)

            # 服务器返回了结果,channel通道接受到结果,发生变化 select感知到
            if channel in readlist:
                # 获取结果
                result = channel.recv(1024)
                # 断开连接后退出
                if len(result) == 0:
                    print("\r\n退出{}用户,ip:{}服务器 \r\n".format(username, host))
                    break
                # 输出到屏幕
                sys.stdout.write(result.decode())
                sys.stdout.flush()
    except RuntimeError as err:
        raise click.echo("连接远程服务器异常.....{}".format(err))
    finally:
        # 执行完后将现在的终端属性恢复为原操作终端属性
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    # 关闭通道
    channel.close()
    # 关闭链接
    trans.close()


class ServerConfig(object):
    """
    服务器配置模板class
    """
    # 名字
    name: str
    # 地址
    host: str
    # ssh端口
    port: int
    # 服务器用户名
    username: str
    # 密码
    password: str
    # 密钥位置
    secretKeyPath: str

    def __init__(self, name, host, port, username, password):
        self.name = name
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @staticmethod
    def to_obj(d: dict):
        """
        将读取的dict 转换为 serverConfig
        :param d:  dict
        :return: ServerConfig
        """
        return ServerConfig(name=d['name'], host=d['host'], port=d['port'], username=d['username'],
                            password=d['password'])
