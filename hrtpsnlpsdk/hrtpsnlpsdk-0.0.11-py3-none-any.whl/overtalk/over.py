import json

import requests


class OvertalkDetector(object):

    def __init__(self, host="behavior-model.answer.private.hrtps.com", port=80, over_version="overtalk-0.0.4"):
        """

        :param host: behavior-model.answer.private.hrtps.com 是内网域名，该域名只可以在内网访问
        :param port:
        :param over_version:
        """
        self.sess = requests.Session()
        self.host = host
        self.port = port
        self.over_version = over_version

    def detect_overtalk(self, text: str, lang: str):
        """

        :param text:
        :param lang:  zh-simple en fr
        :return:
        """
        if lang not in ["zh-simple", "en", "fr"]:
            raise Exception("overtalk lang not support error, raise  [zh-simple,en,fr]")
        else:
            per_url = f"http://{self.host}:{self.port}/{self.over_version}/api/v1/contain"
            req_data = {
                "text": text,
                "lang": lang
            }
            resp = self.sess.post(per_url, json=req_data).text
            prescore_val = json.loads(resp, encoding="utf-8")['prescore']
            return float(prescore_val)

    def detect_overtalk_batch(self, texts: list, lang: str):
        """

        :param texts:
        :param lang:  zh-simple en fr
        :return:
        """
        per_url = f"http://{self.host}:{self.port}/{self.over_version}/api/v1/contain-batch"
        req_data = {
            "text": texts,
            "lang": lang
        }
        resp = self.sess.post(per_url, json=req_data).text
        prescores = json.loads(resp, encoding="utf-8")['prescore']
        return [float(p) for p in prescores]
