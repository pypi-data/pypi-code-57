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
import importlib
import os
import warnings

import click

from rqsdk.const import TAG_MAP, VERSION_MAP
from rqsdk.license_helper import format_rqdatac_uri, license_console, print_rqdata_info, set_to_environ, verify_uri
from rqsdk.script_update import pip_install


@click.group()
@click.help_option("-h", "--help")
def cli():
    """
    输入 rqsdk [COMMAND] --help 查看命令详情
    例如：rqsdk install --help
    """
    pass


@cli.command()
@click.argument('rqdatac_uri', default="", nargs=1)
def license(rqdatac_uri):
    """配置 license 到环境变量"""
    warnings.filterwarnings("ignore", message="rqdatac is already inited. Settings will be changed.")

    if rqdatac_uri == "info":
        uri = os.environ.get('RQDATAC2_CONF')
        if uri is None:
            click.echo("当前环境没有配置 license ")
        else:
            print_rqdata_info(uri)
        return

    elif rqdatac_uri != "":
        rqdatac_uri = format_rqdatac_uri(rqdatac_uri)
        if verify_uri(rqdatac_uri):
            print_rqdata_info(rqdatac_uri)
            set_to_environ(rqdatac_uri)
            return

    rqdatac_uri = rqdatac_uri or os.environ.get('RQDATAC2_CONF')
    license_console(rqdatac_uri)
    return


@cli.command()
@click.argument('product', default="", nargs=1)
@click.option('-i', '--index-url', default="https://pypi.douban.com/simple/", help="指定默认源", hidden=True)
def update(product, index_url):
    """
    更新 rqsdk 及使用 rqsdk 安装的产品。

    \b
    输入 rqsdk update <PRODUCT> 安装对应产品，<PRODUCT> 为空时默认更新已安装产品。例如:
        rqsdk update rqdatac
        rqsdk update

    <PRODUCT> 可选: rqdatac | rqfactor | rqoptimizer | rqalpha_plus

    \b
    * rqdatac - 金融数据API（默认已安装）
    * rqalpha_plus - 多资产回测引擎
    * rqoptimizer - 股票优化器
    * rqfactor - 因子投研和检验
    """
    if product != "":
        if product not in VERSION_MAP.keys():
            click.echo("PRODUCT可选为:{}\n,当前为{}。".format(list(VERSION_MAP.keys()), product))
            return
        key = [product]
    else:
        key = ["rqdatac"]
        try:
            import rqalpha_plus
            key.append("rqalpha_plus")
        except ImportError:
            try:
                import rqfactor
                key.append("rqfactor")
            except ImportError:
                pass
            try:
                import rqoptimizer2
                key.append('rqoptimizer')
            except ImportError:
                pass

    full_name = "rqsdk[{}]".format(",".join(key))
    click.echo("开始更新 {} 请稍后...".format(full_name))
    return pip_install(full_name, index_url)


@cli.command()
@click.argument('product', default="", nargs=1)
@click.option('-i', '--index-url', default="https://pypi.douban.com/simple/", help="指定默认源", hidden=True)
def install(product, index_url):
    """
    安装产品。

    \b
    输入 rqsdk install <PRODUCT> 安装对应产品。例如:
        rqsdk install rqdatac。

    <PRODUCT> 可选: rqdatac | rqfactor | rqoptimizer | rqalpha_plus

    \b
    * rqdatac - 金融数据API（默认已安装）
    * rqalpha_plus - 多资产回测引擎
    * rqoptimizer - 股票优化器
    * rqfactor - 因子投研和检验
    """

    if product == 'rqsdk':
        full_name = product
    elif product in VERSION_MAP.keys():
        from rqsdk import __version__
        full_name = "rqsdk[{}]=={}".format(product, __version__)
    elif product != "":
        click.echo("请输入正确的产品名称:{}。当前输入为{}".format(list(VERSION_MAP.keys()), product))
        return
    else:
        click.echo("请输入产品名称:{}".format(list(VERSION_MAP.keys())))
        return

    click.echo("开始安装 {} 请稍后...".format(product))
    return pip_install(full_name, index_url)


