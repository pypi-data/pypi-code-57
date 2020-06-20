import yagmail

from fundquant.data_get.jsl_data import JslEtf
from fundquant.data_get.lixinren_data import persist_monitor_data_hand
from fundquant.domain.send_email import SendEmail
from fundquant.main_interface.monitor import IndexMonitor


def do_job(n_days=7):
    try:
        JslEtf().persist_all_data()
        # persist_monitor_data_hand()
        IndexMonitor().monitor()
    except Exception as e:
        email_list = SendEmail.get_email_list()
        if email_list is not None and len(email_list) > 0:
            yag = yagmail.SMTP('858776278@qq.com', 'uurpxchfekfebahj', host='smtp.qq.com', port='465')
            yag.send(['murphyxiaoxi@163.com'], '指数跟踪', contents='数据获取异常:' + str(e))
        raise e


def persist_lxr_data_hand(cookie):
    persist_lxr_data_hand(cookie)


if __name__ == '__main__':
    do_job(7)
