from collections import OrderedDict
import urllib.parse
import json
import hashlib
import random


def ksort(value):
    list_dict = [(k, value[k]) for k in sorted(value.keys())]
    res = dict(list_dict)
    return res


class PayBox():
    host_url = ""
    context = {
        'pg_encoding': 'UTF-8',  # charset
        'pg_currency': 'KZT',  # currency of payment, default is KZT
        'pg_lifetime': 86400,
        'pg_result_url': host_url + 'pay?status=paying',  # url to which we will send the payment result
        'pg_request_method': 'GET',  # you can use GET, POST, XML
        'pg_salt': random.randint(21, 43433),  # salt that will be used in encrypting the request
        'pg_success_url': host_url + 'pay/result/?status=success',
        'pg_failure_url': host_url + 'pay/result/?status=failed',
        'pg_testing_mode': 1
    }
    secretWord = ""
    url = 'payment.php'
    merchant_id = '',

    def __init__(self, host_url, context, secret_word, merchant_id):
        self.host_url = host_url
        self.secret_word = secret_word
        self.merchant_id = merchant_id
        self.context = context

    def paying(self, pg_amount=0, pg_order_id="", pg_user_phone="", pg_description="", pg_user_ip="", pg_user_id=""):
        context = self.context
        context['pg_amount'] = pg_amount
        context['pg_description'] = pg_description
        context['pg_order_id'] = pg_order_id
        context['pg_user_phone'] = pg_user_phone
        context['pg_user_ip'] = pg_user_ip
        context['pg_user_id'] = pg_user_id
        context['pg_merchant_id'] = self.merchant_id


        resp = ksort(context)
        dr = OrderedDict(resp)

        dr.update({0: self.url})
        dr.move_to_end(0, last=False)

        dr.update({1: self.secret_word})
        output_json = json.loads(json.dumps(dr))
        output_dict = dict(output_json)
        output_string = ""
        for key, value in output_dict.items():
            if key != '1':
                output_string = output_string + str(value) + ';'
            else:
                output_string = output_string + str(value)

        output_md5_string = hashlib.md5(output_string.encode())

        context = ksort(context)
        context['pg_sig'] = output_md5_string.hexdigest()
        result = urllib.parse.urlencode(context)
        result_url = "https://paybox.kz/" + self.url + '?' + result
        return result_url


