#!/usr/bin/env python
# -*- encoding: utf8 -*-
"""
    WebReport Export
"""
import os
import re
import sys
import json
import textwrap

import requests

from cms.util import MyLogger, User


reload(sys)
sys.setdefaultencoding('utf-8')


BASE_URL = 'http://fr.novogene.com:8080/WebReport/ReportServer'

__author__ = 'suqingdong'
__author_email__ = 'suqingdong@novogene.com'


class WebReport(object):

    def __init__(self, username, password, logger=None):
        self.username = username
        self.password = password
        self.base_url = BASE_URL

        self.logger = logger or MyLogger()

        self.session = requests.session()

    def login(self):

        url = self.base_url + '?op=fs_load&cmd=login'

        payload = {
            'fr_username': self.username,
            'fr_password': self.password,
            'fr_remember': 'true',
        }
        resp = self.session.post(url, data=payload).json()

        if resp.get('fail'):
            self.logger.error('[{errorCode}] {errorMsg}'.format(**resp))
            return False

        self.logger.info('Login Successfully!')
        return True

    def get_sessionid(self, payload):
        resp = self.session.get(self.base_url, params=payload)
        sessionid = re.findall(r'sessionID=(\d+)', resp.text)[0]
        self.logger.info('SessionID: {}'.format(sessionid))
        return sessionid

    def list_transactiontype(self, rtype):
        """
        获取业务线编码，eg. 疾病研究部 1911
        """

        if rtype == '业务线':
            reportlet = 'CRM/kf/F009.cpt'
            widgetname = 'transactiontype'
        elif rtype == '合同':
            reportlet = 'CRM/kf/M112802.cpt'
            widgetname = 'profitname'

        payload = {'reportlet': reportlet}
        sessionid = self.get_sessionid(payload)

        payload = {
            'op': 'widget',
            'widgetname': widgetname,
            'sessionID': sessionid
        }
        resp = self.session.post(self.base_url, params=payload).json()
        print('#业务线序号\t业务线名称')
        for each in resp:
            print('{value}\t{text}'.format(**each))

    def fr_dialog(self, sessionid, formdata):
        payload = {
            'op': 'fr_dialog',
            'cmd': 'parameters_d',
            'sessionID': sessionid
        }

        self.logger.debug('search with: {}'.format(
            json.dumps(formdata, indent=2, ensure_ascii=False)))

        resp = self.session.post(self.base_url, params=payload, data=formdata)

        return resp.cookies

    def export_excel(self, sessionid, cookies, outfile):
        payload = {
            'op': 'export',
            'sessionID': sessionid,
            'format': 'excel',
            'extype': 'simple'
        }
        resp = self.session.get(
            self.base_url, params=payload, cookies=cookies, stream=True)

        with open(outfile, 'wb') as out:
            for chunk in resp.iter_content(chunk_size=1024):
                out.write(chunk)

        self.logger.info('\033[33msave excel: {}\033[0m'.format(outfile))

    def list_table(self, sessionid, cookies):
        payload = {
            'op': 'page_content',
            'sessionID': sessionid,
            'pn': '1',
        }
        resp = self.session.get(self.base_url, params=payload, cookies=cookies)

    def get_report_transaction(self, outfile, transactiontype=None, year=None, month=None, time_min=None, time_max=None, **kwargs):
        """
            业务线维度报表
        """
        payload = {
            'reportlet': '/CRM/kf/y102.cpt',
            'transactiontype': transactiontype,
            'year': year,
            'month': month,
            'time_min': time_min,
            'time_max': time_max,
        }

        self.logger.debug('payload:\n{}'.format(json.dumps(payload, indent=2, ensure_ascii=False)))
        sessionid = self.get_sessionid(payload)

        # get dialog
        formdata = {
            '__parameters__': {
                "LABELPROJECTNUM": "[9879][76ee][7f16][53f7]:",
                "PROJECTNUM": "",
                "LABELCONTRACTNO": "[5408][540c][53f7]:",
                "CONTRACTNO": "",
                "LABELCONFIRMSTATUS": "[786e][8ba4][7c7b][578b]:",
                "CONFIRMTYPE": "",
                "CONFIRMTYPE_TEMP": ""
            }
        }

        # 查询信息存储在cookies中
        cookies = self.fr_dialog(sessionid, formdata)

        # Excel Export
        self.export_excel(sessionid, cookies, outfile)

    def get_report_contract(self, outfile, transactiontype=None, year=None, month=None, **kwargs):
        """
            合同维度项目交付报表
        """
        payload = {
            'reportlet': '/CRM/kf/M112802.cpt',
        }
        sessionid = self.get_sessionid(payload)
        formdata = {
            'PROFITNAME': transactiontype,
            'YEAR': year,
            'MONTH': month,
            # 'QUARTER': 4,
            # 'HALFYEAR': 2,
            'TIMETYPE': 'y',
            'LABELWORKGROUPDESC_C_C_C_C_C_C_C_C': '[67e5][8be2][6761][4ef6]:',
            'LABELYEAR_C_C_C': '[5e74]:',
            'LABELDEPARTMENT_C_C_C_C_C': '[4e1a][52a1][7ebf]:',
            'LABELWORKGROUPDESC_C_C_C_C_C_C_C': '[8fd0][8425][7ecf][7406]:',
            'LABELWORKGROUPDESC_C_C_C_C_C_C_C_C_C': '[65f6][95f4][7ef4][5ea6]:',
            'OPERATOR': ''
        }
            
        cookies = self.fr_dialog(sessionid, formdata)

        self.export_excel(sessionid, cookies, outfile)


