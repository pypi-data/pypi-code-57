import subprocess
from logging.config import fileConfig
import hmac
from flask import Flask, jsonify
from flask import request
import json, logging
from os import path
import sys

fileConfig("logging.ini")
logger = logging.getLogger()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def __do_deploy():
    """
        部署
    """
    curdir = path.dirname(path.abspath(__file__))
    deploy_script_file = app.config['deploy_script']
    cmd = f"bash  {deploy_script_file}"

    (status, output) = subprocess.getstatusoutput(cmd)
    return status, output


@app.route('/deploy', methods=['POST'])
def deploy():
    signature = request.headers.get('X-Hub-Signature')
    sha, signature = signature.split('=')
    secret = str.encode(app.config.get('webhook_sk'))
    hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()

    if not hmac.compare_digest(hashhex, signature):
        logger.error("部署失败")
        return json.dumps({"success": 1, "message": "accessKey error"}), 500
    deploy_result = {}
    logger.info("开始部署")
    deploy_result['success'], deploy_result['message'] = __do_deploy()
    logger.info("部署成功")
    status_code = 500 if deploy_result['success']==1 else 200
    return jsonify(deploy_result), status_code


def main(port=50001, sk='', deploy_script=''):
    app.config['webhook_sk'] = sk
    app.config['deploy_script'] = deploy_script
    app.run(port=port)


if __name__=="__main__":
    sk = sys.argv[1]
    main(sk=sk)

