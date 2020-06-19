# file: ezfuc.py
# Author: eamonn

from datetime import datetime
import warnings
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.text import MIMEText
import smtplib
import requests
from email.mime.application import MIMEApplication
import logging
from email.mime.text import MIMEText
import smtplib
warnings.filterwarnings("ignore")  # 忽略警告


class ezfuc(object):

    @staticmethod
    def retry(count=1):
        """
        方法报错重试
        """

        def dec(f):
            def ff(*args, **kwargs):
                ex = None
                for i in range(count):
                    try:
                        ans = f(*args, **kwargs)
                        return ans
                    except Exception as e:
                        ex = e
                        print(e)
                raise ex

            return ff

        return dec

    @staticmethod
    def md5(*arg):
        """
        md5加密
        :param arg:
        :return:
        """
        import hashlib
        hl = hashlib.md5()
        line = ''.join(list(map(lambda x: str(x), arg)))
        hl.update(line.encode(encoding='utf-8'))
        return hl.hexdigest()

    @staticmethod
    def get_first(arr, default=''):
        """
        不报错获取第一个
        :param arr:
        :param default:
        :return:
        """
        if isinstance(arr, list):
            if len(arr) > 0:
                return arr[0]
        return default

    @staticmethod
    def dict_to_object(res, default=''):
        """
        字典转为对象
        :param res:
        :return:
        """
        from munch import DefaultMunch
        if isinstance(res, str):
            return DefaultMunch.fromJSON(res, default)
        if isinstance(res, dict):
            return DefaultMunch.fromDict(res, default)

    @staticmethod
    def object_to_dict(res, ex="dict"):
        """
        对象转为字典
        :param res:
        :param ex:
        :return:
        """
        if ex == "dict":
            return res.toDict()
        if ex == "json":
            return res.toJSON()

    @staticmethod
    def parse_html(res_text, ex=''):
        """
        对网站代码进行指定格式解析
        :param res_text:
        :param ex:
        :return:
        """
        if isinstance(ex, list):
            if ex[0] == 're':
                import re
                rt = re.findall(ex[1], res_text)
                return res_text, ezfuc.get_first(rt)

            if ex[0] == 'func':
                res_text = ex[1](res_text)
                return res_text

        if ex == 'xpath':
            from lxml import etree
            try:
                selector = etree.HTML(res_text)
            except:
                html = bytes(bytearray(res_text, encoding='utf-8'))
                selector = etree.HTML(html)
            return res_text, selector

        if ex == 'jq':
            from lxml import etree
            from pyquery import PyQuery as pq
            try:
                doc = pq(etree.fromstring(res_text))
            except:
                doc = pq(res_text)
            return res_text, doc

    @staticmethod
    def struct_header(txt):
        """
        格式化header
        :param txt:
        :return:
        """
        arr = txt.split("\n")
        headers = {}
        for i in arr:
            if ": " in i:
                ic = i.split(": ")
                headers[ic[0].replace("\t", "").replace(" ", "")] = ic[1]
        return headers

    @staticmethod
    def struct_data(data):
        """
        结构化data
        :param data:
        :return:
        """
        if type(data) == str and data != '':
            import urllib.parse
            res_data = map(lambda te: te.split('='), urllib.parse.unquote(data).split('&'))
            data = {}
            for i in res_data:
                if i[0] not in data:
                    data[i[0]] = i[1]
                else:
                    if type(data[i[0]]) == str:
                        data[i[0]] = [data[i[0]]]
                    if type(data[i[0]]) == list:
                        data[i[0]].append(i[1])
        if isinstance(data, list):
            if data[1] == str:
                data = data[0]
        return data

    @staticmethod
    def timer():
        """
        计时器
        :return:
        """

        def deco(func):
            def wrapper(*arg, **kw):
                import time
                t0 = time.time()
                res = func(*arg, **kw)
                t = time.time() - t0
                t = 0.1 if t == 0.0 else t
                print("\033[31m%s 方法运行时间为：%.4fs\033[0m" % (func.__name__, t))
                return res

            return wrapper

        return deco

    @staticmethod
    def sleep(t):
        """
        睡眠
        :param t:
        :return:
        """
        import time
        time.sleep(t)

    @staticmethod
    def pprint(arg):
        """
        格式化输出
        :param arg:
        :return:
        """
        from pprint import pprint
        pprint(arg)

    @staticmethod
    def toal_page(total, num):
        """
        计算总页数
        :param total:
        :param num:
        :return:
        """
        return (int(total) + int(num) - 1) // int(num)

    @staticmethod
    def init():
        """
        初始化工作环境
        :return:
        """
        import os, sys
        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        path = path.replace('\\', '/') + '/'
        os.chdir(path)

    @staticmethod
    def replace_plus(text, which, to_what=''):
        """
        同时对字符串里多个字符进行替换
        :param text:
        :param which:
        :param to_what:
        :return:
        """
        if text:
            for i in which:
                text = text.replace(i, to_what)
            return text
        return text

    @staticmethod
    def random_ua():
        """
        随机浏览器头
        :return:
        """
        import random
        user_agent_list = [
            'Mozilla/5.0 (Windows NT {WindowsNT};{WOW64}{language} rv:{Firefox}) Gecko/{builddata} Firefox/{Firefox}'.format(
                **{'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10.0"]),
                   'WOW64': random.choice(["", " WOW64;", " Win64;", " x64;"]),
                   'language': random.choice(["", " {};".format("zh-CN")]), 'builddata': random.choice(
                        ["201{}0{}{}".format(random.randint(0, 6), random.randint(1, 9), random.randint(10, 28))]),
                   'Firefox': random.choice(
                       ["50.0.1", "50.0.2", "50.0", "50.01", "50.010", "50.011", "50.02", "50.03", "50.04", "50.05",
                        "50.06", "50.07", "50.08", "50.09", "50.1.0", "51.0.1", "51.0", "51.01", "51.010", "51.011",
                        "51.012", "51.013", "51.014", "51.02", "51.03", "51.04", "51.05", "51.06", "51.07", "51.08",
                        "51.09", "52.0.1", "52.0.2", "52.0", "52.01", "52.02", "52.03", "52.04", "52.05", "52.06",
                        "52.07", "52.08", "52.09", "52.1.0", "52.1.1", "52.1.2", "52.2.0", "52.2.1", "52.3.0", "52.4.0",
                        "52.4.1", "53.0.2", "53.0.3", "53.0", "53.01", "53.010", "53.02", "53.03", "53.04", "53.05",
                        "53.06", "53.07", "53.08", "53.09", "54.0.1", "54.0", "54.01", "54.010", "54.011", "54.012",
                        "54.013", "54.02", "54.03", "54.04", "54.05", "54.06", "54.07", "54.08", "54.09", "55.0.1",
                        "55.0.2", "55.0.3", "55.0", "55.01", "55.010", "55.011", "55.012", "55.013", "55.02", "55.03",
                        "55.04", "55.05", "55.06", "55.07", "55.08", "55.09", "56.0.1", "56.0", "56.01", "56.010",
                        "56.011", "56.012", "56.02", "56.03", "56.04", "56.05", "56.06", "56.07", "56.08", "56.09",
                        "57.03", "57.04", "57.05", "57.06"]), }),
            'Mozilla/5.0 (Windows NT {WindowsNT};{WOW64}{language}) AppleWebKit/{Safari} (KHTML, '
            'like Gecko) Chrome/{Chrome} Safari/{Safari}'.format(
                **{'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10"]),
                   'WOW64': random.choice(["", " WOW64;", " Win64;", " x64;"]),
                   'language': random.choice(["", " {};".format("zh-CN")]),
                   'Chrome': '{0}.{1}.{2}.{3}'.format(random.randint(50, 61), random.randint(0, 9),
                                                      random.randint(1000, 9999), random.randint(10, 99)),
                   'Safari': '{0}.{1}'.format(random.randint(100, 999), random.randint(0, 99)), }),
            'Mozilla/5.0 ({compatible}Windows NT {WindowsNT};{WOW64} MSIE {ie}.0; Trident/{Trident}.0;){Gecko}'.format(
                **{'compatible': random.choice(["", "compatible; "]),
                   'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10"]),
                   'WOW64': random.choice(["", " WOW64;", " Win64;", " x64;"]),
                   'ie': random.randint(10, 11), 'Trident': random.randint(5, 7),
                   'Gecko': random.choice(["", " like Gecko;"])}),
            'Mozilla/5.0 (Windows NT {WindowsNT}; MSIE 9.0;) Opera {opera1}.{opera2}'.format(
                **{'WindowsNT': random.choice(["6.1", "6.2", "6.3", "10"]),
                   'opera1': random.randint(10, 12), 'opera2': random.randint(10, 99)}),
        ]
        rs = random.choice(user_agent_list)  # 201706  firefox14 chrome63 ie9 opera2
        return rs

    @staticmethod
    def make_dir(path):
        """
        创建目录
        :param path:
        :return:
        """
        import os
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def UUID(*arg):
        import uuid
        """
        根据传过来的字符串进行"+"拼接后，进行uuid3加密
        :param args:
        :return:
        """
        line = ''.join(list(map(lambda x: str(x), arg)))
        uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, line)
        return str(uuid_str)

    @staticmethod
    def color_print(*arg, color="yellow"):
        color_code = 33
        if color.lower() == "red":
            color_code = 31
        if color.lower() == "green":
            color_code = 32
        if color.lower() == "blue":
            color_code = 34
        if color.lower() == "purple":
            color_code = 35

        st = ' '.join(list(map(lambda x: str(x), arg)))
        print(f'\033[1;{color_code}m{st}\033[0m')

    @staticmethod
    def save_excel(resList, excel_name, title=None, path=""):
        """
        将列表数据保存到表格
        :param resList:
        :param excel_name:
        :param title:
        :param path:
        :return:
        """
        import xlsxwriter
        from tqdm import tqdm

        file_name = f"{excel_name}.xlsx"
        if path:
            ezfuc.make_dir(path=path)
            file_name = path + file_name
        workbook = xlsxwriter.Workbook(file_name)
        sheet = workbook.add_worksheet('Sheet1')  # 创建一个sheet表格

        l = 0
        if not isinstance(resList[-1], list):
            resList = [list(i.values()) for i in resList]
        if title:
            resList.insert(0, title)
        print(resList)
        for line in tqdm(resList, ascii=True, desc=excel_name):
            r = 00
            for i in line:
                sheet.write(l, r, i)  # 一个一个将单元格数据写入
                r = r + 1
            l = l + 1
        workbook.close()


