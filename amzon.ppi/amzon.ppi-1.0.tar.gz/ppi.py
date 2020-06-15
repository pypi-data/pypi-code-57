import sys
import subprocess
import os
import requests
a = sys.argv

b = a[1]
if b == "-uninstall":
    os.system("python -m uninstall ppi")
    

elif b == "-update":
    os.system("start python3 update.py")
elif b == "line":
    import urllib.request # ライブラリを取り込む


    # URL,保存するファイルのパスを指定
    url = "https://github.com/amzon-0021/ppi/raw/master/line-1.0.tar.gz" # 保存したいファイルのパスを指定
    save_name = "line.tar.gz" # test1.pngという名前で保存される。

    # ダウンロードを実行
    urllib.request.urlretrieve(url, save_name)
    
    cmd = [f"python", "-m", "pip", "install", "line.tar.gz"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print(res.stdout.decode("cp932"))

else:
    cmd = [f"python", "-m", "pip", "install", b]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    print(res.stdout.decode("cp932"))
    


    
    

