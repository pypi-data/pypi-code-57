import requests
import json
def get_secret(secret):
    import time
    import hmac
    import hashlib
    import base64
    import urllib.parse
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return [timestamp,sign]
def to_btns(title_list,actionURL_List):
    out =[]
    out1 = {}
    for i in range(len(title_list)):
        out.append({"title":title_list[i],"actionURL":actionURL_List[i]})
    out1["btns"] = out
    return out1
def to_links(title_list,messageURL_list,picURL_list):
    out = []
    for i in range(len(title_list)):
        out.append({"title":title_list[i],"messageURL":messageURL_list[i],"picURL":picURL_list[i]})
    return out
class robot:
    def __init__(self,token,secret):
        self.token = token
        self.secret = secret
        self.headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
    def send_text(self,content,At=False,):
        if At == "All":
            data = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "at": {
                    "isAtAll": True  # @全体成员（在此可设置@特定某人）
                }
            }
            self.sign = get_secret(self.secret)
            url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
            r = requests.post(url=url,data=json.dumps(data),headers=self.headers)
            return r.json()
        elif type(At) == list:
            data = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
                "at": {
                    "atMobiles":At
                }
            }
            self.sign = get_secret(self.secret)
            url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
            r = requests.post(url=url, data=json.dumps(data), headers=self.headers)
            return r.json()
        else:
            data = {
                "msgtype": "text",
                "text": {
                    "content": content
                },
            }
            self.sign = get_secret(self.secret)
            url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
            r = requests.post(url=url,data=json.dumps(data),headers=self.headers)
            return r.json()
    def send_link(self,text,title,url,img_url=""):
        if True:
            data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title,
                "picUrl": img_url,
                "messageUrl": url
            }
        }
            self.sign = get_secret(self.secret)
            url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
            r = requests.post(url=url,data=json.dumps(data),headers=self.headers)
            return r.json()
    def send_markdown(self,title,markdown_text,At=False):
        if At == "All":
            data = {
                "msgtype": "markdown",
                "markdown":{
                    "title":title,
                    "text":markdown_text
                },
                "at": {
                    "isAtAll": True  # @全体成员（在此可设置@特定某人）
                }
            }
            self.sign = get_secret(self.secret)
            url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
            r = requests.post(url=url,data=json.dumps(data),headers=self.headers)
            return r.json()
        elif type(At) == list:
            data = {
                "msgtype": "markdown",
                "markdown":{
                    "title":title,
                    "text":markdown_text
                },
                "at": {
                    "atMobiles":At
                }
            }
            self.sign = get_secret(self.secret)
            url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
            r = requests.post(url=url, data=json.dumps(data), headers=self.headers)
            return r.json()
        else:
            data = {
                "msgtype": "markdown",
                "markdown":{
                    "title":title,
                    "text":markdown_text
                },
            }
            self.sign = get_secret(self.secret)
            url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
            r = requests.post(url=url,data=json.dumps(data),headers=self.headers)
            return r.json()
    def send_ztActionCard(self,title,markdown_text,singleTitle,singleURL,btnOrientation):
        data = dict(actionCard={
            "title": title,
            "text": markdown_text,
            "btnOrientation": btnOrientation,
            "singleTitle": singleTitle,
            "singleURL": singleURL
        }, msgtype="actionCard")
        self.sign = get_secret(self.secret)
        url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
        r = requests.post(url=url, data=json.dumps(data), headers=self.headers)
        return r.json()
    def send_dlActionCard(self,title,markdown_text,btns,btnOrientation):
        data = {
    "actionCard": {
        "title":title,
        "text": markdown_text,
        "btnOrientation": btnOrientation,
        "btns": btns
    },
    "msgtype": "actionCard"
}
        self.sign = get_secret(self.secret)
        url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
        r = requests.post(url=url, data=json.dumps(data), headers=self.headers)
        return r.json()
    def send_FeedCard(self,links):
        data = {
            "feedCard": {
                "links": links
            },
            "msgtype": "feedCard"
        }
        self.sign = get_secret(self.secret)
        url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}&timestamp={self.sign[0]}&sign={self.sign[1]}"
        r = requests.post(url=url, data=json.dumps(data), headers=self.headers)
        return r.json()