@cli.command()
def shell():
    """打开 ipython 并执行 rqdatac init"""
    import rqdatac
    rqdatac.init()
    try:
        from IPython import embed
    except ImportError:
        click.echo("请安装ipython:pip install ipython")
    else:
        embed()


@cli.command()
def version():
    """获取版本信息"""
    from rqsdk import __version__
    click.echo("rqsdk=={}".format(__version__))
    for item in VERSION_MAP['rqalpha_plus']:
        try:
            package_name = item.split("==")[0]
            _package = importlib.import_module(package_name)
            click.echo("{}=={}".format(package_name, _package.__version__))
        except:
            pass


@cli.command()
@click.option(
    '-d', '--data-bundle-path', default=os.path.expanduser('~/.rqalpha-plus'), type=click.Path(file_okay=False),
    help="bundle 目录，默认为 ~/.rqalpha-plus"
)
@click.option(
    "--base", default=False, is_flag=True,
    help="更新基础数据及日线，注意：任何回测都需要依赖基础数据"
)
@click.option(
    "--minbar", multiple=True, type=click.STRING,
    help="更新分钟线数据，可选的参数值有 [{}] 或 underlying_symbol 或 order_book_id".format(", ".join(TAG_MAP))
)
@click.option(
    "--tick", multiple=True, type=click.STRING,
    help="更新tick数据，可选的参数值有 [{}] 或 underlying_symbol 或 order_book_id".format(", ".join(TAG_MAP))
)
@click.option("--with-derivatives", is_flag=True, default=False, help="更新分钟线和 tick 时同时更新选择的合约的衍生品数据")
@click.option('-c', '--concurrency', type=click.INT, default=3, help="并行的线程数量，需要低于 rqdatac 的最大可用连接数")
@click.option('--smart', default=False, is_flag=True, help="检索本地已经存在的分钟线和 tick 数据，增量更新对应品种的数据和日线数据")
def update_data(data_bundle_path, base, minbar, tick, with_derivatives, concurrency, smart):
    """
    更新运行回测所需的历史数据

    \b
    例如：
    * 更新日线数据： rqsdk update-data --base
    * 更新股票、期权分钟数据： rqsdk update-data --minbar stock --minbar option
    * 更新鸡蛋期货合约tick数据： rqsdk update-data --tick JD
    * 更新豆粕1905及其合约的衍生品tick数据： rqsdk update-data --tick M1905 --with-derivatives
    * 更新已下载的分钟线和tick数据： rqsdk update-data --smart
    """
    if base is False and not minbar and not tick and smart is False:
        from click import Context
        ctx = Context(update_data)
        click.echo(update_data.get_help(ctx))
        return 1
    try:
        import rqdatac
        rqdatac.init()
    except ValueError as e:
        click.echo('rqdatac init failed with error: {}'.format(e))
        click.echo('请先使用rqsdk license 初始化')
        return 1

    try:
        from rqalpha_plus.bundle import update_bundle_from_rqdatac
        from rqalpha_plus.bundle import update_bundle_from_exist_file
        update_bundle_from_rqdatac(concurrency, data_bundle_path, base, minbar, tick, with_derivatives)
        if smart:
            update_bundle_from_exist_file(concurrency, data_bundle_path)
    except ImportError:
        click.echo("""请先使用'rqsdk install rqalpha_plus'安装rqalpha_plus""")


@cli.command()
@click.option(
    '-d', '--data-bundle-path', default=os.path.expanduser('~/.rqalpha-plus'), type=click.Path(file_okay=False),
    help="bundle 目录，默认为 ~/.rqalpha-plus"
)
@click.option("--sample", is_flag=True, help="下载数据样例")
@click.option('-f', '--file-path', default=None, help="指定的压缩文件包")
def download_data(data_bundle_path, sample=True, file_path=None):
    """
    下载样例回测数据。
    下载样例数据不使用rqdatac流量。
    """
    try:
        from rqalpha_plus.bundle import download_simple_bundle
        return download_simple_bundle(data_bundle_path, sample=sample, file_path=file_path)
    except ImportError:
        click.echo("""请先使用'rqsdk install rqalpha_plus'安装rqalpha_plus""")
