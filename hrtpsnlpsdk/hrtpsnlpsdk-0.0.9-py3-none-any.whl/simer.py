import json

import requests


class Simer(object):

    def __init__(self, host="tomcat.nlp.private.hrtps.com", port=80,
                 over_version="similarity-0.0.10-SNAPSHOT"):
        """

        :param host: behavior-model.answer.private.hrtps.com 是内网域名，该域名只可以在内网访问
        :param port:
        :param over_version:
        """
        self.sess = requests.Session()
        self.host = host
        self.port = port
        self.over_version = over_version

    def get_sim(self, text1: str, text2: str, lang: str):
        """

        :param text:
        :param lang:  zh-simple en fr
        :return:
        """
        if lang not in ["zh-simple"]:
            raise Exception("overtalk lang not support error, raise  [zh-simple]")
        else:
            per_url = f"http://{self.host}:{self.port}/{self.over_version}/api/v1/answer/sim"
            req_data = {
                "text1": text1,
                "text2": text2,
                "sim": "jaccard",
                "n": "2 3",
                "seg": "ngram"
            }
            resp = self.sess.post(per_url, json=req_data).text
            resp_json = json.loads(resp, encoding="utf-8")
            if 'sim' not in resp_json.keys():
                raise Exception(
                    f"err input: \ntext1  {text1} \ntext2  {text2} \n resp  {resp}"
                )
            prescore_val = json.loads(resp, encoding="utf-8")['sim']
            return float(prescore_val)

    def get_sim_batch(self, text1s: list, text2s: list, lang: str):
        for i, text1 in enumerate(text1s):
            text2 = text2s[i]
            yield self.get_sim(text1, text2, lang)