def main(**args):

    username = args['username']
    password = args['password']
    transactiontype = args['transactiontype']

    if isinstance(transactiontype, list):
        args['transactiontype'] = "','".join(transactiontype)

    logger = MyLogger('Report', **args)

    user = User(**args)
    username, password = user.get_user_pass()
    wr = WebReport(username, password, logger=logger)
    if wr.login():
        user.save(username, password)
    else:
        exit(1)

    if transactiontype == ['list']:
        wr.list_transactiontype(args['type'])
        exit()

    outfile = args['output']

    if args['type'] == '业务线':
        wr.get_report_transaction(outfile, **args)
    elif args['type'] == '合同':
        wr.get_report_contract(outfile, **args)


def parser_add_report(parser):

    parser.description = __doc__

    parser.epilog = textwrap.dedent('''
        \033[36mexamples:
            %(prog)s -tid 1911 -o report.1911.xlsx                 # 获取业务线维度的结算收入报表
            %(prog)s -tid 1911 -o report.1911.xlsx -type 合同      # 获取合同维度项目交付报表
            %(prog)s -tid 1924 1925 -o cancer.all.xlsx -type 合同  # 指定多个业务线
            %(prog)s -tid list                                     # 查看业务线维度的业务线代码列表
            %(prog)s -tid list -type 合同                          # 查看合同维度的业务线代码列表
        \033[0m
    ''')

    parser.add_argument('-tid', '--transactiontype',
                        help='the number of your transactiontype, use "list" to list all transactiontypes [default: %(default)s]',
                        nargs='+',
                        default='1911')

    parser.add_argument('-type',
                        '--type',
                        help='the type of report, choices=[%(choices)s] [default: %(default)s]',
                        choices=['业务线', '合同'],
                        default='业务线')

    parser.add_argument('-y', '--year', help='specify the year')
    parser.add_argument('-m', '--month', help='specify the month')

    parser.add_argument('-s', '--time-min', help='specify the start time, format: YYYY-MM-DD')
    parser.add_argument('-e', '--time-max', help='specify the end time, format: YYYY-MM-DD')

    parser.add_argument('-o', '--output',
                        help='the output filename [%(default)s]',
                        default='report.xlsx')

    parser.set_defaults(func=main)
