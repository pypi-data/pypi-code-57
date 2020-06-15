# -*- coding:utf-8 -*-
# @author :adolf
import os
import json
from flask import Flask
from flask import request
from werkzeug.utils import secure_filename
import traceback
import sys
from flask_cors import CORS

"""
只要用于服务器的文件上传
"""
app = Flask(__name__)
CORS(app, resources=r'/*')

upload_file_folder = os.path.join(os.getcwd(), 'model')


def upload():
    file = request.files['files']

    if check_file_type(file.filename):
        file.save(os.path.join(upload_file_folder, file.filename))


def check_file_type(filename):
    file_type = ['pth']
    # 获取文件后缀
    ext = filename.split('.')[1]
    # 判断文件是否是允许上传得类型
    if ext in file_type:
        return True
    else:
        return False


@app.route('/upload_service/', methods=["post", "get"], strict_slashes=False)
def upload_model_file():
    try:
        if request.method == 'POST':
            f = request.files['file']
            if f is not None:
                base_path = sys.path[0]  # 项目的根目录 boot_main.py目录
                if not os.path.exists(os.path.join(base_path, 'model')):
                    os.mkdir(os.path.join(base_path, 'model'))
                upload_path = os.path.join(base_path, 'model',
                                           secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
                f.save(upload_path)
                return json.dumps({"status": 0}, ensure_ascii=False)
            else:
                return json.dumps({"error_msg": "data is None", "status": 1}, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps({"error_msg": "unknown error:" + repr(e), "status": 1}, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020, debug=True)
