# -*- coding:utf-8 -*-
# @author :adolf
import json
from flask import Flask
from flask import request
import traceback
from rpa_ocr.verification_service.verification_main import ocr_pipeline_main
from flask_cors import CORS

"""
support ocr服务
"""
app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/verification_service/', methods=["post", "get"], strict_slashes=False)
def service_main():
    try:
        in_json = request.get_data()
        if in_json is not None:
            in_dict = json.loads(in_json.decode("utf-8"))
            image_with_base64 = in_dict['image']
            scenes = in_dict['scenes']

            result_dict = dict()
            result = ocr_pipeline_main(image_with_base64, scenes)
            result_dict['result'] = result

            return json.dumps(result_dict, ensure_ascii=False)
        else:
            return json.dumps({"error_msg": "data is None", "status": 1}, ensure_ascii=False)
    except Exception as e:
        traceback.print_exc()
        return json.dumps({"error_msg": "unknown error:" + repr(e), "status": 1}, ensure_ascii=False)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2001, debug=True)