class format_time(object):
    """
    格式化时间
    """

    def __init__(self, old_time=''):
        if old_time:

            if isinstance(old_time, str):
                split_str = self.__parse_old_time(old_time)
                self.__time = datetime(split_str[0], split_str[1], split_str[2], split_str[3], split_str[4],
                                       split_str[5])

            if isinstance(old_time, datetime):
                self.__time = old_time

        else:
            self.__time = datetime.now()

    @staticmethod
    def __parse_old_time(old_time):
        time_list = old_time.split(',')
        time_list = [int(i) for i in time_list]
        lack = 6 - len(time_list)
        if lack:
            for i in range(lack):
                time_list.append(0)
        return time_list

    @property
    def detail_time(self):
        return self.__time.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def y_m_d(self):
        return self.__time.strftime('%Y-%m-%d')

    @property
    def ymd(self):
        return self.__time.strftime('%Y%m%d')

    @property
    def y_m(self):
        return self.__time.strftime('%Y-%m')

    @property
    def ym(self):
        return self.__time.strftime('%Y%m')

    @property
    def y(self):
        return self.__time.strftime('%Y')

    @property
    def h(self):
        return self.__time.strftime('%H')


class EmailSend(object):

    def __init__(self, email_host, email_port, email_pass):
        self.logging = logging.getLogger('Waring')
        self.__email_host = email_host
        self.__email_port = email_port
        self.__email_pass = email_pass

    def send_text_email(self, to_address, content, from_addr='email', subject='title'):
        message_text = MIMEText(content, 'plain', 'utf8')
        message_text['From'] = formataddr(["筑龙爬虫部", from_addr])
        message_text['To'] = to_address
        message_text['Subject'] = subject

        try:
            # 在创建客户端对象的同时，连接到邮箱服务器。
            client = smtplib.SMTP_SSL(host=self.__email_host, port=self.__email_port)
            login_result = client.login(from_addr, self.__email_pass)
            if login_result and login_result[0] == 235:
                print('登录成功')
                client.sendmail(from_addr, to_address, message_text.as_string())
                print('邮件发送成功')
            else:
                print('邮件发送异常：', login_result[0], login_result[1])
        except Exception as e:
            # print('连接邮箱服务器异常：',e)
            self.logging.error('连接邮箱服务器异常：{}'.format(e))

    def send_xlsx_email(self, to_address,  from_addr='email', subject='title', file_name=""):
        msg = MIMEMultipart()
        msg['From'] = formataddr(["筑龙爬虫部", from_addr])
        msg['To'] = to_address
        msg['Subject'] = subject
        xlsxpart = MIMEApplication(open(file_name, 'rb').read())
        xlsxpart.add_header('Content-Disposition', 'attachment',
                            filename=('gbk', '', file_name))
        msg.attach(xlsxpart)
        try:
            client = smtplib.SMTP_SSL(self.__email_host, self.__email_port)
            login_result = client.login(from_addr, self.__email_pass)
            if login_result and login_result[0] == 235:
                print('登录成功')
                client.sendmail(from_addr, to_address, msg.as_string())
                print('邮件发送成功')
            else:
                print('邮件发送异常：', login_result[0], login_result[1])
        except Exception as e:
            self.logging.error('连接邮箱服务器异常：{}'.format(e))



    def send_word_email(self):
        pass

    def send_video_email(self):
        pass


@ezfuc.retry(2)
def getIP():
    try:
        res = requests.get("http://192.168.18.8:39111/123",timeout=3).json()
    except:
        return None

    if res["code"] ==200:
        return res
    elif res["code"] ==300:
        ezfuc.color_print("添加白名单失败", color="yellow")
        ezfuc.sleep(2)
        getIP()



def ezproxy(req):
    res = getIP()
    if not res:
        return req
    try:
        req.meta["proxy"] = res["proxy"]
        return req
    except:
        return req