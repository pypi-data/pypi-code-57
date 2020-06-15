# flake8: noqa: E402

"""
This test is created to make sure the framework for local testing
is working correctly.
"""

# added the main directory as the first path
from os.path import dirname
import sys
parent = dirname(dirname(__file__))
sys.path.insert(0, parent)

from worker.test import AppTestRun
from testcase.app import app_lambda


if __name__ == '__main__':
    collections = ['drilling-efficiency.mse']
    app = AppTestRun(app_lambda.lambda_handler, collections)
    app.run()
