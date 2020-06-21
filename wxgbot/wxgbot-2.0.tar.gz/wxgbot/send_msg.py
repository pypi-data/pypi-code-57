#!/usr/bin/env python
# coding: utf-8
import requests
def send_text(text,bot):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot}"
    headers = {"Content-Type": "text/plain"}
    data = {
          "msgtype": "text",
          "text": {
             "content": text,
          }
       }
    r = requests.post(url, headers=headers, json=data)
    print(r.text)

def send_markdown(text,bot):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot}"
    data = {
    "msgtype": "markdown",
    "markdown": {
        "content": text
    }}
    r = requests.post(url,json=data)
    print(r.text)

def send_file(file_path,bot):
    file_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={bot}&type=file"
    file= {'file':open(file_path,'rb')}
    result = requests.post(file_url, files=file)
    file_id = eval(result.text)['media_id']
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot}"
    data = {
        "msgtype": "file",
        "file": {"media_id": file_id,}
    }
    r = requests.post(url, json=data)
    print(r.text)

def send_img(file_path,bot):
    with open(file_path,"rb") as f:
        base64_data = base64.b64encode(f.read())
    file = open(file_path, "rb")
    md = hashlib.md5()
    md.update(file.read())
    res1 = md.hexdigest()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot}"
    headers = {"Content-Type": "text/plain"}
    data = {
            "msgtype": "image",
            "image": {
                "base64": base64_data.decode('utf-8'),
                "md5": res1
            }
        }
    r = requests.post(url, headers=headers, json=data)
    print(r.text)