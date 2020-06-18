#coding=utf-8
from uiautomator import device as d


print d.info
url = "http://img2.ryuedu.cn/upload/vote"
d.screenshot('task_image_name.jpg')
file_path = d.screenshot_custom()
print file_path
def _request_upload_post(url, path):
    if path:
        paths = {"userfile":path}
        headers={"Host":"img2.ryuedu.cn",
             "Connection":"Keep-Alive",
             "Accept-Encoding":"gzip",
             "User-Agent":"okhttp/3.11.0"}
        r = d.request_file("post", url, None, paths, headers)
        print r
        if r:
            return r

_request_upload_post(url, file_path)