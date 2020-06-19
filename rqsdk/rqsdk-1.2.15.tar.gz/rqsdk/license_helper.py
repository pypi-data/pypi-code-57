# -*- coding: utf-8 -*-
#
# Copyright 2016 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import re
import sys

import click
import requests
import rqdatac
from rqdatac.share.errors import AuthenticationFailed
from tabulate import tabulate

from rqsdk.const import PERMISSIONS_INFO_URL, RQDATAC_DEFAULT_ADDRESS
from rqsdk.script_update import update_bash_file


def format_rqdatac_uri(uri):
    """
    整理rqdatac_uri 并返回
    uri可能有以下三种方式
    * 纯license
    * 手机号:密码
    * 完整的rqdatac_uri
    """
    if uri is None:
        raise ValueError("参数异常")

    if ":" not in uri:
        uri = "license:{}".format(uri)

    if '@' not in uri:
        uri = "tcp://{}@{}".format(uri, RQDATAC_DEFAULT_ADDRESS)

    if not re.match(r"\w*://.+:.+@.+:\d+", uri):
        raise ValueError('无效的 rqdatac_uri ,格式应为 user:password 或者 tcp://user:password@ip:port')

    os.environ['RQDATAC2_CONF'] = uri
    return uri


def get_permissions_info(rqdtac_uri):
    """访问米筐官网获取license信息"""
    resp = requests.get(PERMISSIONS_INFO_URL, params={"rqdatac_uri": rqdtac_uri})

    res = resp.json()
    if res['code'] != 0:
        raise Exception("获取license权限信息错误\nuri={}\n{}\n".format(rqdtac_uri, res.get("message")))
    return res['data']


def print_rqdata_info(rqdatac_uri):
    """展示 rqdata_uri 账户的相关信息"""
    if not rqdatac_uri:
        click.echo("当前环境无license")
        return False
    elif not verify_uri(rqdatac_uri):
        click.echo("当前环境license不可用 license={}".format(rqdatac_uri))
        return False

    try:
        rqdatac.init(uri=rqdatac_uri)
        _info = rqdatac.user.get_quota()
        permissions_info = get_permissions_info(rqdatac_uri)
        table_data = permissions_info["permissions_table"]
        data = [[i["name"], i["type"], i["back_test_level"], i["enable"]] for i in table_data]

        tb = tabulate(data, headers=["产品", "标的品种", "频率", "开启"], tablefmt="rst")
        width = tb.find("\n")
        click.echo("=" * width + tb[width:-width] + "=" * width)
        row = []
        if "rqdata_limit__license_type__full" in permissions_info["current_permissions"]:
            pass
        elif "rqdata_limit__license_type__edu" in permissions_info["current_permissions"]:
            row += ["教育版 |"]
        else:
            row += ["试用版 |"]

        if _info['bytes_limit'] == 0:
            row += ["流量限制:该 license 无流量限制 |"]
        else:
            row += ["流量限制: {:.2f} MB |".format(_info['bytes_limit'] / 2 ** 20)]
            row += ["剩余流量: {:.2f} MB |".format((_info['bytes_limit'] - _info['bytes_used']) / 2 ** 20)]
        row += ["剩余有效天数: {} |".format(_info['remaining_days'])]

        click.echo(tabulate([row], tablefmt="plain"))
        click.echo("=" * width)
        for i in range(int(len(rqdatac_uri) / width) + 1):
            click.echo(rqdatac_uri[i * width:(i + 1) * width])
        click.echo("=" * width)
    except AuthenticationFailed as r:
        click.echo("=" * 50)
        click.echo("登录失败，该 license 或用户无法用于初始化 rqdatac\n{}".format(rqdatac_uri))
        click.echo("请联系商务或技术支持")
        click.echo("=" * 50)
        return False
    return True


def set_to_environ(rqdatac_uri):
    """将rqdatac_uri设置为环境变量"""
    if sys.platform.startswith("win"):
        os.popen("setx RQDATAC2_CONF {uri} ".format(uri=rqdatac_uri))
    else:
        update_bash_file(rqdatac_uri)
    click.echo("当前 license 已设置为 {uri}".format(uri=rqdatac_uri))
    click.echo("请重启当前的 terminal ".format(uri=rqdatac_uri))


def verify_uri(uri):
    """验证uri是否可以登录rqdatac"""
    try:
        rqdatac.init(uri=uri)
        rqdatac.user.get_quota()  # for raise AuthenticationFailed
    except AuthenticationFailed as r:
        return False
    return uri


def license_console(rqdatac_uri):
    """license 交互环境"""
    while True:
        # print
        print_rqdata_info(rqdatac_uri)

        # input
        click.echo('如需修改请按照【用户名:密码】的格式输入您的用户名密码或直接键入license key。')
        click.echo('不更改则按 Enter 键退出')
        rqdatac_uri = input()
        if not rqdatac_uri:
            return
        rqdatac_uri = format_rqdatac_uri(rqdatac_uri)
        if verify_uri(rqdatac_uri):
            print_rqdata_info(rqdatac_uri)
            set_to_environ(rqdatac_uri)
            return
