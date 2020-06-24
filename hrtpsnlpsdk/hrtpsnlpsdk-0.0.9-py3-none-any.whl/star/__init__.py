import os
from typing import List

import numpy as np
import requests
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from .thriftio import STARService
from ..kashgari.process import load_processor
from ..utils.text_utils import min_len_sen_tokenizer, tokenize


class STARDetecter(object):

    def __init__(self, host="115.159.102.194", port=16113):
        """
        调用 WEB API
        115.159.102.194 是测试服务器
        """
        self.host = host
        self.port = port

    @classmethod
    def _predict_sen(cls, sub_sen_text, client):
        sub_pre_label = client.star_detect(sub_sen_text)
        return sub_pre_label

    def predict_proportion(self, texts: List):
        """
        计算比例


        [
            {
                "tag":[
                    {
                        "name":"句子类型",
                        "offset":"",
                        "length":""
                    }
                ]
            }
        ]
        :param texts:
        :return:
        """
        all_len_dic = []
        for text in texts:
            len_dic = {}
            all_len = len(text)
            for p in self.predict_doc(text):
                sub_pre_label, sub_sen_text, sub_sen_ind, sub_sen_len = p
                if sub_pre_label not in len_dic.keys():
                    len_dic[sub_pre_label] = (sub_sen_len / all_len)
                else:
                    len_dic[sub_pre_label] += (sub_sen_len / all_len)
            all_len_dic.append(len_dic)
        return all_len_dic

    def predict_doc(self, doc_text: str, sen_split="。!?！？：；;:", min_sen_len=64):
        """

        :param doc_text: 长文本
        :param sen_split:  切分句子分隔符
        :param min_sen_len:  长句子切分窗口， 单句子过长则按照此长度平均切分
        :return:
        """
        transport = TSocket.TSocket(self.host, self.port)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        thrift_client = STARService.Client(protocol)
        transport.open()

        sub_sens = min_len_sen_tokenizer(doc_text, split_set=sen_split, minlen=min_sen_len)

        for sub_sen in sub_sens:
            sub_sen_text, sub_sen_ind, sub_sen_len = sub_sen
            sub_sen_text = "".join(sub_sen_text)
            sub_pre_label = self._predict_sen(sub_sen_text, thrift_client)
            yield sub_pre_label, sub_sen_text, sub_sen_ind, sub_sen_len
        transport.close()

    def predict_position(self, texts: List, **kwargs) -> List:
        """
        :return:
                [
                    {
                        "tag":[
                            {
                                "name":"句子类型",
                                "offset":"",
                                "length":""
                            }
                        ]
                    }
                ]
        :param texts:
        """
        pre_result = []
        for text in texts:
            tags = []
            # 行文本切分后预测
            for p in self.predict_doc(text, kwargs):
                sub_pre_label, sub_sen_text, sub_sen_ind, sub_sen_len = p
                tags.append({
                    "name": f"{sub_pre_label}",
                    "offset": sub_sen_ind,
                    "length": sub_sen_len,
                })
            pre_result.append({"tag": tags})
        return pre_result


class STARSequenceDetecter(object):

    def __init__(self, host="115.159.102.194", port=80):
        """
        调用 WEB API
        115.159.102.194 是测试服务器
        """
        self.host = host
        self.port = port
        model_mess_path = os.path.dirname(__file__)
        # self.situation_processor =
        # self.action_processor = load_processor(os.path.join(model_mess_path, "..", "data", "starner", "action", "model_info.json"))
        # self.result_processor = load_processor(os.path.join(model_mess_path, "..", "data", "starner", "result", "model_info.json"))

        self.process_dic = {
            "situation": load_processor(
                os.path.join(model_mess_path, "..", "data", "starner", "situation", "model_info.json")),
            "action": load_processor(
                os.path.join(model_mess_path, "..", "data", "starner", "action", "model_info.json")),
            "result": load_processor(
                os.path.join(model_mess_path, "..", "data", "starner", "result", "model_info.json"))
        }
        self.req_url_dic = {
            "situation": "http://model.ai-api.hrtps.com/v1/models/bilstm_BIEO_td_situation_epoch5_batch32_seq512_appendsele:predict",
            "action": "http://model.ai-api.hrtps.com/v1/models/bilstm_BIEO_td_action_epoch5_batch32_seq512_appendsele:predict",
            "result": "http://model.ai-api.hrtps.com/v1/models/bilstm_BIEO_td_result_epoch3_batch32_seq512_appendsele:predict",
        }

    def predict(self, texts, tp):
        processor = self.process_dic[tp]
        req_url = self.req_url_dic[tp]
        tensor = processor.process_x_dataset(texts)
        tensor = [{
            "Input-Token:0": i.tolist(),
            "Input-Segment:0": np.zeros(i.shape).tolist()
        } for i in tensor]

        r = requests.post(req_url, json={"instances": tensor})
        preds = r.json()['predictions']
        return preds, processor.idx2label

    def trans_seq_index(self, seq_list):
        tag_dic = []
        seq_start = 0
        seq_len = 0
        last_label = "O"
        for i, s in enumerate(seq_list):

            if "-" in s:
                s = s.split("-")[1]
            elif s != "O":
                s = s.replace("[PAD]", "O")

            if s != "O" and i == 0:
                seq_start = i
                seq_len += 1
                last_label = s
            elif s == last_label and s != "O":
                seq_len += 1
            elif s != last_label and last_label == "O":
                seq_start = i
                seq_len = 1
                last_label = s
            elif s != last_label and last_label != "O":
                tag_dic.append(
                    {
                        "name": last_label,
                        "offset": seq_start,
                        "length": seq_len,
                    }
                )
                seq_start = i
                seq_len = 0
                last_label = s

        return tag_dic

    def predict_position(self, texts: List, **kwargs) -> List:
        """
        :return:
                [
                    {
                        "tag":[
                            {
                                "name":"句子类型",
                                "offset":"",
                                "length":""
                            }
                        ]
                    }
                ]
        :param texts:
        """
        pre_result = []
        texts = [tokenize(t) for t in texts]
        situation_pres, lab_dic_situation = self.predict(texts, "situation")
        action_pres, lab_dic_action = self.predict(texts, "action")
        result_pres, lab_dic_result = self.predict(texts, "result")
        lab_dic = {}

        for k in lab_dic_situation.keys():
            v = lab_dic_situation[k]
            lab_dic[k] = v
        for k in lab_dic_action.keys():
            v = lab_dic_action[k]
            lab_dic[k + 5] = v
        for k in lab_dic_result.keys():
            v = lab_dic_result[k]
            lab_dic[k + 10] = v

        for i, action_pre in enumerate(action_pres):
            situation_pre = situation_pres[i]
            result_pre = result_pres[i]

            mg_pre = np.concatenate([situation_pre, action_pre, result_pre], axis=1)

            labels = []
            for pre_ind, probs in enumerate(mg_pre):

                for prob_i, prob in enumerate(probs):
                    label = lab_dic[prob_i]
                    if prob > 0.8 and label != "O" and label != "[PAD]":
                        labels.append(label)
                        break
                if (len(labels) - 1) != pre_ind:
                    labels.append("O")

            tag_dic = self.trans_seq_index(labels)

            pre_result.append(
                {
                    "tag": tag_dic
                }
            )

        return pre_result
